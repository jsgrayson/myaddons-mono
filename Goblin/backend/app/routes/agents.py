from fastapi import APIRouter

router = APIRouter(prefix="/agents")

@router.get("/")
def agents():
    return {"agents": ["warden", "tsm_brain", "gmail_archiver", "bank_runner", "ah_runner"]}
