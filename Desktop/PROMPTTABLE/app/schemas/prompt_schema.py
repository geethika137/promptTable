from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, BeforeValidator
from bson import ObjectId
from typing_extensions import Annotated


# ✅ Proper Mongo ObjectId handler using Annotated + BeforeValidator
def validate_object_id(v: Any) -> str:
    """Convert ObjectId to string, validate if not already."""
    if isinstance(v, ObjectId):
        return str(v)
    if not ObjectId.is_valid(v):
        raise ValueError("Invalid ObjectId")
    return str(v)


# ✅ Annotated type that FastAPI + Pydantic can serialize and document safely
PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]


# ✅ Base schema
class PromptBase(BaseModel):
    Type: Optional[str] = None
    Name: Optional[str] = None
    IconPath: Optional[str] = None
    Tech: Optional[str] = None
    AiRole: Optional[str] = None
    SystemRole: Optional[str] = None
    Objective: Optional[str] = None
    TaskInstructions: Optional[str] = None
    TaskInput: Optional[str] = None
    TaskOutputFormat: Optional[str] = None
    TaskExample: Optional[str] = None
    LLM: Optional[str] = None
    SettingsJson: Optional[Dict[str, Any]] = None
    CreatedBy: Optional[str] = None


# ✅ For creating a new prompt
class PromptCreate(PromptBase):
    pass


# ✅ For updating an existing prompt
class PromptUpdate(PromptBase):
    UpdatedDateTime: Optional[datetime] = Field(default_factory=datetime.utcnow)


# ✅ For MongoDB documents returned in responses
class PromptResponse(PromptBase):
    id: Optional[PyObjectId] = Field(alias="_id")
    CreateDateTime: datetime = Field(default_factory=datetime.utcnow)
    UpdatedDateTime: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
