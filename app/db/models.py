from sqlalchemy import Column, String, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum
import uuid
from app.db.database import Base


class RecipeStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(255), index=True, nullable=False)
    cooking_time = Column(String(50), nullable=True)
    required_tools = Column(JSON, nullable=True)
    ingredients = Column(JSON, nullable=False)
    steps = Column(JSON, nullable=True)
    nutrition = Column(JSON, nullable=True)
    status = Column(Enum(RecipeStatus), default=RecipeStatus.ACTIVE, nullable=False)

