
"""Practice retrieving documents through the repository."""

from rag.database import SessionLocal
from rag.repository import get_all_documents, get_document_by_id


def main() -> None:
    """Read stored documents using a database session."""

    with SessionLocal() as db:
        documents = get_all_documents(db)

        print("All documents:")

        for document in documents:
            print(f"{document.id}: {document.title}")

        print()

        document = get_document_by_id(db, document_id=1)

        if document is None:
            print("Document not found.")
        else:
            print(f"Found document: {document.title}")


if __name__ == "__main__":
    main()
