import os
from fastapi import FastAPI
from router import routes

app = FastAPI()

app.include_router(routes.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Neurobagel Query Tool AI API"}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))

    uvicorn.run(app, host=host, port=port)
