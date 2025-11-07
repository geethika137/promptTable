from fastapi import FastAPI
from app.api.v1.prompt_routes import router as prompt_router

app = FastAPI(title="Prompt API with MongoDB")

app.include_router(prompt_router)

@app.get("/")
def root():
    print("Prompt API is running successfully 🚀")
    return {"message": "Prompt API running successfully 🚀"}
