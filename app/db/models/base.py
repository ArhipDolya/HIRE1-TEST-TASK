from datetime import datetime

from sqlalchemy import MetaData, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column


metadata = MetaData()

Base = declarative_base(metadata=metadata)


class TimedBaseModel(Base):
    """An abstract base model that adds created_at and updated_at timestamp fields to the model"""

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now(), nullable=False)
