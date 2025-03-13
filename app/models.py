from app import Mapped, mapped_column, db, bcrypt, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first: Mapped[str] = mapped_column(nullable=False)
    last: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)  # Use password_hash instead of password
    is_blocked: Mapped[bool] = mapped_column(default=False)

    # Relationship with transactions
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, first, last, email, password):
        self.first = first
        self.last = last
        self.email = email
        self.set_password(password)  # Use set_password to hash the password

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class ImageData(db.Model):
    __tablename__ = "image_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)

    def get_image_url(self):
        return f"{self.filename}"  # URL to serve the image


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    av_qty: Mapped[int] = mapped_column(nullable=False)
    exp_date: Mapped[datetime] = mapped_column(nullable=True)  # Expiry date should store datetime, not int
    description: Mapped[str] = mapped_column(nullable=True)
    image_id: Mapped[int] = mapped_column(ForeignKey("image_data.id"), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    def get_image_url(self):
        image = ImageData.query.get(self.image_id) if self.image_id else None
        return image.get_image_url() if image else None


class Transaction(db.Model):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    items: Mapped[dict] = mapped_column(db.JSON, nullable=False)  # Store cart items as JSON
    total_amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(default="Pending")
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationship with User model
    user = relationship("User", back_populates="transactions")
