from sqlalchemy import Column, String, Integer, Text, ForeignKey, Float, TIMESTAMP, text
from sqlalchemy.orm import relationship
from api.database import Base
from enum import Enum as PyEnum
from sqlalchemy import Enum

class Genre(PyEnum):
    ACTION = "Action"
    COMEDY = "Comedy"
    DRAMA = "Drama"
    HORROR = "Horror"
    ROMANCE = "Romance"
    SCIENCE_FICTION = "Science Fiction"
    FANTASY = "Fantasy"
    THRILLER = "Thriller"
    DOCUMENTARY = "Documentary"
    ANIMATION = "Animation"
    ADVENTURE = "Adventure"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    google_id = Column(String, unique=True, nullable=True)  # Google's user ID
    avatar_url = Column(String, nullable=True)  # Profile picture from Google
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

class Movie(Base):
    __tablename__ = "movies"

    id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    director = Column(String)
    genre = Column(Enum(Genre))
    release_year = Column(Integer)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    reviews = relationship("Review", back_populates="movie")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    movie_id = Column(String, ForeignKey("movies.id"), nullable=False)
    rating = Column(Float, nullable=False)
    review_text = Column(Text)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user = relationship("User")
    movie = relationship("Movie", back_populates="reviews")