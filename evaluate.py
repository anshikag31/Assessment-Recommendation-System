import requests
import re
from urllib.parse import urlparse
from fuzzywuzzy import fuzz

test_data = [
    {
        "query": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "relevant_assessments": [
            "Automata - Fix (New) | SHL",
            "Core Java (Entry Level) (New) | SHL",
            "Java 8 (New) | SHL",
            "Core Java (Advanced Level) (New) | SHL",
            "Java Design Patterns (New) | SHL ",
            " Java Frameworks( New) | SHL ",
            " Java Platform Enterprise Edition 7 (Java EE 7) | SHL ",
            " Business Communication (adaptive) | SHL ",
            "Business Communication | SHL ",
            " Interviewing and Hiring Concepts (U.S.) | SHL"
        ]
    },
    {
        "query": "I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options.",
        "relevant_assessments": [
            "Entry level Sales 7.1 (International) | SHL",
            "Entry Level Sales Sift Out 7.1 | SHL",
            "Entry Level Sales Solution | SHL",
            "Sales Transformation Individual Contributor | SHL",
            "Sales Manager Solution | SHL",
            "Insurance Sales Manager Solution | SHL",
            "Sales Representative Solution | SHL",
            "Contact Center Sales Service | SHL",
            "Sales Support Specialist Solution | SHL",
            "Technical Sales Associate Solution | SHL",
            "SVAR - Spoken English (Indian Accent) (New) | SHL",
            "Sales & Service Phone Solution | SHL",
            "Sales & Service Phone Simulation | SHL",
            "English Comprehension (New) | SHL"
        ]
    },
    {
        "query": "I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour.",
        "relevant_assessments": [
            "Motivation Questionnaire MQM5 | SHL",
            "Global Skills Assessment | SHL",
            "Administrative Professional - Short Form | SHL",
            "Graduate 8.0 Job Focused Assessment | SHL"
        ]
    },
    {
        "query": "Content Writer required, expert in English and SEO.",
        "relevant_assessments": [
            "Drupal (New) | SHL",
            "Writex Email Writing | SHL",
            "Spelling | SHL",
            "Search Engine Optimization (New) | SHL",
            "Administrative Professional - Short Form | SHL",
            "General Entry Level – Data Entry 7.0 Solution | SHL"
        ]
    },
    {
        "query": "I am looking for a QA Engineer with automation and manual testing experience. Give me a 1-hour assessment.",
        "relevant_assessments": [
            "Manual Testing (New) | SHL",
            "Automata Selenium | SHL",
            "Automata - Fix (New) | SHL",
            "Automation Anywhere RPA Development | SHL",
            "Micro Focus Unified Functional Testing (New) | SHL",
            "Automata Front End | SHL",
            "JavaScript (New) | SHL",
            "HTML/CSS (New) | SHL",
            "Selenium (New) | SHL",
            "SQL Server (New) | SHL",
            "Automata - SQL (New) | SHL"
           
        ]
    },
    {
        "query": "ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long.",
        "relevant_assessments": [
            "Administrative Professional - Short Form | SHL",
            "Verify - Numerical Ability | SHL",
            "Business Commnications | SHL",
            "Bank Collections Agent Short Form | SHL",
            "Financial Professional - Short Form | SHL",
            "Bank Administrative Assistant - Short Form | SHL",
            "Bank Operations Supervisor - Short Form | SHL",
            "General Entry Level – Data Entry 7.0 Solution | SHL",
            "Basic Computer Literacy (Windows 10) (New) | SHL"
        ]
    },
    {
        "query": "I am hiring for a creative content role with a focus on branding and marketing. The assessment should be at most 90 mins.",
        "relevant_assessments": [
            "SHL Verify Interactive - Inductive Reasoning | SHL",
            "Global Skills Development Report | SHL",
            "Sales Manager Solution | SHL",
            "Customer Service Short Form | SHL",
            "Marketing (New) | SHL",
            "Occupational Personality Questionnaire OPQ32r | SHL"
        ]
    }
]
def extract_assessment_name(url, description):
    path = urlparse(url).path
    name_from_url = path.rstrip('/').split('/')[-1].replace('-', ' ').title()
    name_from_desc = description.split(':')[0].strip() if ':' in description else ''
    name = name_from_desc if name_from_desc and len(name_from_desc) > 5 else name_from_url
    return f"{name} | SHL"


