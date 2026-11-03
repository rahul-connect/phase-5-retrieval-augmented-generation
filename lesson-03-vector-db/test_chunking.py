from rag.chunking import chunk_recursive

text = "Python programming is fun"

chunks = chunk_recursive(text, chunk_size=15)

print(chunks)