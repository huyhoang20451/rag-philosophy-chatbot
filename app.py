import os
import uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI  # Sử dụng để kết nối API cục bộ
from langchain.schema import SystemMessage, HumanMessage
from config import CHATBOT_CONFIGS

load_dotenv()

app = FastAPI(title="RAG Philosophy Chatbot - Llama.cpp Server Version")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# -------------------------------------------------------------
# KẾT NỐI ĐẾN CỔNG LLAMA.CPP SERVER ĐANG CHẠY QWEN 2.5
# -------------------------------------------------------------
# Thay đổi URL bên dưới nếu bạn mở cổng khác (ví dụ: http://localhost:8080/v1)
LLAMACPP_API_URL = "http://localhost:8080/v1" 

print(f"🔗 Đang kết nối tới cổng llama.cpp tại: {LLAMACPP_API_URL}...")
llm = ChatOpenAI(
    openai_api_base=LLAMACPP_API_URL,
    openai_api_key="not-needed-for-local", # Thao tác giả lập OpenAI format
    model_name="qwen2.5-1.5b",             # Tên định danh mô hình
    temperature=0.5,
    max_tokens=512
)
print("✅ Kết nối cổng dịch vụ LLM hoàn tất!")

# Khởi tạo Embeddings cho RAG
embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
retrievers = {}

def create_retriever_from_text(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk, metadata={}) for chunk in chunks]
    ids = [str(uuid.uuid4()) for _ in docs]
    vectorstore = FAISS.from_documents(docs, embeddings_model, ids=ids)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

@app.on_event("startup")
def startup_event():
    print("⏳ Đang khởi tạo cơ sở dữ liệu triết học (RAG)...")
    for school_key, config in CHATBOT_CONFIGS.items():
        retrievers[school_key] = create_retriever_from_text(config['text_data'])
    print("✅ Khởi tạo RAG hoàn tất!")

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    conversation: List[Message]
    school: str = 'khacky'

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask(data: ChatRequest):
    if not data.conversation:
        raise HTTPException(status_code=400, detail="Dữ liệu hội thoại không hợp lệ")

    try:
        question = data.conversation[-1].content
        recent_conversation = data.conversation[-3:] if len(data.conversation) > 3 else data.conversation
        context_text = "\n".join([f"{c.role}: {c.content}" for c in recent_conversation])
        
        config = CHATBOT_CONFIGS.get(data.school, CHATBOT_CONFIGS['khacky'])
        retriever = retrievers.get(data.school, retrievers['khacky'])
        
        retrieved_docs = retriever.invoke(question)
        docs_text = "\n\n".join([f"Doc {i+1}: {doc.page_content}" for i, doc in enumerate(retrieved_docs[:2])])
        
        # Vì ChatOpenAI tự động đóng gói Prompt theo chuẩn ChatML (system/user/assistant) của Qwen,
        # chúng ta chỉ cần truyền cấu trúc tin nhắn sạch sẽ như thế này:
        system_prompt = f"""Bạn là một triết gia đại diện cho trường phái {config['school_name']}.
Yêu cầu: {config['additional_instructions']}
Đối tượng người nghe: Sinh viên năm 4 Đại học FPT trong kỷ nguyên AI.
Quy tắc: Ngắn gọn (2-3 đoạn văn), không tự ý trích dẫn nguồn (như Doc 1, Doc 2), ngôn ngữ đơn giản, bám sát tư tưởng trường phái.

[Ngữ cảnh triết học để bạn tham khảo]:
{docs_text}

[Lịch sử trò chuyện gần đây]:
{context_text}"""

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question)
        ]
        
        # Gọi API bất đồng bộ tới server llama.cpp
        answer = await llm.ainvoke(messages)
        
        return {"answer": answer.content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)