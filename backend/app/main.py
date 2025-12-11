from fastapi import FastAPI
from .routes import root, status, agents, ml, tasks

app = FastAPI(title="Goblin Backend API", version="0.1.0")

app.include_router(root.router)
app.include_router(status.router)
app.include_router(agents.router)
app.include_router(ml.router)
app.include_router(tasks.router)