def normalize_name(name):
    name = name.lower()
    name = re.sub(r'\| shl$', '', name)
    name = re.sub(r'\([^)]*\)', '', name)  # Remove (New), (Advanced), etc.
    name = re.sub(r'[^\w\s]', '', name)  # Remove punctuation
    name = re.sub(r'\d+\.*\d*', '', name)  # Remove version numbers
    name = re.sub(r'\s+', ' ', name)
    return name.strip()

def enhanced_fuzzy_match(str1, str2, threshold=75):
    norm1 = normalize_name(str1)
    norm2 = normalize_name(str2)
    score = fuzz.token_sort_ratio(norm1, norm2)
    if score >= threshold:
        print(f"✅ Match: '{norm1}' ≈ '{norm2}' (Score: {score})")
        return True
    else:
        print(f"❌ No match: '{norm1}' ≠ '{norm2}' (Score: {score})")
        return False


def recall_at_k_fuzzy(relevant, predicted, k, threshold=75):
    predicted_at_k = predicted[:k]
    hits = 0
    for r in relevant:
        for p in predicted_at_k:
            if enhanced_fuzzy_match(r, p, threshold):
                hits += 1
                break
    return hits / len(relevant) if relevant else 0.0

def average_precision_at_k_fuzzy(relevant, predicted, k, threshold=75):
    score = 0.0
    hits = 0
    predicted_at_k = predicted[:k]
    matched = set()

    for i, p in enumerate(predicted_at_k):
        for r in relevant:
            if r not in matched and enhanced_fuzzy_match(p, r, threshold):
                hits += 1
                matched.add(r)
                score += hits / (i + 1)
                break
    return score / min(len(relevant), k) if relevant else 0.0

