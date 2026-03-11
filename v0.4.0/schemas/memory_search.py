#!/usr/bin/env python3
"""
TaskPilot Memory Search v0.4.0

[P5] BM25-style keyword search over training_log.jsonl and run_events.jsonl.
Enables queries like "what did we learn about protocol extraction" across cycles.

No external dependencies — pure Python implementation using TF-IDF-like scoring.
"""

import json
import math
import re
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Common English stopwords
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
    "in", "is", "it", "its", "of", "on", "or", "that", "the", "to", "was", "were",
    "will", "with", "this", "but", "not", "have", "had", "do", "does", "did", "can",
    "could", "should", "would", "may", "might", "shall", "must",
}

# BM25 parameters
K1 = 1.5
B = 0.75


@dataclass
class SearchResult:
    """A single search result with relevance score."""
    document_id: str
    source_file: str
    score: float
    snippet: str
    metadata: Dict = field(default_factory=dict)


@dataclass
class SearchIndex:
    """In-memory search index over JSONL documents."""
    documents: List[Dict] = field(default_factory=list)
    doc_count: int = 0
    avg_doc_length: float = 0.0
    idf_cache: Dict[str, float] = field(default_factory=dict)
    doc_term_freqs: List[Counter] = field(default_factory=list)
    doc_lengths: List[int] = field(default_factory=list)


def tokenize(text: str) -> List[str]:
    """Tokenize text into lowercase words, removing stopwords."""
    words = re.findall(r'[a-z0-9_]+', text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def build_index(documents: List[Dict], text_fields: List[str]) -> SearchIndex:
    """Build a BM25 search index from a list of documents."""
    index = SearchIndex()
    index.documents = documents
    index.doc_count = len(documents)

    # Compute term frequencies and document lengths
    all_term_counts = Counter()

    for doc in documents:
        text = " ".join(str(doc.get(f, "")) for f in text_fields if doc.get(f))
        tokens = tokenize(text)
        tf = Counter(tokens)
        index.doc_term_freqs.append(tf)
        index.doc_lengths.append(len(tokens))

        # Count documents containing each term
        for term in set(tokens):
            all_term_counts[term] += 1

    # Compute average document length
    total_length = sum(index.doc_lengths)
    index.avg_doc_length = total_length / index.doc_count if index.doc_count > 0 else 1.0

    # Compute IDF for each term
    for term, doc_freq in all_term_counts.items():
        idf = math.log((index.doc_count - doc_freq + 0.5) / (doc_freq + 0.5) + 1.0)
        index.idf_cache[term] = idf

    logger.info(f"Built index: {index.doc_count} documents, {len(index.idf_cache)} terms")
    return index


def search(index: SearchIndex, query: str, max_results: int = 10) -> List[Tuple[int, float]]:
    """Search the index with a BM25 query. Returns (doc_index, score) pairs."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    scores = []
    for doc_idx in range(index.doc_count):
        score = 0.0
        tf = index.doc_term_freqs[doc_idx]
        doc_len = index.doc_lengths[doc_idx]

        for term in query_tokens:
            if term not in index.idf_cache:
                continue

            idf = index.idf_cache[term]
            term_freq = tf.get(term, 0)

            # BM25 scoring
            numerator = term_freq * (K1 + 1)
            denominator = term_freq + K1 * (1 - B + B * (doc_len / index.avg_doc_length))
            score += idf * (numerator / denominator) if denominator > 0 else 0.0

        if score > 0:
            scores.append((doc_idx, score))

    # Sort by score descending
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:max_results]


class MemorySearch:
    """Search over TaskPilot memory files (JSONL format)."""

    def __init__(self, memory_paths: List[Path], text_fields: Optional[List[str]] = None):
        self.memory_paths = memory_paths
        self.text_fields = text_fields or ["rationale", "notes", "detail", "description",
                                            "type", "target", "suggested_by"]
        self.all_documents: List[Dict] = []
        self.doc_sources: List[str] = []
        self.index: Optional[SearchIndex] = None
        self._load_all()

    def _load_all(self):
        """Load all JSONL files into memory."""
        for path in self.memory_paths:
            if not path.exists():
                logger.warning(f"Memory file not found: {path}")
                continue

            with open(path, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        doc = json.loads(line)
                        self.all_documents.append(doc)
                        self.doc_sources.append(str(path))
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON at {path}:{line_num}")

        logger.info(f"Loaded {len(self.all_documents)} documents from {len(self.memory_paths)} files")

        if self.all_documents:
            self.index = build_index(self.all_documents, self.text_fields)

    def query(self, query_text: str, max_results: int = 10) -> List[SearchResult]:
        """Search memory for relevant documents."""
        if not self.index or not self.all_documents:
            return []

        results = search(self.index, query_text, max_results)

        search_results = []
        for doc_idx, score in results:
            doc = self.all_documents[doc_idx]
            source = self.doc_sources[doc_idx]

            # Build snippet from text fields
            snippet_parts = []
            for f in self.text_fields:
                val = doc.get(f)
                if val and isinstance(val, str):
                    snippet_parts.append(f"{f}: {val[:100]}")
            snippet = " | ".join(snippet_parts[:3])

            search_results.append(SearchResult(
                document_id=doc.get("id", f"doc_{doc_idx}"),
                source_file=source,
                score=score,
                snippet=snippet,
                metadata={
                    "timestamp": doc.get("timestamp", ""),
                    "type": doc.get("type", ""),
                    "version": doc.get("version", ""),
                }
            ))

        return search_results


def main():
    """Main entry point — demo search."""
    base_dir = Path(__file__).parent.parent.parent  # repo root
    memory_paths = [
        base_dir / "v0.1.0" / "training_log.jsonl",
    ]

    searcher = MemorySearch(memory_paths)

    queries = [
        "protocol extraction testability",
        "key rotation crypto security",
        "exit criteria binary validation",
        "MAST failure mode coverage",
    ]

    for q in queries:
        print(f"\n=== Search: '{q}' ===")
        results = searcher.query(q, max_results=3)
        if not results:
            print("  No results found")
        for r in results:
            print(f"  [{r.score:.3f}] {r.document_id} — {r.snippet[:120]}...")


if __name__ == "__main__":
    main()
