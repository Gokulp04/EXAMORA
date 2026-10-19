# EXAMORA

## AI-Powered Exam Preparation Assistant

EXAMORA is a smart exam preparation platform designed to help
students prepare efficiently when they have limited time before
an examination.

Instead of forcing students to study an entire syllabus,
EXAMORA allows them to select a specific module and creates
a focused preparation workflow based on their available study time.

---

## 🎯 Problem Statement

Students often face difficulty preparing for examinations when:

- The syllabus is large.
- Study material is scattered across multiple files.
- They have limited preparation time.
- They do not know which topics are important.
- They spend too much time deciding what to study.
- They try to prepare every module even when only one module
  is required for a CIA or unit test.

EXAMORA addresses these problems through an intelligent,
module-focused preparation system.

---

## 💡 Solution

EXAMORA provides a structured workflow:

1. Enter subject details.
2. Upload the syllabus.
3. Detect Module 1 to Module 5.
4. Upload study material.
5. Select only the required module.
6. Analyze important topics.
7. Generate exam-oriented questions.
8. Create a personalized study plan.
9. Generate quick revision points.
10. Calculate an exam readiness score.

---

## 🚀 Key Features

### 1. Subject & Exam Setup

Students can enter:

- Subject name
- Exam date
- Available study time

---

### 2. Syllabus Processing

EXAMORA can process:

- PDF
- PPTX
- DOCX
- TXT

The uploaded syllabus is analyzed to identify
Module 1 to Module 5.

---

### 3. Module-Focused Preparation

Students can select a single module.

For example:

Module 2 → Machine Learning

EXAMORA analyzes only Module 2 instead of unnecessarily
including all five modules.

---

### 4. Study Material Processing

Students can upload multiple files for a selected module.

EXAMORA extracts readable text from the uploaded material
and combines it for analysis.

---

### 5. Topic Importance Analysis

Topics are evaluated using rule-based intelligent scoring.

Each topic receives:

- Importance score
- Priority
- Star rating

Priority levels include:

- Very High
- High
- Medium
- Low

---

### 6. Content Percentage

EXAMORA calculates the approximate content contribution
of each module.

Example:

Module 1 → 18%
Module 2 → 24%
Module 3 → 20%
Module 4 → 17%
Module 5 → 21%

The percentage is calculated from extracted content.

---

### 7. Exam Question Generation

EXAMORA generates exam-oriented questions such as:

- 2 Mark
- 5 Mark
- 10 Mark
- 13 Mark
- 16 Mark

Questions are generated from the important topics
identified during analysis.

---

### 8. Smart Study Planner

The study planner uses:

- Available study time
- Topic importance
- Topic priority

to distribute preparation time.

Example:

3 Hours Available

→ Classification — 45 min
→ Regression — 35 min
→ Evaluation — 30 min
→ Applications — 25 min
→ Revision — remaining time

---

### 9. Quick Revision

EXAMORA generates focused revision points
for last-minute preparation.

---

### 10. Exam Readiness

The system calculates a preparation readiness score
based on:

- Topic coverage
- Topic importance
- Available study time

---

## 🏗️ Project Architecture

```text
EXAMORA/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── uploads/
│   ├── syllabus/
│   ├── module_1/
│   ├── module_2/
│   ├── module_3/
│   ├── module_4/
│   └── module_5/
│
├── data/
│   ├── extracted/
│   └── processed/
│
├── ai/
│   ├── __init__.py
│   ├── processor.py
│   ├── analyzer.py
│   ├── question_generator.py
│   └── study_planner.py
│
├── services/
│   ├── __init__.py
│   ├── file_service.py
│   ├── syllabus_service.py
│   ├── module_service.py
│   └── analysis_service.py
│
├── utils/
│   ├── __init__.py
│   ├── pdf_utils.py
│   ├── ppt_utils.py
│   ├── docx_utils.py
│   └── text_utils.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── modules.html
│   ├── preparation.html
│   ├── analysis.html
│   ├── questions.html
│   └── results.html
│
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── dashboard.css
│   │
│   ├── js/
│   │   ├── main.js
│   │   ├── upload.js
│   │   └── dashboard.js
│   │
│   └── images/
│
└── tests/
    ├── test_pdf.py
    ├── test_modules.py
    └── test_planner.py