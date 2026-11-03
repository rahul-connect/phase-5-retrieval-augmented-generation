from rag.chunking import split_by_sentences

text = "Python is useful. FastAPI is fast. PostgreSQL stores data."

chunks = split_by_sentences(text, chunk_size=35)

for chunk in chunks:
    print(repr(chunk), len(chunk))