from backend.database import Base, engine

# Load all SQLAlchemy models
import backend.models


def create_tables():
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()