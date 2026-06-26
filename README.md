END to END rag project# RAG Webpage Chatbot

Chat with any webpage. Paste a URL, ask questions, get answers grounded in that page's content - with memory for follow-up questions.

## How it works
`URL → scrape → chunk → embed (local) → FAISS index → retrieve → LLM generates cited answer`

## Tech stack
LangChain · FAISS · HuggingFace (local embeddings + hosted LLM) · Streamlit

## Setup
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file with your free HuggingFace token:
```
HF_TOKEN=your_token_here
```

## Run
```
streamlit run streamlit.py
```
Paste a URL, click **Ingest URL**, then ask questions in the chat box.

## Limitations
- No caching - re-ingests on every new URL
- Citations are prompt-instructed, not code-enforced
- No automated answer evaluation yet

## License
MIT# RAG Webpage Chatbot

Chat with any webpage. Paste a URL, ask questions, get answers grounded in that page's content - with memory for follow-up questions.

## How it works
`URL → scrape → chunk → embed (local) → FAISS index → retrieve → LLM generates cited answer`

## Tech stack
LangChain · FAISS · HuggingFace (local embeddings + hosted LLM) · Streamlit

## Setup
```
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create a `.env` file with your free HuggingFace token:
```
HF_TOKEN=your_token_here
```

## Run
```
streamlit run streamlit.py
```
Paste a URL, click **Ingest URL**, then ask questions in the chat box.

## Limitations
- No caching - re-ingests on every new URL
- Citations are prompt-instructed, not code-enforced
- No automated answer evaluation yet

