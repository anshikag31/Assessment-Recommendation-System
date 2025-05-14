# Intelligent SHL Assessment Recommendation System

## Objective : 
To build a smart recommendation engine that suggests relevant SHL assessments based on recruiter queries. The system understands context, role requirements, skills, soft skills, and duration constraints using NLP and traditional ML techniques.

## Approach : 
We adopted a hybrid scoring system combining TF-IDF-based semantic similarity with rule-based heuristics to match recruiter prompts with assessment descriptions. The goal was to mimic a domain expert's ability to parse vague queries and map them to structured assessment catalogs.

## Modules and Logic

## 1.utils.py 
– Core NLP & Matching Logic

Text Cleaning & Phrase Preservation
Replaces multi-word phrases (e.g., "core java") with underscores to maintain semantic unity during tokenization.

TF-IDF Similarity
Utilized TfidfVectorizer to compute cosine similarity between the prompt and catalog assessment blobs to capture textual closeness.

Heuristic Scoring (via score_item)
Applied domain knowledge:
+4 for strong technical skill match
+2.5 for role/title alignment
+0.5 for soft skills and an extra 
+0.5 when combined with roles
+0.25 for country references
+1 for matching experience pattern
+1 to +1.5 for duration closeness (within 5–10 mins)
Small bonus for shared words

Custom Duration Parsing
Extracts duration from query and handles flexible string inputs like "40 mins" or "1 hour".
Embedded BERT model support for semantic embeddings (commented out for local resource constraints).

## 2.Workflow

Query Input: e.g., "Need a Java Developer with good communication skills, test duration ~40 mins".

Text Normalization: Preserve key phrases, remove noise.

TF-IDF Similarity: Find top 10 closest assessments.

Heuristic Scoring: Re-rank using the custom score function based on multiple overlapping criteria.

Output: Ranked list of recommended assessments.

## 3.evaluate.py – Benchmark Testing

Used predefined test cases mimicking real-world recruiter queries.

Compared system's top N output against ground truth labels for recall-based evaluation.

Included diverse job roles: Developer, Sales, Content Writer, QA Engineer, and Administrative Assistant.

## 4.Dependencies

scikit-learn, torch, transformers, fuzzywuzzy, re, json, requests

Local support for BERT model loading (with fallback to HuggingFace Hub)

## 5.Results (Sample Case)

Query: "Looking for a Java Developer with soft skills for a 40 min assessment"

## Top Matches:
"Automata - Fix (New) | SHL", 
"Core Java (Entry Level) (New) | SHL", 
"Java 8 (New) | SHL", 
"Core Java (Advanced Level) (New) | SHL", 
"Java Design Patterns (New) | SHL ", 
" Java Frameworks( New) | SHL ", 
Scoring matched the expected relevant assessments, verifying the accuracy and domain alignment.

## 6. Final Evaluation:
Mean Recall@10: 0.5042
MAP@10: 0.3926

## 7. Key Features
Handles natural language input with partial or vague descriptions
Incorporates skill-role-soft skill heuristics
Filters by duration and experience
Designed to scale with any structured assessment catalog

## URL of the webapp that you built? Please make sure that it is functioning and reachable for us to try - 
https://assessment-recommendation-system-gtzdef2pbjzyjebofmy5nj.streamlit.app/

## Get API end point which can be queried using a query or piece of text and returns result in JSON? - 
https://assessment-recommendation-system-3p5c.onrender.com/recommend?query=I%20am%20hiring%20for%20Java%20developers%20who%20can%20also%20collaborate%20effectively%20with%20my%20business%20teams.%20Looking%20for%20an%20assessment(s)%20that%20can%20be%20co
(enter the query in the link, after query = )
