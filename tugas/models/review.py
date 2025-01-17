from models.base import Base
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column


class Review(Base):
    __tablename__ = 'reviews'

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    description = mapped_column(Text)
    email = mapped_column(String(30), nullable= False)
    rating = mapped_column(Integer, nullable=True)
   
