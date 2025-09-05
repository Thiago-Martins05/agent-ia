"""
Main agent implementation for the Gemini Agent.
"""
import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from tools import tool_registry, gemini_client
from memory import memory_manager
from settings import get_settings


class GeminiAgent:
    """Main agent class that orchestrates all components."""
    
    def __init__(self, session_id: Optional[str] = None):
        self.settings = get_settings()
        self.session_id = session_id or str(uuid.uuid4())
        self.tools = tool_registry
        self.memory = memory_manager
        self.client = gemini_client
        self.conversation_count = 0
        
        # Initialize agent
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize the agent with basic knowledge."""
        try:
            # Store agent information in memory
            self.memory.store_memory(
                key="agent_info",
                value={
                    "name": self.settings.agent_name,
                    "description": self.settings.agent_description,
                    "session_id": self.session_id,
                    "created_at": datetime.now().isoformat()
                },
                memory_type="system"
            )
            
            # Store available tools
            self.memory.store_memory(
                key="available_tools",
                value=list(self.tools.list_tools().keys()),
                memory_type="system"
            )
            
        except Exception as e:
            print(f"Warning: Failed to initialize agent memory: {str(e)}")
    
    async def process_input(
        self, 
        user_input: str, 
        context: Optional[str] = None
    ) -> str:
        """Process user input and generate response."""
        try:
            self.conversation_count += 1
            
            # Get relevant context
            session_context = self.memory.get_context_for_session(self.session_id)
            full_context = f"{session_context}\n{context}" if context else session_context
            
            # Generate response using Gemini
            response = await self.client.generate_response(
                prompt=user_input,
                context=full_context
            )
            
            # Store conversation in memory
            self.memory.store_conversation(
                session_id=self.session_id,
                user_input=user_input,
                agent_response=response,
                context=full_context,
                metadata={
                    "conversation_count": self.conversation_count,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            return response
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            
            # Store error in memory
            self.memory.store_conversation(
                session_id=self.session_id,
                user_input=user_input,
                agent_response=error_response,
                context=context,
                metadata={
                    "error": True,
                    "error_message": str(e),
                    "conversation_count": self.conversation_count
                }
            )
            
            return error_response
    
    async def process_with_tools(
        self, 
        user_input: str, 
        context: Optional[str] = None
    ) -> str:
        """Process input with tool usage capability."""
        try:
            self.conversation_count += 1
            
            # Get relevant context
            session_context = self.memory.get_context_for_session(self.session_id)
            full_context = f"{session_context}\n{context}" if context else session_context
            
            # Generate response with tools
            response = await self.client.generate_with_tools(
                prompt=user_input,
                tools=self.tools,
                context=full_context
            )
            
            # Store conversation in memory
            self.memory.store_conversation(
                session_id=self.session_id,
                user_input=user_input,
                agent_response=response,
                context=full_context,
                metadata={
                    "conversation_count": self.conversation_count,
                    "used_tools": True,
                    "timestamp": datetime.now().isoformat()
                }
            )
            
            return response
            
        except Exception as e:
            error_response = f"I apologize, but I encountered an error: {str(e)}"
            
            # Store error in memory
            self.memory.store_conversation(
                session_id=self.session_id,
                user_input=user_input,
                agent_response=error_response,
                context=context,
                metadata={
                    "error": True,
                    "error_message": str(e),
                    "conversation_count": self.conversation_count
                }
            )
            
            return error_response
    
    async def add_knowledge(
        self, 
        topic: str, 
        content: str, 
        source: Optional[str] = None,
        confidence: float = 1.0
    ) -> bool:
        """Add knowledge to the agent's knowledge base."""
        try:
            self.memory.store_knowledge(
                topic=topic,
                content=content,
                source=source,
                confidence=confidence,
                metadata={
                    "added_by": "agent",
                    "session_id": self.session_id,
                    "timestamp": datetime.now().isoformat()
                }
            )
            return True
        except Exception as e:
            print(f"Failed to add knowledge: {str(e)}")
            return False
    
    async def search_knowledge(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search the agent's knowledge base."""
        try:
            return self.memory.search_knowledge(query, limit=limit)
        except Exception as e:
            print(f"Failed to search knowledge: {str(e)}")
            return []
    
    async def get_conversation_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for the current session."""
        try:
            return self.memory.get_conversation_history(self.session_id, limit=limit)
        except Exception as e:
            print(f"Failed to get conversation history: {str(e)}")
            return []
    
    async def clear_memory(self, memory_type: Optional[str] = None) -> bool:
        """Clear agent memory (use with caution)."""
        try:
            if memory_type:
                # Clear specific memory type
                # This would require additional implementation in MemoryManager
                pass
            else:
                # Clear all memory for this session
                # This would require additional implementation in MemoryManager
                pass
            return True
        except Exception as e:
            print(f"Failed to clear memory: {str(e)}")
            return False
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agent."""
        return {
            "name": self.settings.agent_name,
            "description": self.settings.agent_description,
            "session_id": self.session_id,
            "conversation_count": self.conversation_count,
            "available_tools": list(self.tools.list_tools().keys()),
            "memory_type": self.settings.memory_type
        }
    
    async def execute_tool(self, tool_name: str, *args, **kwargs) -> str:
        """Execute a specific tool."""
        try:
            tool_func = self.tools.get_tool(tool_name)
            if not tool_func:
                return f"Tool '{tool_name}' not found"
            
            result = await tool_func(*args, **kwargs)
            return result
        except Exception as e:
            return f"Error executing tool '{tool_name}': {str(e)}"


# Factory function for creating agents
def create_agent(session_id: Optional[str] = None) -> GeminiAgent:
    """Create a new Gemini agent instance."""
    return GeminiAgent(session_id=session_id)