def evaluate(test_data, k=10, threshold=75):
    recall_scores = []
    map_scores = []

    for example in test_data:
        query = example["query"]
        relevant = example["relevant_assessments"]

        print(f"\n🔍 Evaluating query: {query}")

        try:
            response = requests.post("http://127.0.0.1:8000/recommend", json={"query": query})
            print(f"🔁 Response Status Code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"📦 Response JSON: {result}")
                print("🔎 Raw recommended assessments from response:")
                for r in result.get("recommended_assessments", []):
                    print(f" - URL: {r.get('url')}, Description: {r.get('description')}")

                recommended_assessments = [
                    extract_assessment_name(r["url"], r["description"])
                    for r in result.get("recommended_assessments", [])
                ]

                recall = recall_at_k_fuzzy(relevant, recommended_assessments, k, threshold)
                ap = average_precision_at_k_fuzzy(relevant, recommended_assessments, k, threshold)

                recall_scores.append(recall)
                map_scores.append(ap)

                print(f"✅ Recall@{k}: {recall:.4f}, AP@{k}: {ap:.4f}")
            else:
                print(f"❌ Failed to fetch for query. Status Code: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error while making request: {e}")

    mean_recall = sum(recall_scores) / len(recall_scores) if recall_scores else 0.0
    mean_ap = sum(map_scores) / len(map_scores) if map_scores else 0.0

    print(f"\n📊 Final Evaluation:")
    print(f"Mean Recall@{k}: {mean_recall:.4f}")
    print(f"MAP@{k}: {mean_ap:.4f}")

if __name__ == "__main__":
    evaluate(test_data, k=10)

"""
import requests

test_data = [
    {
        "query": "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "relevant_assessments": [
            "Automata - Fix (New) | SHL",
            "Core Java (Entry Level) (New) | SHL",
            "Java 8 (New) | SHL",
            "Core Java (Advanced Level) (New) | SHL",
            "Agile Software Development | SHL",
            "Technology Professional 8.0 Job Focused Assessment | SHL",
            "Computer Science (New) | SHL"
        ]
    },
    {
        "query": "I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test. Give me some options.",
        "relevant_assessments": [
            "Entry level Sales 7.1 (International) | SHL",
            "Entry Level Sales Sift Out 7.1 | SHL",
            "Entry Level Sales Solution | SHL",
            "Sales Representative Solution | SHL",
            "Sales Support Specialist Solution | SHL",
            "Technical Sales Associate Solution | SHL",
            "SVAR - Spoken English (Indian Accent) (New) | SHL",
            "Sales & Service Phone Solution | SHL",
            "Sales & Service Phone Simulation | SHL",
            "English Comprehension (New) | SHL"
        ]
    },
    {
        "query": "I am looking for a COO for my company in China and I want to see if they are culturally a right fit for our company. Suggest me an assessment that they can complete in about an hour.",
        "relevant_assessments": [
            "Motivation Questionnaire MQM5 | SHL",
            "Global Skills Assessment | SHL",
            "Graduate 8.0 Job Focused Assessment | SHL"
        ]
    },
    {
        "query": "Content Writer required, expert in English and SEO.",
        "relevant_assessments": [
            "Drupal (New) | SHL",
            "Search Engine Optimization (New) | SHL",
            "Administrative Professional - Short Form | SHL",
            "General Entry Level – Data Entry 7.0 Solution | SHL"
        ]
    },
    {
        "query": "I am looking for a QA Engineer with automation and manual testing experience. Give me a 1-hour assessment.",
        "relevant_assessments": [
            "Automata Selenium | SHL",
            "Automata - Fix (New) | SHL",
            "Automata Front End | SHL",
            "JavaScript (New) | SHL",
            "HTML/CSS (New) | SHL",
            "HTML5 (New) | SHL",
            "CSS3 (New) | SHL",
            "Selenium (New) | SHL",
            "SQL Server (New) | SHL",
            "Automata - SQL (New) | SHL",
            "Manual Testing (New) | SHL"
        ]
    },
    {
        "query": "ICICI Bank Assistant Admin, Experience required 0-2 years, test should be 30-40 mins long.",
        "relevant_assessments": [
            "Administrative Professional - Short Form | SHL",
            "Verify - Numerical Ability | SHL",
            "Financial Professional - Short Form | SHL",
            "Bank Administrative Assistant - Short Form | SHL",
            "General Entry Level – Data Entry 7.0 Solution | SHL",
            "Basic Computer Literacy (Windows 10) (New) | SHL"
        ]
    },
    {
        "query": "I am hiring for a creative content role with a focus on branding and marketing. The assessment should be at most 90 mins.",
        "relevant_assessments": [
            "SHL Verify Interactive - Inductive Reasoning | SHL",
            "Occupational Personality Questionnaire OPQ32r | SHL"
        ]
    }
]
def normalize_name(name):
    #Normalize assessment names for comparison.
    return name.strip().lower().replace("–", "-").replace("—", "-").replace("  ", " ")


def recall_at_k(relevant, predicted, k):
    relevant_set = set(normalize_name(r) for r in relevant)
    predicted_at_k = [normalize_name(p) for p in predicted[:k]]
    hits = len([item for item in predicted_at_k if item in relevant_set])
    return hits / len(relevant) if relevant else 0.0

def average_precision_at_k(relevant, predicted, k):
    score = 0.0
    hits = 0
    normalized_relevant = [normalize_name(r) for r in relevant]
    normalized_predicted = [normalize_name(p) for p in predicted[:k]]

    for i, p in enumerate(normalized_predicted):
        if p in normalized_relevant and p not in normalized_predicted[:i]:
            hits += 1
            score += hits / (i + 1)
    return score / min(len(relevant), k) if relevant else 0.0

def evaluate(test_data, k=10):
    recall_scores = []
    map_scores = []

    for example in test_data:
        query = example["query"]
        relevant = [r.split(" | ")[0] for r in example["relevant_assessments"]]

        print(f"\n🔍 Evaluating query: {query}")

        try:
            response = requests.post("http://127.0.0.1:8000/recommend", json={"query": query})

            print(f"🔁 Response Status Code: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"📦 Response JSON: {result}")

                recommended_assessments = [
                    r.get("name", "").strip() for r in result.get("recommended_assessments", [])
                ]

                recall = recall_at_k(relevant, recommended_assessments, k)
                ap = average_precision_at_k(relevant, recommended_assessments, k)

                recall_scores.append(recall)
                map_scores.append(ap)

                print(f"✅ Recall@{k}: {recall:.4f}, AP@{k}: {ap:.4f}")
            else:
                print(f"❌ Failed to fetch for query. Status Code: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Error while making request: {e}")

    mean_recall = sum(recall_scores) / len(recall_scores) if recall_scores else 0.0
    mean_ap = sum(map_scores) / len(map_scores) if map_scores else 0.0

    print(f"\n📊 Final Evaluation:")
    print(f"Mean Recall@{k}: {mean_recall:.4f}")
    print(f"MAP@{k}: {mean_ap:.4f}")

# Run evaluation
evaluate(test_data, k=10)

"""
