# Backward-compatible import. Use app.db.database.Base everywhere.
from app.db.database import Base

__all__ = ["Base"]
