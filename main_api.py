"""
FastAPI web interface for the Gemini Agent.
"""
import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent import create_agent
from settings import get_settings, ensure_directories


# Initialize FastAPI app
app = FastAPI(
    title="Gemini Agent API",
    description="An intelligent agent powered by Google Gemini",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global settings
settings = get_settings()

# Pydantic models for API requests/responses
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[str] = None
    use_tools: bool = True

class ChatResponse(BaseModel):
    response: str
    session_id: str
    conversation_count: int
    timestamp: str
    used_tools: bool = False

class AgentInfoResponse(BaseModel):
    name: str
    description: str
    session_id: str
    conversation_count: int
    available_tools: List[str]
    memory_type: str

class ConversationHistoryResponse(BaseModel):
    conversations: List[Dict[str, Any]]
    total_count: int

class KnowledgeRequest(BaseModel):
    topic: str
    content: str
    source: Optional[str] = None
    confidence: float = 1.0

class KnowledgeResponse(BaseModel):
    success: bool
    message: str
    knowledge_id: Optional[int] = None

class SearchRequest(BaseModel):
    query: str
    limit: int = 5

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total_found: int

# Store active agents by session ID
active_agents: Dict[str, Any] = {}


def get_or_create_agent(session_id: Optional[str] = None):
    """Get existing agent or create new one."""
    if not session_id:
        session_id = str(uuid.uuid4())
    
    if session_id not in active_agents:
        active_agents[session_id] = create_agent(session_id=session_id)
    
    return active_agents[session_id], session_id


@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    try:
        ensure_directories()
        print(f"Gemini Agent API started on {settings.api_host}:{settings.api_port}")
    except Exception as e:
        print(f"Error during startup: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with basic API information."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gemini Agent API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .container { max-width: 800px; margin: 0 auto; }
            .endpoint { background: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 5px; }
            .method { font-weight: bold; color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Gemini Agent API</h1>
            <p>An intelligent agent powered by Google Gemini</p>
            
            <h2>Available Endpoints:</h2>
            
            <div class="endpoint">
                <span class="method">POST</span> /chat - Send a message to the agent
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /agent/info - Get agent information
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /agent/info/{session_id} - Get agent info for specific session
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /conversation/history/{session_id} - Get conversation history
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> /knowledge/add - Add knowledge to the agent
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span> /knowledge/search - Search knowledge base
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> /docs - Interactive API documentation
            </div>
            
            <h2>Usage Example:</h2>
            <pre>
curl -X POST "http://localhost:8000/chat" \\
     -H "Content-Type: application/json" \\
     -d '{"message": "Hello, how are you?"}'
            </pre>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message to the agent and get a response."""
    try:
        agent, session_id = get_or_create_agent(request.session_id)
        
        # Process the message
        if request.use_tools:
            response = await agent.process_with_tools(
                user_input=request.message,
                context=request.context
            )
        else:
            response = await agent.process_input(
                user_input=request.message,
                context=request.context
            )
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            conversation_count=agent.conversation_count,
            timestamp=datetime.now().isoformat(),
            used_tools=request.use_tools
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agent/info", response_model=AgentInfoResponse)
async def get_agent_info():
    """Get general agent information."""
    try:
        agent, session_id = get_or_create_agent()
        info = agent.get_agent_info()
        
        return AgentInfoResponse(
            name=info["name"],
            description=info["description"],
            session_id=session_id,
            conversation_count=info["conversation_count"],
            available_tools=info["available_tools"],
            memory_type=info["memory_type"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agent/info/{session_id}", response_model=AgentInfoResponse)
async def get_agent_info_by_session(session_id: str):
    """Get agent information for a specific session."""
    try:
        agent, session_id = get_or_create_agent(session_id)
        info = agent.get_agent_info()
        
        return AgentInfoResponse(
            name=info["name"],
            description=info["description"],
            session_id=session_id,
            conversation_count=info["conversation_count"],
            available_tools=info["available_tools"],
            memory_type=info["memory_type"]
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/conversation/history/{session_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(session_id: str, limit: int = 10):
    """Get conversation history for a session."""
    try:
        agent, _ = get_or_create_agent(session_id)
        history = await agent.get_conversation_history(limit=limit)
        
        return ConversationHistoryResponse(
            conversations=history,
            total_count=len(history)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/knowledge/add", response_model=KnowledgeResponse)
async def add_knowledge(request: KnowledgeRequest):
    """Add knowledge to the agent's knowledge base."""
    try:
        agent, session_id = get_or_create_agent()
        
        success = await agent.add_knowledge(
            topic=request.topic,
            content=request.content,
            source=request.source,
            confidence=request.confidence
        )
        
        if success:
            return KnowledgeResponse(
                success=True,
                message="Knowledge added successfully",
                knowledge_id=1  # This would be the actual ID in a real implementation
            )
        else:
            return KnowledgeResponse(
                success=False,
                message="Failed to add knowledge"
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/knowledge/search", response_model=SearchResponse)
async def search_knowledge(request: SearchRequest):
    """Search the agent's knowledge base."""
    try:
        agent, _ = get_or_create_agent()
        results = await agent.search_knowledge(request.query, limit=request.limit)
        
        return SearchResponse(
            results=results,
            total_found=len(results)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tools")
async def list_tools():
    """List all available tools."""
    try:
        agent, _ = get_or_create_agent()
        tools = agent.tools.list_tools()
        
        return {
            "tools": tools,
            "total_count": len(tools)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/execute")
async def execute_tool(tool_name: str, args: List[Any] = None, kwargs: Dict[str, Any] = None):
    """Execute a specific tool."""
    try:
        agent, _ = get_or_create_agent()
        
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        
        result = await agent.execute_tool(tool_name, *args, **kwargs)
        
        return {
            "tool_name": tool_name,
            "result": result,
            "success": True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main_api:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
