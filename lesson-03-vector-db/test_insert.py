
"""Practice inserting a document with SQLAlchemy."""

from rag.database import SessionLocal
from rag.models import Document


def main():
    """Insert one document into PostgreSQL."""

    with SessionLocal() as db:
        document = Document(
            title="My First RAG Document",
            content="Python is a programming language used for AI.",
            source="manual-test",
        )

        db.add(document)
        db.commit()

        print(f"Inserted document ID: {document.id}")
        print(f"Document title: {document.title}")


if __name__ == "__main__":
    main()
