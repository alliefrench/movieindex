from enum import Enum as PyEnum

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    text,
)
from sqlalchemy.orm import relationship

# Import with absolute paths (working directory is project root for both local and Vercel)
from api.database import Base


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


class PermissionType(PyEnum):
    VIEW_CONTENT = "view_content"
    WRITE_REVIEWS = "write_reviews"
    ADD_MOVIES = "add_movies"
    EDIT_MOVIES = "edit_movies"
    DELETE_MOVIES = "delete_movies"
    MANAGE_USERS = "manage_users"


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

    # Relationship to permissions - TEMPORARILY COMMENTED OUT
    # permissions = relationship("UserPermission", back_populates="user")


# Temporarily commented out to prevent interference with OAuth flow
# class Permission(Base):
#     __tablename__ = "permissions"
#
#     id = Column(String, primary_key=True, nullable=False)
#     name = Column(Enum(PermissionType), nullable=False, unique=True)
#     description = Column(String, nullable=False)
#     created_at = Column(
#         TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
#     )
#
#     # Relationship to users who have this permission
#     users = relationship("UserPermission", back_populates="permission")

# class UserPermission(Base):
#     __tablename__ = "user_permissions"
#
#     id = Column(String, primary_key=True, nullable=False)
#     user_id = Column(String, ForeignKey("users.id"), nullable=False)
#     permission_id = Column(String, ForeignKey("permissions.id"), nullable=False)
#     granted_by = Column(String, ForeignKey("users.id"), nullable=True)  # Who granted this permission
#     created_at = Column(
#         TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
#     )
#
#     # Relationships - removed back_populates since User.permissions is commented out
#     user = relationship("User", foreign_keys=[user_id])
#     permission = relationship("Permission", back_populates="users")
#     granted_by_user = relationship("User", foreign_keys=[granted_by])


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
