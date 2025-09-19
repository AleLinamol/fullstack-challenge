from fastapi import FastAPI

app = FastAPI()
@app.post("/rpc")
async def rpc_endpoint():
    return {"message": "Servidor funcionando"}