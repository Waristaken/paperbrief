
# 📄 PaperBrief // AI Research Intelligence System

PaperBrief is a high-tech, dark-themed full-stack AI workspace engineered to ingest complex academic research manuscripts (PDFs), parse their raw textual layers, and extract structural intelligence parameters using the Gemini AI API framework.

## ⚡ Architectural Advantages Over Consumer Chatbots

- **Zero-Prompting Execution:** The granular text parsing and prompting logic are fully abstracted away inside a secure backend pipeline (`extractor.py`). Users upload metrics and receive predictable data visualization panels instantly without drafting instructions.
- **Strict JSON Serialization:** The architecture enforces a rigid JSON response template structure from the underlying LLM layer. This converts loose narrative feedback into searchable database strings and arrays.
- **Ephemeral Processing Privacy:** Features an integrated data-destruction cycle. Uploaded manuscripts are permanently deleted from the host server disk space (`os.remove`) the exact millisecond background evaluations finish, ensuring zero historical logging risk.

## 🛠️ Complete Technology Stack

- **Backend Logic:** Python, Flask Server Routing Core
- **AI Processing Pipeline:** Google Gemini API (`gemini-flash-latest`)
- **Document Engineering:** PyMuPDF / Fitz Layout Extraction Engine
- **Frontend Panel:** Custom CSS Neon-Grid UI & Interactive JavaScript Drag-and-Drop Event API 

---

## 📁 Repository Project Architecture

```text
paperbrief/
├── static/
│   ├── script.js        # Drag-and-Drop Event Mappings & Async API Fetch Controller
│   └── style.css         # Dark Neon Cyberpunk Design UI Framework
├── templates/
│   └── index.html       # Structural Grid Interface Elements & Form IDs
├── uploads/             # Ephemeral Local Landing Space (Auto-wiped)
├── .gitignore           # Configuration Matrix Protecting Secret Environment Variables
├── app.py               # Main Flask Multi-Part Stream Data Router
└── extractor.py         # Document Token Extraction & Schema Mapping Controller
```

---

## 🚀 Local Deployment Configurations

To build and run this system locally on your terminal node, execute the following parameters:

### 1. Initialize Workspace Environment
Clone this project repository to your local directory block and spin up an isolated virtual python execution cell:
```bash
git clone https://github.com
cd paperbrief
python -m venv .venv
```

### 2. Activate Terminal Shell & Load Dependencies
Activate your local virtual script context and execute package configurations:

**For Windows PowerShell:**
```powershell
.\.venv\Scripts\Activate.ps1
pip install flask pymupdf google-generativeai python-dotenv
```

### 3. Inject Access Keys
Create a local `.env` configuration file sitting directly inside your root workspace folder and bind your Google AI Studio credentials:
```env
GOOGLE_API_KEY=your_private_gemini_api_key_here
```

### 4. Execute Core Server
Launch your main Flask application worker loop:
```bash
python app.py
