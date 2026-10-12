# EXAMORA — AI-Powered Exam Preparation Assistant

**Study Smarter. Prepare Better. Perform with Confidence.**

EXAMORA is a Python and Flask-based web application designed to help students prepare for examinations in a structured and time-efficient way.

Students often struggle to organize lecture notes, PDFs, presentations, and other study materials, especially when examinations are approaching. EXAMORA aims to simplify this process by processing uploaded learning materials, organizing content module-wise, identifying important topics, generating practice questions, and preparing study plans based on the student's available time.

## Overview

EXAMORA provides a centralized platform for managing examination preparation. Students can upload their study materials, review module-wise content, analyze topics, practice questions, and follow a structured preparation plan.

The current version uses document extraction and rule-based analysis. It is designed as a foundation for future integration with advanced AI and natural language processing services.

## Key Features

- **Study Dashboard:** Provides a central interface for examination preparation.
- **Study Material Upload:** Supports PDF, PPTX, DOCX, and TXT files.
- **Syllabus Processing:** Helps identify and organize syllabus modules.
- **Module-Wise Preparation:** Organizes preparation around individual modules.
- **Content Analysis:** Extracts text and analyzes learning material using rule-based techniques.
- **Important Topic Identification:** Uses heuristic scoring to prioritize topics.
- **Practice Question Generation:** Creates practice questions for different mark categories.
- **Personalized Study Planning:** Helps organize preparation based on available study time.
- **Revision Support:** Provides structured revision content and preparation summaries.
- **Readiness Overview:** Displays a preparation-readiness score based on the application's analysis.
- **Flask Web Interface:** Provides a browser-based experience.

*Note: Generated questions, topic priorities, and readiness scores are heuristic estimates. They are not guaranteed predictions of actual examination questions or marks.*

## Technology Stack

### Backend
- Python
- Flask
- Werkzeug

### Document Processing
- pypdf
- python-pptx
- python-docx

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2 templates

### Configuration
- python-dotenv
- Gunicorn for deployment

## Project Structure

```text
EXAMORA/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
├── uploads/
│   ├── syllabus/
│   ├── module_1/
│   ├── module_2/
│   ├── module_3/
│   ├── module_4/
│   └── module_5/
├── data/
│   ├── extracted/
│   └── processed/
├── ai/
│   ├── __init__.py
│   ├── processor.py
│   ├── analyzer.py
│   ├── question_generator.py
│   └── study_planner.py
├── services/
│   ├── __init__.py
│   ├── file_service.py
│   ├── syllabus_service.py
│   ├── module_service.py
│   └── analysis_service.py
├── utils/
│   ├── __init__.py
│   ├── pdf_utils.py
│   ├── ppt_utils.py
│   ├── docx_utils.py
│   └── text_utils.py
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
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── tests/
    ├── test_pdf.py
    ├── test_modules.py
    └── test_planner.py
```

## Getting Started

### Prerequisites

- Python 3.11 or a compatible supported Python version
- pip
- Git (for cloning the repository)

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd EXAMORA
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual repository URL.

### 2. Create a Virtual Environment

**Windows:**

```bash
py -m venv .venv
.venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Make sure `requirements.txt` includes all required packages, including `gunicorn` if it is needed for your deployment platform.

### 4. Configure Environment Variables

Create a local `.env` file and configure the application secret:

```env
EXAMORA_SECRET_KEY=replace-with-a-strong-random-secret
```

Use a unique secret for your own environment. Never commit `.env` files, API keys, or passwords to GitHub.

### 5. Run the Application

```bash
py app.py
```

Open your browser and visit:

http://127.0.0.1:5000

### 6. Run Tests

```bash
py -m unittest discover -s tests -v
```

## How It Works

1. The student opens the EXAMORA web application.
2. The student enters examination details and uploads available study materials.
3. The application extracts readable text from supported documents.
4. The syllabus and learning content are organized for module-wise preparation.
5. Rule-based analysis identifies potential topics for focused revision.
6. The application generates practice questions and a study plan.
7. The student uses the resulting preparation dashboard to guide revision.

## Current Limitations

- Topic identification and question generation use rule-based logic and may require manual review.
- Scanned PDFs may require OCR support, which is not guaranteed in the current version.
- The current prototype uses local file storage and a shared analysis file.
- Multi-user accounts, isolated user data, and production-grade database storage are not yet implemented.
- Uploaded materials may not persist on hosting platforms that use ephemeral storage.
- The readiness score is an estimate generated by the application, not a validated measure of exam performance.

## Future Enhancements

- Integration with a large language model for more advanced content understanding.
- Optical Character Recognition (OCR) for handwritten and scanned notes.
- Database integration for securely storing users, subjects, and preparation progress.
- Individual student accounts and isolated study materials.
- Persistent cloud storage for uploaded documents.
- Improved syllabus extraction and configurable module detection.
- More advanced question generation and revision recommendations.
- Progress tracking and examination analytics.
- Responsive UI improvements and accessibility enhancements.

## Security Notes

- Never commit `.env`, passwords, API keys, private study materials, or personal information.
- Validate uploaded files and enforce suitable file-size limits.
- Use secure secret management and production settings when deploying.
- Implement authentication, access controls, and isolated storage before supporting multiple students.

## Project Status

**Status:** Prototype / Active Development

EXAMORA is being developed as an educational technology project to make exam preparation more organized, accessible, and time-efficient.

## License

Choose a license before distributing or reusing this project. If you intend to publish it as an open-source project, consider adding an appropriate license file.

---

**EXAMORA — Making Exam Preparation More Organized.**
