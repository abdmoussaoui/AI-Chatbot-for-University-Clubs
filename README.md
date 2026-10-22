# 🤖 FSBM Club Advisor — AI-Powered University Club Recommendation Chatbot

An intelligent, AI-powered conversational assistant designed to help students at the **Faculty of Sciences Ben M'Sik (FSBM)** discover student clubs that best match their interests, skills, and personal aspirations.

Built as a full-stack application, the system combines a modern **React and TypeScript frontend** with a **Python/FastAPI backend**, leveraging **Retrieval-Augmented Generation (RAG)**, semantic search, and Large Language Models (LLMs) to deliver accurate, context-aware, and personalized club recommendations.

---

## ✨ Key Features

- **Conversational AI:** Interacts naturally with students to understand their interests, skills, preferences, and goals.
- **Personalized Club Recommendations:** Identifies and recommends the most suitable student clubs based on individual profiles.
- **Retrieval-Augmented Generation (RAG):** Grounds AI-generated responses in verified club information stored in `clubs.json`, reducing hallucinations and improving reliability.
- **Semantic Search:** Uses vector embeddings and FAISS to retrieve relevant club information based on the meaning of student queries.
- **Dynamic Data Visualization:** Automatically generates bar charts illustrating club compatibility scores after recommendations.
- **Modern & Responsive Interface:** Provides an intuitive, interactive chat experience developed with React, TypeScript, and Tailwind CSS.
- **Full-Stack Architecture:** Separates frontend and backend services to improve organization and maintainability.

---

## 🏗️ Project Architecture

The application follows a modular, full-stack architecture organized into two main components:

- **Backend:** Handles conversational AI, RAG processing, semantic retrieval, recommendation generation, API communication, and data visualization.
- **Frontend:** Provides a responsive user interface for interacting with the chatbot and displaying recommendations.

### Project Structure

```bash
AI-Chatbot-for-University-Clubs/
│
├── backend/                    # Python / FastAPI backend
│   ├── data/
│   │   └── clubs.json          # Student clubs dataset
│   ├── static/
│   │   └── plots/              # Generated visualization charts
│   ├── main.py                 # API entry point
│   ├── rag_chain.py            # RAG pipeline implementation
│   ├── visualization.py        # Recommendation visualization
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment configuration
│
└── frontend/                   # React / TypeScript frontend
    ├── src/                    # Frontend source code
    ├── package.json            # JavaScript dependencies
    └── ...
```

---

## 🛠️ Technology Stack

### Backend

| Technology | Purpose |
|---|---|
| Python 3.9+ | Backend programming language |
| FastAPI | REST API development |
| LangChain | RAG pipeline orchestration |
| OpenRouter | Access to LLMs such as Mistral 7B |
| Hugging Face | Sentence-transformer embedding models |
| FAISS | Vector storage and semantic similarity search |
| Matplotlib | Recommendation score visualization |
| Uvicorn | ASGI application server |

### Frontend

| Technology | Purpose |
|---|---|
| React | Interactive user interface |
| TypeScript | Type-safe frontend development |
| Vite | Fast development and build tooling |
| Tailwind CSS | Responsive UI styling |
| Axios | Frontend–backend API communication |

---

## 🚀 Getting Started

Follow the instructions below to install and run the application locally.

### Prerequisites

Make sure the following tools are installed:

