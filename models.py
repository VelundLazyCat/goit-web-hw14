from sqlalchemy import String, Date, ForeignKey, func, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), index=True)
    email: Mapped[str] = mapped_column(
        String(50), index=True, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    # created_at: Mapped[Date] = mapped_column(Date, default=func.now())
    avatar: Mapped[str] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    confirmed: Mapped[str] = mapped_column(Boolean, default=False)


class Contact(Base):
    __tablename__ = 'contacts'
    contact_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(20), index=True)
    last_name: Mapped[str] = mapped_column(String(20), index=True)
    email: Mapped[str] = mapped_column(String(50), index=True, unique=True)
    telephon_number: Mapped[str] = mapped_column(String(15), unique=True)
    birthday: Mapped[Date] = mapped_column(Date, nullable=False)
    description: Mapped[str] = mapped_column(String(250))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    user: Mapped["User"] = relationship(
        'User', backref="contacts", lazy="joined")
