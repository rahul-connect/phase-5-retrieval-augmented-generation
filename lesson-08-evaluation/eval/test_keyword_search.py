from rag.database import SessionLocal
from rag.better_search import keyword_search
from sqlalchemy import func, select

from rag.models import Chunk, Document

query = "Compare REST and GraphQL"

with SessionLocal() as db:
    rows = keyword_search(
        db=db,
        query=query,
        top_k=20,
    )

print("Keyword matches:", len(rows))

for chunk, title, score in rows:
    print(f"{title} (rank={score:.3f})")



with SessionLocal() as db:
    tsquery = func.to_tsquery("english", "rest | graphql")

    stmt = (
        select(Chunk, Document.title)
        .join(Chunk.document)
        .where(Chunk.content_tsv.op("@@")(tsquery))
        .limit(20)
    )

    rows = db.execute(stmt).all()

print("\nOR keyword matches:", len(rows))

for chunk, title in rows:
    print(title)