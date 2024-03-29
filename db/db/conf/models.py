"""Модели данных в db_conf."""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""


class Entity(Base):
    """Сущность (Entity) для хранения в timeseries database."""

    __tablename__: str = "entity"
    # PK
    entity_id: Mapped[int] = mapped_column(primary_key=True)
    # FK
