import os
from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
GROQ_API_KEY=os.getenv("GROQ_API_KEY")
client=Groq(api_key=GROQ_API_KEY)
@st.cache_resource
def build_vectorstore_cached(chunks):
    if not chunks:
        return None
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(chunks, embeddings)
if GROQ_API_KEY is None:
        st.error("GROQ_API_KEY not found. Check your .env file.")
        st.stop()
def load_pdf(pdf_files):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_files.read())
        temp_file_path = tmp_file.name
    loader= PyPDFLoader(temp_file_path)
    documents=loader.load()
    for doc in documents:
        doc.metadata["source"]=pdf_files.name
    os.remove(temp_file_path)
    return documents
def chunk_docs(documents):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=100 )
    chunks=text_splitter.split_documents(documents)
    return chunks
def build_vectorstore(chunks):
    embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore=FAISS.from_documents(chunks,embeddings)
    return vectorstore
def context_builder(docs):
    return "\n\n".join([doc.page_content for doc in docs])
def generate_ans(context,test_query,client):
    chat_context=format_chat_history(st.session_state.chat_history)
    prompt= f"""
    You are an expert technical explainer.
    conversation so far:
    {chat_context}
    Your task is to answer the question using ONLY the information provided in the context,
    but you are allowed to:
    - Paraphrase the content
    - Summarize across multiple parts of the context
    - Explain concepts in clear, natural language

    Rules:
    - Do NOT add facts that are not supported by the context.
    - Do NOT use outside knowledge.
    -Use ONLY the document context for factual answers.
    - If the answer cannot be inferred from the context, say: "Not found in the document."

        Answer style:
    - Write in a natural, conversational tone.
    - Use 3–5 complete sentences.
    - Start with a direct answer, then explain.
    Context: {context}
    Question: {test_query}
    """
    
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role":"user","content":prompt}

        ],
        temperature=0.4
    )
    answer=response.choices[0].message.content
    return answer
def format_chat_history(chat_history):
    formatted=""
    for msg in chat_history:
        formatted+=f"{msg['role'].capitalize()}: {msg['content']}\n"
    return formatted

if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]
if "conversations" not in st.session_state:
    st.session_state.conversations=[[]]
if "active_chat_index" not in st.session_state:
    st.session_state.active_chat_index=0


st.markdown("""
# 📄 Document Intelligence Assistant
### AI-powered PDF analysis, comparison, and information extraction
""")
st.markdown("""
<style>
.block-container {
    max-width: 900px;
}
</style>
""", unsafe_allow_html=True)
st.caption("Upload PDFs once. Chats stay separate. Ask focused questions.")
st.divider()
pdf_files=st.file_uploader("Upload one or more PDF files", type="pdf",accept_multiple_files=True)
with st.sidebar:
    st.header("💬 Chats")

    for i, chat in enumerate(st.session_state.conversations):
        is_active = i == st.session_state.active_chat_index
        label = f" -> Chat {i+1}" if is_active else f"chat {i+1}"
        if st.button(label, key=f"chat_{i}"):
            st.session_state.active_chat_index = i
            st.rerun()

    st.divider()

    if st.button("➕ New Chat"):
        st.session_state.conversations.append([])
        st.session_state.active_chat_index = len(st.session_state.conversations) - 1
        st.rerun()
active_chat=st.session_state.conversations[st.session_state.active_chat_index]
for msg in active_chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
MAX_TURNS = 6  # 6 user + 6 assistant messages
st.session_state.chat_history = st.session_state.chat_history[-2*MAX_TURNS:]
if pdf_files is None:
    st.warning("Please upload a PDF file.")
    st.stop()
documents=[]
for pdf in pdf_files:
    docs=load_pdf(pdf)
    documents.extend(docs)
if len(documents) == 0:
    st.info("Upload PDF files to start chatting.")
    st.stop()
chunks=chunk_docs(documents)
if len(chunks) == 0:
    st.warning("No text chunks created from PDFs.")
    st.stop()
vectorstore=build_vectorstore_cached(chunks)
if vectorstore is None:
    st.stop()
#st.success(f"split into {len(chunks)} chunks")
#st.success("Created retriver")
test_query=st.chat_input("Ask a question about the document: ")
if test_query is None or test_query.strip()=="":
    st.stop()


retriever=vectorstore.as_retriever(search_kwargs={"k":3})
docs=retriever.invoke(test_query)
sources=[]
for doc in docs:
    source=doc.metadata.get("source","Unknown file")
    page=doc.metadata.get("page","unknown page")
    sources.append((source,page))
sources=list(set(sources))
#st.write("Retrieved chunks: ",len(docs))
#st.write(docs[0].page_content[:300])
context= context_builder(docs)

# Show user message immediately
with st.chat_message("user"):
    st.write(test_query)

# Generate answer
with st.spinner("Analyzing document... ⏳ (~3 seconds)"):
    answer = generate_ans(context, test_query, client)
active_chat.append({"role": "user", "content": test_query})
active_chat.append({"role": "assistant", "content": answer})
# Show assistant message
with st.chat_message("assistant"):
    st.write(answer)
st.session_state.chat_history.append(
    {"role":"user","content": test_query}
)
st.session_state.chat_history.append(
    {"role":"assistant","content":answer}
)
with st.expander("Sources"):
    for source, page in sources:
        st.write(f"- {source}, page {page}")
#,placeholder="E.g. What is the architecture proposed in the paper? discussed in the document"