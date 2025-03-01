from sqlalchemy import Boolean, Column, ForeignKey, String, create_engine, inspect
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///blur_application.db")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True)
    subscription = Column(Boolean, default=False)
    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(String, primary_key=True)
    directory = Column(String, unique=True, nullable=False)
    user_email = Column(String, ForeignKey("users.email"), nullable=False)
    user = relationship("User", back_populates="orders", cascade="all")


def create_db():
    inspector = inspect(engine)
    if not inspector.has_table("users"):
        Base.metadata.create_all(bind=engine)
