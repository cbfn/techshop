from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict[str, str]:
    """Retorna o status de saúde da API."""
    return {"status": "ok"}
