from fastapi import FastAPI
from routes import users, conversations, messages
import inspect

app = FastAPI()

# Inclusion des routes
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(conversations.router, prefix="/conversations", tags=["Conversations"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API ChatGPT"}

print("🔍 Routes enregistrées :")
for route in app.routes:
    if hasattr(route, "path"):
        print(f"{route.methods} ➜ {route.path}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000, reload=True)