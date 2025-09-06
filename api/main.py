from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gemini_client import get_gemini_response
from src.chat_session import ChatSession
from src.tool_executor import execute_tool
from settings import SYSTEM_PROMPT

app = FastAPI(
    title="Gemini AI Agent API",
    description="Um agente de IA inteligente com ferramentas externas",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global chat session
chat_sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    used_tool: bool = False
    tool_name: str = None
    session_id: str

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/", response_model=HealthResponse)
async def root():
    return HealthResponse(
        status="success",
        message="Gemini AI Agent API está funcionando!"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="success",
        message="API saudável e pronta para uso"
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get or create session
        if request.session_id not in chat_sessions:
            chat_sessions[request.session_id] = ChatSession(SYSTEM_PROMPT)
        
        session = chat_sessions[request.session_id]
        session.add_user_message(request.message)
        
        # Get response from Gemini
        response = get_gemini_response(session.get_history())
        
        used_tool = False
        tool_name = None
        
        if response.startswith("TOOL:"):
            # Execute tool
            used_tool = True
            tool_result = execute_tool(response)
            
            # Extract tool name for response
            try:
                _, tool_call = response.split(":", 1)
                tool_name, _, _ = tool_call.strip().partition(":")
                tool_name = tool_name.strip()
            except:
                tool_name = "unknown"
            
            session.add_agent_message(tool_result)
            final_response = f"🔧 O agente decidiu usar uma ferramenta...\n\nResultado da ferramenta:\n{tool_result}"
        else:
            session.add_agent_message(response)
            final_response = response
        
        return ChatResponse(
            response=final_response,
            used_tool=used_tool,
            tool_name=tool_name,
            session_id=request.session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@app.get("/sessions")
async def list_sessions():
    return {"sessions": list(chat_sessions.keys())}

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return {"message": f"Sessão {session_id} removida com sucesso"}
    else:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
