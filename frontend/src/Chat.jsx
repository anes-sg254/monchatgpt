import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [history, setHistory] = useState([]);
  const [selectedConv, setSelectedConv] = useState(null);
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Charger les messages depuis la base de données pour l'utilisateur 1
  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/messages/1");
        console.log("📅 Messages BDD :", response.data);
        const fetchedMessages = response.data.map(msg => ({
          sender: msg.sender,
          content: msg.content,
        }));

        // Construire l'historique avec paires user + model
        const userMessages = [];
        for (let i = 0; i < fetchedMessages.length; i++) {
          const msg = fetchedMessages[i];
          if (
            msg.sender === "user" &&
            i + 1 < fetchedMessages.length &&
            fetchedMessages[i + 1].sender === "model"
          ) {
            userMessages.push({
              id: i,
              title: msg.content.substring(0, 20) + "...",
              fullMessages: [msg, fetchedMessages[i + 1]],
            });
          }
        }
        setHistory(userMessages);
        setMessages([]); // Vider le chat
      } catch (err) {
        console.error("Erreur chargement messages :", err);
      }
    };

    fetchMessages();
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");

    try {
      await axios.post("http://127.0.0.1:5000/messages/", {
        conversation_id: 1,
        sender: "user",
        content: input,
      });
    } catch (err) {
      console.error("Erreur stockage user :", err);
    }

    try {
      const response = await axios.post("http://127.0.0.1:5000/messages/chat", {
        conversation_id: 1,
        sender: "user",
        content: input,
      });

      console.log("🔵 Réponse backend :", response.data);

      const modelMessage = { sender: "model", content: response.data.ai_response };
      const newMessages = [...updatedMessages, modelMessage];
      setMessages(newMessages);

      try {
        await axios.post("http://127.0.0.1:5000/messages/", {
          conversation_id: 1,
          sender: "model",
          content: response.data.ai_response,
        });
      } catch (err) {
        console.error("Erreur stockage model :", err);
      }

      const newConv = {
        id: Date.now(),
        title: input.substring(0, 20) + "...",
        fullMessages: newMessages,
      };
      setHistory([newConv, ...history]);
      setSelectedConv(newConv.id);
    } catch (error) {
      console.error("Erreur lors de l'envoi du message :", error);
    }
  };

  const handleSelectConversation = (convId) => {
    const conv = history.find((c) => c.id === convId);
    setMessages(conv.fullMessages);
    setSelectedConv(convId);
  };

  return (
    <div className="full-screen">
      <header className="header">
        <h1>MonChatGPT</h1>
      </header>
      <div className="app-layout">
        <div className="sidebar">
          <h2>Historique</h2>
          {history.map((conv) => (
            <div
              key={conv.id}
              className={`history-item ${selectedConv === conv.id ? "selected" : ""}`}
              onClick={() => handleSelectConversation(conv.id)}
            >
              {conv.title}
            </div>
          ))}
        </div>

        <div className="chat-main">
          <div className="chat-box">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`message ${msg.sender === "user" ? "user-message" : "ai-message"}`}
              >
                {msg.content}
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          <div className="input-container">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Écris un message..."
            />
            <button onClick={sendMessage}>Envoyer</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Chat;
