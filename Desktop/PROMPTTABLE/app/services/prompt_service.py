from fastapi import HTTPException
from bson import ObjectId
from app.schemas.prompt_schema import PromptCreate, PromptUpdate

class PromptService:
    def __init__(self, db):
        self.collection = db.prompts

    async def create_prompt(self, prompt: PromptCreate):
        data = prompt.model_dump()
        result = await self.collection.insert_one(data)
        created = await self.collection.find_one({"_id": result.inserted_id})
        created["_id"] = str(created["_id"])
        return created

    async def get_prompt(self, prompt_id: str):
        if not ObjectId.is_valid(prompt_id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        prompt = await self.collection.find_one({"_id": ObjectId(prompt_id)})
        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")
        prompt["_id"] = str(prompt["_id"])
        return prompt

    async def get_all_prompts(self):
        prompts = []
        async for doc in self.collection.find():
            doc["_id"] = str(doc["_id"])
            prompts.append(doc)
        return prompts

    async def update_prompt(self, prompt_id: str, prompt: PromptUpdate):
        if not ObjectId.is_valid(prompt_id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        update_data = {k: v for k, v in prompt.model_dump().items() if v is not None}
        result = await self.collection.update_one(
            {"_id": ObjectId(prompt_id)}, {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Prompt not found or not modified")
        updated = await self.collection.find_one({"_id": ObjectId(prompt_id)})
        updated["_id"] = str(updated["_id"])
        return updated

    async def delete_prompt(self, prompt_id: str):
        if not ObjectId.is_valid(prompt_id):
            raise HTTPException(status_code=400, detail="Invalid ObjectId format")
        result = await self.collection.delete_one({"_id": ObjectId(prompt_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Prompt not found")
        return {"message": "Prompt deleted successfully"}
