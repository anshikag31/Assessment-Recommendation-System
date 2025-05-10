import os
import re
import json
import torch
from transformers import BertTokenizer, BertModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define important skill and keyword groups
SKILLS = {"java", "c", "c++", "python", "javascript", "html", "css", "sql", "ms", "selenium", "core_java", "mfs", "360", "automation", "test cases"}
ROLES = {"developer", "content writer", "quality assurance", "software", "engineer", "core_java", "ms", "analyst", "mfs", "360", "tester", "business", "sales", "market"}
SOFT_SKILLS = {"communication", "collaborate", "team", "interpersonal", "reasoning", "inductive"}
COUNTRIES = {"india", "china", "america", "usa", "uk", "germany", "canada"}
EXPERIENCE_PATTERN = r"(\d+)[-\s]?(to|–|–)?\s*(\d+)?\s*(years|yrs|year|yr)?\s*(experience)?"

# Local model path
local_model_path = r"C:\Users\KIIT\Documents\shl_cv_parser/bert-base-uncased"
"""
def load_or_download_bert_model(path):
    if os.path.exists(path) and os.path.isfile(os.path.join(path, "vocab.txt")):
        tokenizer = BertTokenizer.from_pretrained(path, local_files_only=True)
        model = BertModel.from_pretrained(path, local_files_only=True)
    else:
        tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        model = BertModel.from_pretrained("bert-base-uncased")
        os.makedirs(path, exist_ok=True)
        tokenizer.save_pretrained(path)
        model.save_pretrained(path)
    return tokenizer, model

bert_tokenizer, bert_model = load_or_download_bert_model(local_model_path)
"""

#tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_vectorizer = TfidfVectorizer(
    stop_words='english',
    lowercase=True,
    token_pattern=r"(?u)\b\w\w+\b"  # default pattern, but now explicit
)


def preserve_phrases(text, phrase_list):
    text = text.lower()
    for phrase in phrase_list:
        pattern = re.escape(phrase.lower())
        text = re.sub(pattern, phrase.lower().replace(" ", "_"), text)
    return text

def clean_text(text):
    text = preserve_phrases(str(text), SKILLS | ROLES)
    text = re.sub(r"[^a-z0-9_\s]", " ", text.lower())
    return text.strip()

def extract_numbers(text):
    return re.findall(r'\d+', text)
"""
def get_bert_embedding(text):
    inputs = bert_tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
"""

def extract_target_duration(prompt):
    match = re.search(r'(\d+)\s*(minutes?|mins?)', prompt.lower())
    return int(match.group(1)) if match else None

# Score an item given the query details
def score_item(query_words, query_numbers, prompt, item):
    assessment_name = item.get("assessment_name", "").lower()
    description = item.get("description", "").lower()
    blob_fields = [
        assessment_name,
        description,
        " ".join(item.get("test_type", [])),
        item.get("remote_support", ""),
        item.get("adaptive_support", ""),
        str(item.get("duration", ""))
    ]
    blob = clean_text(" ".join(blob_fields))
    blob_words = set(blob.split())
    blob_numbers = extract_numbers(blob)

    score = 0.0

    # Skills match
    if SKILLS & query_words & blob_words:
        score += 4.0

    # Role match
    if ROLES & query_words & blob_words:
        score += 2.5

    # Soft skills match
    soft_skills_match = SOFT_SKILLS & query_words & blob_words
    if soft_skills_match:
        score += 0.5
        if ROLES & query_words & blob_words:
            score += 0.5  # boost if soft + role

    # Country match
    if COUNTRIES & query_words & blob_words:
        score += 0.25

    # Experience mention
    if re.search(EXPERIENCE_PATTERN, prompt) and re.search(EXPERIENCE_PATTERN, blob):
        score += 1.0

    # Duration match
    target_duration = extract_target_duration(prompt)
    item_duration_raw = str(item.get("duration", "")).strip()
    if target_duration:
        if item_duration_raw.isdigit():
            item_duration = int(item_duration_raw)
            duration_diff = abs(item_duration - target_duration)
            if duration_diff <= 5:
                score += 1.5
            elif duration_diff <= 10:
                score += 1.0
        else:
            print(f"Skipping duration comparison for non-numeric value: '{item_duration_raw}'")

    # Mild boost for shared general words
    shared = query_words & blob_words
    score += len(shared) * 0.1

    return score

