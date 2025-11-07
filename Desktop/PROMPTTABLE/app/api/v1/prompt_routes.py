from fastapi import APIRouter, Depends
from typing import List
from app.schemas.prompt_schema import PromptCreate, PromptUpdate, PromptResponse
from app.services.prompt_service import PromptService
from app.core.database import get_db

router = APIRouter(prefix="/prompts", tags=["Prompts"])

@router.post("/", response_model=PromptResponse)
async def create_prompt(prompt: PromptCreate, db=Depends(get_db)):
    service = PromptService(db)
    return await service.create_prompt(prompt)

@router.get("/", response_model=List[PromptResponse])
async def get_all_prompts(db=Depends(get_db)):
    service = PromptService(db)
    return await service.get_all_prompts()

@router.get("/{prompt_id}", response_model=PromptResponse)
async def get_prompt(prompt_id: str, db=Depends(get_db)):
    service = PromptService(db)
    return await service.get_prompt(prompt_id)

@router.put("/{prompt_id}", response_model=PromptResponse)
async def update_prompt(prompt_id: str, prompt: PromptUpdate, db=Depends(get_db)):
    service = PromptService(db)
    return await service.update_prompt(prompt_id, prompt)

@router.delete("/{prompt_id}")
async def delete_prompt(prompt_id: str, db=Depends(get_db)):
    service = PromptService(db)
    return await service.delete_prompt(prompt_id)
