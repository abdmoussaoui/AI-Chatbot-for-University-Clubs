# FSBM Club Advisor Chatbot

Welcome to the FSBM Club Advisor Chatbot! This is an intelligent, conversational agent designed to help students at the Faculty of Sciences Ben M'sik (FSBM) discover the perfect student club based on their interests, skills, and aspirations.

The application features a modern React/TypeScript frontend and a powerful Python/FastAPI backend that leverages a Retrieval-Augmented Generation (RAG) architecture to provide accurate and personalized recommendations.

## Features

- **Conversational AI**: Understands natural language to identify user interests and goals.
- **Personalized Recommendations**: Suggests the most suitable club from a predefined list.
- **RAG Architecture**: Provides responses based on factual club data (`clubs.json`) to avoid hallucinations and ensure accuracy.
- **Dynamic Visualization**: Generates a custom bar chart to visually represent club compatibility scores after a recommendation is made.
- **Interactive & Responsive UI**: A clean and modern chat interface built with React and TypeScript.
- **Full-stack Application**: A clear separation between the frontend and backend services.

## Project Structure

The project is organized into two main directories:

```bash
├── backend/ # FastAPI application (Python)
│ ├── data/
│ │ └── clubs.json
│ ├── static/
│ │ └── plots/
│ ├── main.py
│ ├── rag_chain.py
│ ├── visualization.py
│ ├── requirements.txt
│ └── .env
└── frontend/ # React + TypeScript application
├── src/
├── package.json
└── ...
```

## Tech Stack

### Backend

- **Framework**: **FastAPI**
- **Language**: **Python 3.9+**
- **AI & Machine Learning**:
  - **LangChain**: For orchestrating the RAG pipeline.
  - **OpenRouter**: To access LLMs like Mistral 7B for generation.
  - **Hugging Face**: For `sentence-transformers` embeddings.
  - **FAISS**: For efficient similarity search in the vector store.
- **Data Visualization**: **Matplotlib**
- **Web Server**: **Uvicorn**

### Frontend

- **Framework**: **React**
- **Language**: **TypeScript**
- **Build Tool**: **Vite**
- **Styling**: **Tailwind CSS**
- **API Communication**: **Axios**

## Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

- **Node.js** (v18 or later) and **npm**
- **Python** (v3.9 or later) and **pip**
- A free **OpenRouter API Key** from [openrouter.ai](https://openrouter.ai).

---

### 1. Backend Setup (Python)

First, set up and run the backend server.

```bash
# 1. Navigate to the backend directory

cd backend

# 2. Create and activate a virtual environment

# On Windows

python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux

python3 -m venv venv
source venv/bin/activate

# 3. Install the required Python packages from requirements.txt

pip install -r requirements.txt

# 4. Create a .env file in the `backend` directory

touch .env

# 5. Add your environment variables to the .env file

# See the "Environment Variables" section below for the content.
```

Now, run the backend server:

# Start the FastAPI server with auto-reload

```bash
uvicorn main:app --reload
```

The backend API will be available at http://127.0.0.1:8000. The server will automatically load all necessary models on startup.

### 2. Frontend Setup (React + TypeScript)

In a new terminal window, set up and run the frontend application.

```bash
# 1. Navigate to the frontend directory from the project root

cd frontend

# 2. Install the required npm packages

npm install --legacy-peer-deps

# 3. Start the frontend development server

npm run dev
```

The frontend application will be available at http://localhost:5173. Open this URL in your browser to start chatting!

## Environment Variables

The backend requires a .env file for configuration. Create a file named .env inside the backend directory and add the following content:

# Your API key from https://openrouter.ai

OPENROUTER_API_KEY="your_openrouter_api_key"

# The URL of your frontend application for CORS policy

CORS_ORIGINS="http://localhost:5173"

# Required for OpenRouter API requests (as per their policy)

# You can leave these as default for local development

SITE_URL="http://localhost:8000"
SITE_NAME="FSBM Club Assistant"

- **OPENROUTER_API_KEY**: Required. Your unique API key to use the language model.
- **CORS_ORIGINS**: Required. The URL where your frontend is running. This allows the frontend to make requests to the backend.
- **SITE_URL & SITE_NAME**: Used as HTTP Referer and Title headers in API calls to OpenRouter.

## How It Works: The RAG Architecture

The chatbot uses a Retrieval-Augmented Generation (RAG) pipeline to provide intelligent and context-aware responses.

- **Data Loading**: At startup, the server loads club information from `backend/data/clubs.json`.
- **Vectorization**: The description of each club is converted into a numerical vector (embedding) using a `sentence-transformers` model from Hugging Face. These vectors are stored in a FAISS in-memory vector store for fast retrieval.
- **User Query & Retrieval**: When a user sends a message, the backend searches the FAISS vector store to find the clubs whose descriptions are most semantically similar to the user's query and conversation history.
- **Augmentation & Generation**: A detailed prompt is constructed containing:
  - The user's original query.
  - The recent conversation history.
  - The retrieved club data (the "augmented" context).
  - Specific instructions on how to behave and format the output.
  - This complete prompt is sent to the Mistral 7B model via OpenRouter.
- **Response & Visualization**:
  - The LLM returns a structured JSON response, either asking a clarifying question or recommending a specific club.
  - If a recommendation is made, the backend uses Matplotlib to generate a bar chart showing compatibility scores. This chart is saved as an image, and its URL is sent to the frontend along with the text response.

## API Endpoints

The backend exposes the following API endpoints:

- **POST /chat**
  - The main endpoint for interacting with the chatbot.
  - **Request Body**: `{ "message": "...", "session": [...] }`
  - **Response Body**: `{ "response": "...", "recommendation": {...}, "club_scores": {...}, "plot_url": "..." }`
- **GET /clubs**
  - Returns a JSON list of all available clubs from `clubs.json`.
- **GET /static/plots/{plot_name}.png**
  - Serves the generated recommendation plot images.
# AI-Chatbot-for-University-Clubs
