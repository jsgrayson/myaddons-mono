from fastapi import APIRouter

router = APIRouter(prefix="/tasks")

@router.get("/list")
def list_tasks():
    return {"tasks": []}
