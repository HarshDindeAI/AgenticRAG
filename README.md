# 🤖 AgenticRAG

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Next.js](https://img.shields.io/badge/Next.js-15.2.4-black.svg)](https://nextjs.org/)
[![FlaskAPI](https://img.shields.io/badge/FlaskAPI-latest-teal.svg)](http://flask.palletsprojects.com/en/stable/)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://reactjs.org/)

A modern web application that combines RAG (Retrieval-Augmented Generation) with agentic capabilities for intelligent document processing and querying.


## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Diagram](#-diagram)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Application](#-running-the-application)
- [Development](#-development)
- [Dependencies](#-dependencies)

## 📁 Project Structure

```
AgenticRAG/
├── app/
│   ├── backend/           # Python backend server
│   │   ├── agent.py       # Agent implementation
│   │   ├── app.py         # FastAPI server
│   │   ├── prepdocs.py    # Document preprocessing
│   │   ├── search.py      # Search functionality
│   │   └── parse_tabular.py  # Tabular data parsing
│   └── frontend/          # Next.js frontend application
│       ├── src/           # Source code
│       ├── public/        # Static assets
│       └── package.json   # Frontend dependencies
├── data/                  # Data directory
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## Diagram
<img src="./image.png"></img>

## ✨ Features

- 📄 **Document preprocessing** and parsing
- 📊 **Tabular data support** (Excel, CSV) (Upcoming)
- 🔍 **Intelligent search** capabilities
- 🧠 **Agent-based** query processing
- 💻 **Modern web interface**
- 🔢 **Token counting** and management

## 🛠️ Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/HarshDindeAI/AgenticRAG.git
cd AgenticRAG
```

### 2. Set up the Python environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# For Linux/Mac:
source .venv/bin/activate
# For Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# For Windows (Command Prompt):
.\.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt
```

### 3. Set up environment variables

```bash
# For Linux/Mac:
cp app/backend/.env.example app/backend/.env
# For Windows (PowerShell):
Copy-Item app/backend/.env.example app/backend/.env
# For Windows (Command Prompt):
copy app\backend\.env.example app\backend\.env
```

Edit the `.env` file with your configuration:

| Variable | Description | Example |
|----------|-------------|---------|
| `POSTGRES_CONNECTION_STRING` | PostgreSQL database connection | `postgresql+psycopg://username:password@localhost:port/database` |
| `DEVICE` | Computing device | `cpu` or `cuda` for GPU support |
| `MODEL` | AI model path | `models/gemini-2.0-flash` |
| `TEMPERATURE` | Model randomness (0.0-1.0) | `0.3` |
| `GEMINI_API_KEY` | Google Gemini API key | `your-api-key` |
| `COLLECTION_NAME` | Document collection name | `lib` |

### 4. Install frontend dependencies

```bash
cd app/frontend
npm install
```

## 🖥️ Running the Application

### 1. Start the backend server

```bash
# Make sure you're in the project root directory
# For Linux/Mac:
cd app/backend
uvicorn app:app --reload
# For Windows:
cd app\backend
uvicorn app:app --reload
```

### 2. Start the frontend development server

```bash
# In a new terminal, make sure you're in the project root directory
# For Linux/Mac:
cd app/frontend
npm run dev
# For Windows:
cd app\frontend
npm run dev
```

The application will be available at `http://localhost:3000` 🎉

## 🛠️ Development

- `
- 🔄 Frontend development server supports hot reloading
- 📝 Use `npm run lint` to check frontend code style

## 📦 Dependencies

### Backend
- pandas >= 2.0.0
- openpyxl >= 3.1.0
- tiktoken >= 0.5.0
- xlrd >= 2.0.1

### Frontend
- React 19
- Next.js 15.2.4
- TypeScript

---

Made with ❤️ and 🧠 by HarshDindeAI
