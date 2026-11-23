
from app.core.database import Base
from sqlalchemy.orm import  Mapped, mapped_column
from sqlalchemy.sql.sqltypes import String

class SchoolModel(Base):
    
    __tablename__ = "schools"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=True)
        