def normalize_catalog(catalog):
    for item in catalog:
        for key in ['assessment_name', 'description']:
            if key in item and isinstance(item[key], str):
                item[key] = item[key].strip().lower()
    return catalog
    
def get_recommendations(prompt, catalog):
    query = clean_text(prompt)
    descriptions = []

    # Preprocess catalog items
    for item in catalog:
        assessment_name = item.get("assessment_name", "").lower()
        description = item.get("description", "").lower()
        blob_fields = [
            assessment_name,
            description,
            " ".join(item.get("test_type", [])),
            item.get("remote_support", ""),
            item.get("adaptive_support", ""),
            str(item.get("duration", ""))
        ]
        blob = clean_text(" ".join(blob_fields))
        descriptions.append(blob)

    # Get top matches using TF-IDF similarity
    top_indices, similarities = get_top_matches_tfidf(query, descriptions, top_k=10)
    
    # Collect top matching items from catalog
    top_items = []
    for idx, sim in zip(top_indices, similarities):
        item = catalog[idx]
        item['similarity'] = float(sim)  # Optional: include similarity score
        top_items.append(item)

    return top_items

"""
def get_recommendations(prompt, catalog):
    query = clean_text(prompt)
    query_words = set(query.split())
    query_numbers = extract_numbers(prompt)

    print("Query words:", query_words)
    print("Query numbers:", query_numbers)

    results = []

    for item in catalog:
        # Clean all fields and build a blob
        assessment_name = item.get("assessment_name", "").lower()
        description = item.get("description", "").lower()
        blob_fields = [
            assessment_name,
            description,
            " ".join(item.get("test_type", [])),
            item.get("remote_support", ""),
            item.get("adaptive_support", ""),
            str(item.get("duration", ""))
        ]
        blob = clean_text(" ".join(blob_fields))
        blob_words = set(blob.split())
        blob_numbers = extract_numbers(blob)

        score = 0

        # Match skills - high priority
        if SKILLS.intersection(query_words & blob_words):
            score += 10

        # Match roles - medium-high priority
        if ROLES.intersection(query_words & blob_words):
            score += 7

        # Match soft skills - low priority unless combined
        soft_match = SOFT_SKILLS.intersection(query_words & blob_words)
        if soft_match:
            score += 1
            if ROLES.intersection(query_words & blob_words):
                score += 1

        # Match countries - least priority
        if COUNTRIES.intersection(query_words & blob_words):
            score += 0.5

        # Match experience pattern
        if re.search(EXPERIENCE_PATTERN, prompt) and re.search(EXPERIENCE_PATTERN, blob):
            score += 2

        # Match duration
        target_duration = extract_target_duration(prompt)
        item_duration_raw = str(item.get("duration", "")).strip()
        if target_duration and item_duration_raw.isdigit():
            item_duration = int(item_duration_raw)
            if abs(item_duration - target_duration) <= 5:
                score += 3
            elif abs(item_duration - target_duration) <= 10:
                score += 2
        elif target_duration:
            print(f"Skipping duration comparison due to non-numeric item duration: '{item_duration_raw}'")

        # Mild boost for other shared words
        common_words = query_words.intersection(blob_words)
        score += len(common_words) * 0.25

        if score > 0:
            results.append((score, item))

    results.sort(reverse=True, key=lambda x: x[0])
    return [item for score, item in results[:10]]
"""

def get_top_matches_tfidf(query, descriptions, top_k=10):
    corpus = [query] + descriptions
    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)
    query_vec = tfidf_matrix[0]
    desc_vecs = tfidf_matrix[1:]
    similarities = cosine_similarity(query_vec, desc_vecs).flatten()
    top_indices = similarities.argsort()[::-1][:top_k]
    return top_indices, similarities[top_indices]
