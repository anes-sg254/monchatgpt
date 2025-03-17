# MonChatGPT 🫠
Créez votre propre clone de ChatGPT avec historique des conversations, frontend réactif et backend connecté à un modèle HuggingFace.

## 🌐 Technologies Utilisées
- **Frontend** : React Vite, CSS pur
- **Backend** : FastAPI (Python), PostgreSQL
- **IA** : Modèle via HuggingFace API (ex: Mistral.)

---

# 🚀 Lancer le projet

## 💻 Backend (FastAPI + PostgreSQL)

### 1. Cloner le repo
```bash
git clone <votre-lien-repo>
cd monchatgpt2
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Configurer la base PostgreSQL
- Créer une base de données `chatgpt`
- Importer le fichier `schema.sql`

### 4. Créer un fichier `.env`
```env
HF_TOKEN=hf_votre_token_huggingface
DB_HOST=localhost
DB_NAME=chatgpt
DB_USER=postgres
DB_PASSWORD=motdepasse
DB_PORT=5432
```

### 5. Lancer le serveur backend
```bash
uvicorn main:app --reload --port 5000
```
Accéder à la doc API : [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs)

---

## 🛠 Frontend (React Vite)

### 1. Accéder au dossier frontend
```bash
cd frontend
```

### 2. Installer les dépendances
```bash
npm install
```

### 3. Lancer le serveur React
```bash
npm run dev
```

L'application est accessible sur [http://localhost:5173](http://localhost:5173)

---

# 🎓 Fonctionnalités
- Envoi de message utilisateur et réponse IA
- Historique des conversations (chargé depuis la base)
- Stockage en base PostgreSQL de chaque échange
- Interface réactive et responsive avec design sombre/bleu





