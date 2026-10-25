# TalentMatch Intelligence Pipeline
### AI-Powered Multi-Format ATS Optimization & Recruitment Analytics Platform

## 🚀 Project Overview
**TalentMatch Intelligence Pipeline** is an end-to-end, production-grade enterprise data analytics and AI-driven screening solution designed to bridge the structural gap between unstructured candidate profiles and highly specific corporate job descriptions. 

Unlike traditional ATS software that relies on rigid keyword-counting algorithms, this framework evaluates semantic context, extracts keywords from multi-format artifacts (PDFs, PNG, JPG), scrapes job postings directly from online portals, tracks historical scoring trends via a local relational database, and exposes an interactive batch-ranking leaderboard for recruitment teams.

---

## 📊 Core Architecture & Technical Workflow
The architecture processes unstructured target payloads through five integrated pipeline lifecycle stages:

1. **Multi-Channel Data Ingestion:** The pipeline accepts raw character streams, document file uploads, or live job posting URLs (e.g., LinkedIn/Indeed). Web-based targets are parsed programmatically using a custom `BeautifulSoup` engine to filter out layout tags, script payloads, and styling code.
2. **Text Normalization Engine (Parser Node):** `parser_utils.py` automatically routes artifacts based on structural file extensions. Regular text-based PDFs stream directly through programmatic binary channels using `PyPDF2`, while image-based document snapshots are processed via a computer vision layer powered by `Tesseract OCR` and `Pillow (PIL)`.
3. **AI Cognitive Processing & Schema Enforcement:** Cleaned text segments are routed to `ai_engine.py` where they hit the state-of-the-art **`gemini-3.8-flash`** model node via the unified 2026 Google Gen AI SDK client gateway. A strict system validation prompt enforces a valid JSON return layout containing computed ATS compatibility indexing, structural proficiency inventories, missing critical capabilities, and a raw markdown single-column recruiter-ready resume template.
4. **URL-Encoding & Relational Data Ingestion:** To prevent connection framework runtime crashes caused by special character strings inside internal passwords (e.g., `Ravi@1618`), the workflow leverages `urllib.parse.quote_plus` to safely format database credentials. The payload metrics are then asynchronously updated into a local relational `MySQL Server` schema (`talentmatch_analytics_db.scan_logs`) via an object-relational mapping (ORM) setup running over `SQLAlchemy` and `PyMySQL`.
5. **Analytics & Visualization Dashboards:** The frontend presentation engine running on a native `Streamlit` server decodes database arrays to update live trend line charts, render interactive data frames, organize capabilities into visual red/green badge blocks, and execute batch-candidate leaderboard sorting algorithms.

---

## 📂 Project Directory Structure & Sequence
The project workspace is structured systematically to reflect enterprise modular coding standards:
* **`requirements.txt`** — System environment dependencies manifest file.
* **`parser_utils.py`** — Local data extraction scripts, OCR visual arrays, and HTML web-scraping controllers.
* **`ai_engine.py`** — Google Gen AI SDK client configuration, JSON cleaning wrappers, and generative model prompts.
* **`app.py`** — Primary control application, multi-tab Streamlit dashboard interface, URL-encoding logic, and relational MySQL database sync nodes.

---

## 🛠️ Tech Stack & Dependency Matrix (Why These Tools Were Chosen)
* **`google-genai`:** Implements the official 2026 unified AI engine routing. Legacy `google.generativeai` modules have been completely deprecated and throw 404 endpoint errors on v1beta API channels.
* **`urllib.parse`:** Encodes operational database authentication strings containing `@` symbols to bypass internal socket routing connection bugs.
* **`sqlalchemy` & `pymysql`:** Creates an automated database mapping wrapper that executes `CREATE TABLE IF NOT EXISTS` routines while isolating raw operations from SQL Injection vulnerabilities.
* **`pytesseract` & `Pillow (PIL)`:** Powers the computer vision scanning arrays required to extract characters from compressed digital images and phone screenshots.
* **`beautifulsoup4` & `requests`:** Allows direct web parsing to harvest text contents from dominant hiring portals without requiring hardcoded payload scraping blocks.
* **`pandas` & `json`:** Manages structured vectors to compute sorted multi-resume matrices and display dynamic ranking tables.

---

## ⚙️ Local Deployment & Execution Manual

### 1. Clone the Core Workspace
Initialize your local workspace environment by pulling the repository assets:
```bash
git clone https://github.com
cd talentmatch-intelligence-pipeline
```

### 2. Configure System Software Prerequisites
Ensure your local host running Windows has the **Tesseract OCR System Software** configured:
1. Download the production executable setup directly from the [Official Tesseract Installer Repository](https://github.com).
2. Install the program binaries and map the exact deployment executable address (`C:\Program Files\Tesseract-OCR\tesseract.exe`) to your `parser_utils.py` system paths.

### 3. Deploy Python Package Modules
Run the package manager script to sync all library layers listed in the system manifest:
```bash
python -m pip install -r requirements.txt
```

### 4. Initialize the Relational Server Layer
Verify that your local **MySQL Server** instance is actively listening on network port `3306` and that your administrative root user account credentials line up with your configuration values.

### 5. Obtain a Free AI Access Token
1. Secure a free-tier development authentication key by logging into the [Google AI Studio Console](https://google.com).
2. Copy the token generated under the API configuration profile page.

### 6. Boot Up the Dashboard Server Platform
Execute the system launch sequence via your project command line console:
```bash
python -m streamlit run app.py
```
Your active terminal console will automatically create a network route. Open your local browser session at `http://localhost:8501`, enter your secure Gemini access key inside the sidebar configurations window, and drop your profile assets to launch your first evaluation!
