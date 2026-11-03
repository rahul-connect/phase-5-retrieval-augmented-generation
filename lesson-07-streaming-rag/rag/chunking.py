"""Utilities for splitting documents into text chunks."""

import re

def split_by_characters(text: str, chunk_size: int) -> list[str]:
    """Split text into pieces of at most chunk_size characters."""
    pieces: list[str] = []

    for i in range(0, len(text), chunk_size):
        piece = text[i:i + chunk_size]
        pieces.append(piece)

    return pieces


def split_by_words(text: str, chunk_size: int) -> list[str]:
    """Split text into chunks while preserving word boundaries."""
    words = text.split()

    chunks: list[str] = []
    current_chunk = ""

    for word in words:
        # Handle a word that exceeds the maximum chunk size.
        if len(word) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            pieces = split_by_characters(word, chunk_size)
            chunks.extend(pieces)
            continue

        # Start a new chunk if our accumulator is empty.
        if not current_chunk:
            current_chunk = word
            continue

        # Try adding the next word to the current chunk.
        combined = current_chunk + " " + word

        if len(combined) <= chunk_size:
            current_chunk = combined
        else:
            chunks.append(current_chunk)
            current_chunk = word

    # Save the final unfinished chunk.
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def split_by_sentences(text: str, chunk_size: int) -> list[str]:
    """Split text into chunks while preserving sentence boundaries."""
    sentences = re.split(r"(?<=\.) ", text)

    chunks: list[str] = []
    current_chunk = ""

    for sentence in sentences:
        # If a sentence is too large, split it by words.
        if len(sentence) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            pieces = split_by_words(sentence, chunk_size)
            chunks.extend(pieces)
            continue

        # Start a new chunk.
        if not current_chunk:
            current_chunk = sentence
            continue

        # Try combining two sentences.
        combined = current_chunk + " " + sentence

        if len(combined) <= chunk_size:
            current_chunk = combined
        else:
            chunks.append(current_chunk)
            current_chunk = sentence

    # Save the final chunk.
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def chunk_recursive(
    text: str,
    chunk_size: int = 500,
) -> list[str]:
    """Split text into chunks while preserving natural boundaries."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if not text.strip():
        return []

    if len(text) <= chunk_size:
        return [text]

    paragraphs = text.split("\n\n")

    chunks: list[str] = []
    current_chunk = ""

    for paragraph in paragraphs:

        if len(paragraph) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = ""

            pieces = split_by_sentences(paragraph, chunk_size)
            chunks.extend(pieces)
            continue
        
        if not current_chunk:
            current_chunk = paragraph
            continue

        combined = current_chunk + "\n\n" + paragraph

        if len(combined) <= chunk_size:
            current_chunk = combined
        else:
            chunks.append(current_chunk)
            current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks