from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API rodando com sucesso!"}

@app.get("/status")
def status():
    return {"status": "Ok", "versão": "1.0.0"}