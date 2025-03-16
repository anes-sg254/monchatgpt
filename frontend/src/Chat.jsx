import React, { useState } from "react";
import axios from "axios";
import "./app.css";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", content: input };
    setMessages([...messages, userMessage]);
    setInput("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/messages/chat", {
        conversation_id: 1,
        sender: "user",
        content: input,
      });

      const aiMessage = { sender: "ai", content: response.data.ai_response };
      setMessages([...messages, userMessage, aiMessage]);
    } catch (error) {
      console.error("Erreur lors de l'envoi du message :", error);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender === "user" ? "user-message" : "ai-message"}`}>
            {msg.content}
          </div>
        ))}
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
  );
}

export default Chat;
