import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

import backend.ingest as ingest
import backend.retrieval as retrieval
from backend.config import DEFAULT_SAMPLE_PDF
import faiss

chunks, pages = ingest.extract_chunks_from_pdf(str(DEFAULT_SAMPLE_PDF))
print(f"Extracted {len(chunks)} chunks from {pages} pages.")

model = retrieval.get_retrieval_model()
texts = [c["text"] for c in chunks]
embeddings = retrieval.encode_passages(texts, model)

dim = embeddings.shape[1]
index = faiss.IndexFlatIP(dim)
index.add(embeddings)

in_chapter = [
    "What is photosynthesis and what is its chemical equation?",
    "Which steps are involved in photosynthesis?",
    "How do guard cells open and close the stomatal pore?",
    "How do desert plants adapt to minimize water loss?",
    "What is the function of nitrogen absorbed by plants from soil?",
    "What are the three types of heterotrophic nutrition?",
    "What is the role of hydrochloric acid and pepsin in the stomach?",
    "What do bile juice and pancreatic enzymes do in the small intestine?",
    "What happens during aerobic respiration in the mitochondria?",
    "Why does lactic acid accumulate in human muscle cells during exercise?"
]

off_topic = [
    "What is Newton's third law of motion?",
    "Who was the first President of the United States?",
    "How do you calculate compound interest in banking?",
    "What are the rules of playing cricket?",
    "Can you write a Python function to sort a binary search tree?"
]

print("\n=== IN-CHAPTER QUESTIONS (Top-1 Cosine Scores) ===")
in_scores = []
for q in in_chapter:
    res, top_s = retrieval.search_similar_chunks(q, chunks, index, model, k=3)
    in_scores.append(top_s)
    print(f"Score: {top_s:.4f} | [Page {res[0]['page']}] | Q: {q}")

print("\n=== OFF-TOPIC QUESTIONS (Top-1 Cosine Scores) ===")
off_scores = []
for q in off_topic:
    res, top_s = retrieval.search_similar_chunks(q, chunks, index, model, k=3)
    off_scores.append(top_s)
    print(f"Score: {top_s:.4f} | [Page {res[0]['page']}] | Q: {q}")

print(f"\nIn-chapter range: min={min(in_scores):.4f}, avg={sum(in_scores)/len(in_scores):.4f}, max={max(in_scores):.4f}")
print(f"Off-topic range:  min={min(off_scores):.4f}, avg={sum(off_scores)/len(off_scores):.4f}, max={max(off_scores):.4f}")
margin = min(in_scores) - max(off_scores)
print(f"Separation margin: {margin:.4f}")
recommended = round((min(in_scores) + max(off_scores)) / 2, 2)
print(f"Recommended SIM_THRESHOLD: {recommended}")