- **Node.js 18+** and npm
- **Python 3.9+** and pip
- An **OpenRouter API key**, available at [openrouter.ai](https://openrouter.ai)

### 1. Backend Installation

Navigate to the backend directory:

```bash
cd backend
```

**Create a Python virtual environment:**

```bash
python -m venv venv
```

**Activate the virtual environment:**

Windows:

```bash
.\venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

On macOS or Linux, you can use `python3` instead of `python` when creating the virtual environment.

**Install the Python dependencies:**

```bash
pip install -r requirements.txt
```

**Configure the environment variables:**

Create a `.env` file inside the `backend` directory.

macOS / Linux:

```bash
touch .env
```

Windows PowerShell:

```powershell
New-Item .env -ItemType File
```

Add the required configuration described in the **Environment Variables** section.

**Start the backend server:**

```bash
uvicorn main:app --reload
```

The backend API will be accessible at:

**http://127.0.0.1:8000**

The server automatically loads the necessary models and initializes the retrieval system at startup.

### 2. Frontend Installation

Open a new terminal and navigate to the frontend directory from the project root:

```bash
cd frontend
```

**Install the required dependencies:**

```bash
npm install --legacy-peer-deps
```

**Start the development server:**

```bash
npm run dev
```

The frontend application will be accessible at:

**http://localhost:5173**

Open this address in your browser to interact with the AI-powered club advisor.

---

## ⚙️ Environment Variables

The backend requires a `.env` file to manage API credentials and application configuration.

Create `backend/.env` and add the following variables:

```env
# OpenRouter API authentication
OPENROUTER_API_KEY="your_openrouter_api_key"

# Frontend origin allowed by the CORS policy
CORS_ORIGINS="http://localhost:5173"

# OpenRouter application identification
SITE_URL="http://localhost:8000"
SITE_NAME="FSBM Club Assistant"
```

### Configuration Details

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | API key used to authenticate requests to the language model through OpenRouter. |
| `CORS_ORIGINS` | Specifies the frontend origin authorized to communicate with the backend. |
| `SITE_URL` | Application URL used as the HTTP Referer header in OpenRouter requests. |
| `SITE_NAME` | Application name used as the Title header in OpenRouter requests. |

**Security Note:** Keep your `.env` file private and never expose your API keys in a public GitHub repository.

---

## 🧠 How It Works — RAG Pipeline

The chatbot relies on a **Retrieval-Augmented Generation (RAG)** architecture to combine semantic information retrieval with the natural language generation capabilities of an LLM.

This approach ensures that club recommendations are grounded in available university club information rather than relying exclusively on the model's pretrained knowledge.

### Step 1 — Data Loading

When the backend starts, club information is loaded from:

`backend/data/clubs.json`

This dataset serves as the knowledge base for the recommendation system.

### Step 2 — Embedding Generation & Vector Storage

Each club description is transformed into a numerical vector representation using a **sentence-transformers** embedding model from Hugging Face.

The generated embeddings are stored in an **in-memory FAISS vector store**, enabling efficient semantic similarity search.

### Step 3 — User Query & Semantic Retrieval

When a student submits a message:

1. The backend processes the user's request and relevant conversation history.
2. FAISS performs semantic similarity search against the stored club embeddings.
3. The system retrieves the club descriptions most relevant to the student's interests and objectives.

Unlike traditional keyword matching, semantic retrieval helps identify meaningful relationships between student preferences and club descriptions.

### Step 4 — Context Augmentation & Response Generation

The retrieved information is combined into a structured prompt containing:

- The student's original query.
- Recent conversation history.
- Relevant club information retrieved from FAISS.
- Specific instructions governing the assistant's behavior and response format.

This enriched prompt is sent to **Mistral 7B through OpenRouter** to generate an informed, context-aware response.

### Step 5 — Personalized Recommendations

The language model returns a structured JSON response based on the conversation context.

Depending on the information available, the chatbot can:

- Ask follow-up questions to better understand the student's preferences.
- Recommend a specific club that matches the student's interests and aspirations.

### Step 6 — Recommendation Visualization

When a club recommendation is generated:

1. The backend processes club compatibility scores.
2. Matplotlib creates a customized bar chart displaying these scores.
3. The generated chart is saved as an image in `backend/static/plots/`.
4. The backend returns the chart URL alongside the chatbot response.
5. The frontend displays the recommendation and its associated visualization.

This provides students with both a conversational explanation and a visual representation of club compatibility.

### RAG Workflow Overview

```text
                  Student Query
                       |
                       v
              FastAPI Backend
                       |
                       v
           Query & Context Processing
                       |
                       v
             Semantic Retrieval
                (FAISS Index)
                       ^
                       |
              Club Embeddings
          (Hugging Face Models)
                       ^
                       |
               clubs.json Dataset
                       |
                       v
             Retrieved Club Data
                       |
                       v
             Prompt Augmentation
          (Query + History + Context)
                       |
                       v
              LLM via OpenRouter
                  (Mistral 7B)
                       |
                       v
              Structured Response
                       |
               +-------+-------+
               |               |
               v               v
        Clarification     Recommendation
          Question              |
                                v
                       Matplotlib Chart
                                |
                                v
                      Response + Plot URL
                                |
                                v
                       React Frontend
```

---

## 🔌 API Endpoints

The FastAPI backend provides REST endpoints for chatbot interaction, club information retrieval, and visualization access.

### `POST /chat`

Main endpoint responsible for conversational interactions and personalized club recommendations.

**Request body:**

```json
{
  "message": "...",
  "session": []
}
```

**Response body:**

```json
{
  "response": "...",
  "recommendation": {},
  "club_scores": {},
  "plot_url": "..."
}
```

The response contains the chatbot's message, recommendation information, club compatibility scores, and the generated visualization URL when applicable.

### `GET /clubs`

Retrieves the list of available student clubs.

**Data source:**

`backend/data/clubs.json`

Returns the stored