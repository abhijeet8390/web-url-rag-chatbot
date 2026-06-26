# Data Ingestion 

import os 
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint,ChatHuggingFace
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

embadding_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

HF_TOKEN = os.environ.get("HF_TOKEN")
huggingface_repo_id = "Qwen/Qwen2.5-7B-Instruct"

llm = HuggingFaceEndpoint(
    repo_id= huggingface_repo_id,
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.3,
    max_new_tokens=512
)
chat_model = ChatHuggingFace(llm=llm)
## ingester 

def ingest_url(url:str):
    loader = WebBaseLoader(url)
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 600,
        chunk_overlap = 80
    )
    
    chunks = splitter.split_documents(documents)
    
    vectorstore = FAISS.from_documents(chunks,embadding_model)
    
    return vectorstore.as_retriever(search_kwargs = {"k": 3})


# Prompt

def build_prompt(question, retrieved_docs, chat_history):
    
    context = "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}]\n{doc.page_content}"
        for doc in retrieved_docs
    )
    history_text = "\n".join(
        f"User: {q}\nAssistant: {a}" for q, a in chat_history[-3:]
    )
    return f"""You are a helpful assistant. Answer the question using ONLY the context below.
If the answer isn't in the context, say you don't know - do not make things up.
Cite the source URL for any fact you use.
 
Conversation so far:
{history_text}
 
Context:
{context}
 
Question: {question}
Answer:"""
    
    
# chat history 
def main():
    url = input("Enter a URL to chat about: ").strip()
    print("Ingesting... (this may take a moment)")
    retriever = ingest_url(url)
    print("Ready! Ask questions, or type 'exit' to quit.\n")
 
    chat_history = []  
    
    while True:
        question = input("You: ").strip()
        if question.lower() == "exit":
            break
 
        retrieved_docs = retriever.invoke(question)
        prompt = build_prompt(question, retrieved_docs, chat_history)
        response = chat_model.invoke(prompt)
        answer = response.content
 
        print(f"\nBot: {answer}\n")
        chat_history.append((question, answer))
        
if __name__ == "__main__":
    main()
    
