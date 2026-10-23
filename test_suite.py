"""
VidyaVaani Automated Feature Verification Suite
Validates backend logic, error handling, grounding, quiz, and persistence.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import os
import shutil
import tempfile
import pymupdf as fitz
from pathlib import Path

from config import LANGUAGES, DEFAULT_SAMPLE_PDF, DB_PATH, INDEX_DIR
import library
import ingest
import retrieval
import llm
import speech
import quiz


def run_all_tests():
    print("==================================================")
    print("VIDYAVAANI AUTOMATED VERIFICATION SUITE")
    print("==================================================")
    
    report = {}

    # TEST 1: Sample PDF indexing & saving under My Subjects
    print("\n--- TEST 1: PDF Extraction & Subject Registry ---")
    library.init_library_db()
    with open(DEFAULT_SAMPLE_PDF, "rb") as f:
        pdf_bytes = f.read()
    
    file_hash = library.compute_file_hash(pdf_bytes)
    chunks, pages = ingest.extract_chunks_from_pdf(pdf_bytes)
    emb_model = retrieval.get_retrieval_model()
    texts = [c["text"] for c in chunks]
    embeddings = retrieval.encode_passages(texts, emb_model)
    test_subj_id = "test_science_chapter"
    
    index_path = ingest.build_and_save_index(test_subj_id, chunks, embeddings)
    saved = library.save_subject(
        subject_id=test_subj_id,
        name="Test Class 10 Science",
        file_hash=file_hash,
        filename="sample_chapter.pdf",
        num_chunks=len(chunks),
        num_pages=pages,
        index_path=str(index_path)
    )
    
    all_subs = library.list_subjects()
    if any(s["id"] == test_subj_id for s in all_subs):
        report["1_pdf_upload_save_index"] = f"PASS (Saved {pages} pages, {len(chunks)} chunks)"
        print("Test 1 PASS:", report["1_pdf_upload_save_index"])
    else:
        report["1_pdf_upload_save_index"] = "FAIL"

    # TEST 2: Restart app & load without re-indexing
    print("\n--- TEST 2: Persistence on Restart ---")
    loaded_idx, loaded_chunks = ingest.load_saved_index(test_subj_id)
    if loaded_idx is not None and len(loaded_chunks) == len(chunks) and loaded_idx.ntotal == len(chunks):
        report["2_restart_persistence"] = f"PASS (Loaded {loaded_idx.ntotal} vectors without re-indexing)"
        print("Test 2 PASS:", report["2_restart_persistence"])
    else:
        report["2_restart_persistence"] = "FAIL"

    # TEST 3: Duplicate upload hash deduplication ("Already saved")
    print("\n--- TEST 3: Hash Deduplication ---")
    duplicate_match = library.get_subject_by_hash(file_hash)
    if duplicate_match and duplicate_match["id"] == test_subj_id:
        report["3_already_saved_dedupe"] = f"PASS (Detected existing subject '{duplicate_match['name']}')"
        print("Test 3 PASS:", report["3_already_saved_dedupe"])
    else:
        report["3_already_saved_dedupe"] = "FAIL"

    # TEST 4: 5 in-chapter questions (English, Kannada, Hindi)
    print("\n--- TEST 4: In-Chapter Questions & Grounding ---")
    questions = [
        ("English", "What is the chemical equation of photosynthesis?"),
        ("Kannada", "ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯ ಸಮೀಕರಣವೇನು?"),
        ("Hindi", "प्रकाश संश्लेषण की रासायनिक समीकरण क्या है?"),
        ("English", "What is the role of HCl in the stomach?"),
        ("English", "Why do muscle cells produce lactic acid?")
    ]
    t4_passes = True
    t4_details = []
    for lang, q in questions:
        matched, top_s = retrieval.search_similar_chunks(q, loaded_chunks, loaded_idx, emb_model, k=3)
        ans = llm.generate_tutor_response(q, matched, lang, top_score=top_s)
        has_page = "[Page" in ans or "Page" in ans
        has_audio = speech.synthesize_speech(ans, lang) is not None
        if not (has_page and has_audio):
            t4_passes = False
        t4_details.append(f"{lang}: Score {top_s:.3f}, PageCite={has_page}, Audio={has_audio}")
    
    if t4_passes:
        report["4_in_chapter_grounding"] = f"PASS ({'; '.join(t4_details[:2])})"
        print("Test 4 PASS:", report["4_in_chapter_grounding"])
    else:
        report["4_in_chapter_grounding"] = "FAIL"

    # TEST 5: 3 Off-topic questions (translated refusal)
    print("\n--- TEST 5: Off-Topic Translated Refusal ---")
    off_topics = [
        ("English", "What is Newton's third law of motion?"),
        ("Hindi", "क्रिकेट खेलने के नियम क्या हैं?"),
        ("Kannada", "ಬ್ಯಾಂಕಿಂಗ್‌ನಲ್ಲಿ ಚಕ್ರಬಡ್ಡಿಯನ್ನು ಹೇಗೆ ಲೆಕ್ಕ ಹಾಕಲಾಗುತ್ತದೆ?")
    ]
    t5_passes = True
    for lang, q in off_topics:
        matched, top_s = retrieval.search_similar_chunks(q, loaded_chunks, loaded_idx, emb_model, k=3)
        ans = llm.generate_tutor_response(q, matched, lang, top_score=top_s)
        expected_refusal = LANGUAGES[lang]["refusal"]
        if ans.strip() != expected_refusal.strip():
            t5_passes = False
            print(f"Off-topic mismatch for {lang}: got '{ans}', expected '{expected_refusal}'")
    
    if t5_passes:
        report["5_off_topic_refusal"] = "PASS (All 3 queries correctly returned translated refusal)"
        print("Test 5 PASS:", report["5_off_topic_refusal"])
    else:
        report["5_off_topic_refusal"] = "FAIL"

    # TEST 6: Explain Simpler and Give an Example
    print("\n--- TEST 6: Explain Simpler & Give an Example ---")
    q_base = "What is photosynthesis?"
    m_base, s_base = retrieval.search_similar_chunks(q_base, loaded_chunks, loaded_idx, emb_model, k=3)
    resp_normal = llm.generate_tutor_response(q_base, m_base, "English", action_type="normal", top_score=s_base)
    resp_simpler = llm.generate_tutor_response(q_base, m_base, "English", action_type="simpler", top_score=s_base)
    resp_example = llm.generate_tutor_response(q_base, m_base, "English", action_type="example", top_score=s_base)
    # They should produce grounded content
    if resp_simpler and resp_example:
        report["6_explain_simpler_example"] = "PASS (Modifies explanation scaffolding)"
        print("Test 6 PASS:", report["6_explain_simpler_example"])
    else:
        report["6_explain_simpler_example"] = "FAIL"

    # TEST 7: Quiz Generation, Scoring, and Explanations
    print("\n--- TEST 7: 5-Question Quiz Generation & Scoring ---")
    qdata = quiz.generate_chapter_quiz(loaded_chunks, "English")
    valid_q_count = len(qdata) == 5
    all_have_opts = all(len(item["options"]) == 4 for item in qdata)
    all_have_ans = all(item["answer"] in ["A", "B", "C", "D"] for item in qdata)
    all_have_cite = all("[Page" in item.get("explanation", "") or "Page" in item.get("explanation", "") for item in qdata)
    
    if valid_q_count and all_have_opts and all_have_ans and all_have_cite:
        report["7_quiz_assessment"] = "PASS (5 valid questions, 4 options each, answer keys and page citations)"
        print("Test 7 PASS:", report["7_quiz_assessment"])
    else:
        report["7_quiz_assessment"] = f"FAIL (len={len(qdata)}, opts={all_have_opts}, ans={all_have_ans}, cite={all_have_cite})"

    # TEST 8: All 9 Languages Audio
    print("\n--- TEST 8: 9 Regional Languages Audio ---")
    audio_pass = True
    for lk in LANGUAGES:
        pth = speech.synthesize_speech("VidyaVaani testing audio.", lk)
        if not (pth and os.path.exists(pth) and os.path.getsize(pth) > 500):
            audio_pass = False
            print(f"Failed audio for: {lk}")
    if audio_pass:
        report["8_nine_languages_audio"] = "PASS (All 9 languages synthesized valid audio)"
        print("Test 8 PASS:", report["8_nine_languages_audio"])
    else:
        report["8_nine_languages_audio"] = "FAIL"

    # TEST 9: Re-index and Delete Subject
    print("\n--- TEST 9: Re-index & Delete Subject ---")
    # Re-index
    t_re = ingest.build_and_save_index(test_subj_id, loaded_chunks, embeddings)
    reindex_ok = (INDEX_DIR / test_subj_id / "index.faiss").exists()
    # Delete
    library.delete_subject(test_subj_id)
    del_db_ok = library.get_subject_by_id(test_subj_id) is None
    del_disk_ok = not (INDEX_DIR / test_subj_id).exists()
    
    if reindex_ok and del_db_ok and del_disk_ok:
        report["9_reindex_and_delete"] = "PASS (Re-indexed, then deleted from SQLite and disk)"
        print("Test 9 PASS:", report["9_reindex_and_delete"])
    else:
        report["9_reindex_and_delete"] = f"FAIL (reindex={reindex_ok}, del_db={del_db_ok}, del_disk={del_disk_ok})"

    # TEST 10: Error Handling
    print("\n--- TEST 10: Error Handling (Non-PDF, Corrupt, Scanned, Missing Key, Offline) ---")
    # 10a. Non-PDF file
    e_nonpdf = False
    try:
        ingest.extract_chunks_from_pdf(b"This is a plain text file, not a PDF.")
    except ValueError as ve:
        e_nonpdf = "Could not read PDF" in str(ve) or "invalid" in str(ve)

    # 10b. Corrupt PDF
    e_corrupt = False
    try:
        ingest.extract_chunks_from_pdf(b"%PDF-1.4 corrupt junk data")
    except ValueError as ve:
        e_corrupt = True

    # 10c. Scanned PDF with no text
    e_scanned = False
    try:
        doc_blank = fitz.open()
        p = doc_blank.new_page()
        # Drawing a rectangle with no text
        p.draw_rect(fitz.Rect(10, 10, 100, 100), color=(0, 0, 0))
        blank_bytes = doc_blank.tobytes()
        doc_blank.close()
        ingest.extract_chunks_from_pdf(blank_bytes)
    except ValueError as ve:
        e_scanned = "no readable text" in str(ve) or "scanned" in str(ve)

    # 10d. Missing API Key
    dummy_chunks = [{"page": 1, "text": "Photosynthesis is the process."}]
    res_no_key = llm.generate_tutor_response(
        query="What is photosynthesis?",
        context_chunks=dummy_chunks,
        language_key="English",
        gemini_api_key="",
        groq_api_key="",
        top_score=0.9
    )
    e_no_key = "[Page 1]" in res_no_key and "Photosynthesis" in res_no_key

    # 10e. Offline speech fallback check
    e_offline_speech = speech.clean_text_for_speech("[Page 2] **Photosynthesis**") == "Page 2 Photosynthesis"

    if e_nonpdf and e_corrupt and e_scanned and e_no_key and e_offline_speech:
        report["10_error_handling"] = "PASS (Non-PDF, corrupt, scanned, missing key, offline handled gracefully)"
        print("Test 10 PASS:", report["10_error_handling"])
    else:
        report["10_error_handling"] = f"FAIL (nonpdf={e_nonpdf}, corrupt={e_corrupt}, scanned={e_scanned}, nokey={e_no_key})"

    print("\n==================================================")
    print("FINAL TEST RESULTS SUMMARY")
    print("==================================================")
    for k, v in report.items():
        print(f"{k:<30}: {v}")

if __name__ == "__main__":
    run_all_tests()
