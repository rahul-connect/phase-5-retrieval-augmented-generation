from rag.chunking import split_by_words

text = "Python programming is fun"

chunks = split_by_words(text, chunk_size=15)

print(chunks)

long_word = "ABCDEFGHIJKL"

result = split_by_words(long_word, chunk_size=5)

print(result)