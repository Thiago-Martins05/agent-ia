"""
Memory management for the Gemini Agent.
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from settings import get_settings


class MemoryManager:
    """Manages agent memory using SQLite database."""
    
    def __init__(self):
        self.settings = get_settings()
        self.db_path = self.settings.memory_path / "agent_memory.db"
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the memory database."""
        try:
            # Ensure memory directory exists
            self.settings.memory_path.mkdir(parents=True, exist_ok=True)
            
            # Create database connection
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create conversations table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        user_input TEXT NOT NULL,
                        agent_response TEXT NOT NULL,
                        context TEXT,
                        metadata TEXT
                    )
                """)
                
                # Create memories table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        key TEXT UNIQUE NOT NULL,
                        value TEXT NOT NULL,
                        memory_type TEXT DEFAULT 'general',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                """)
                
                # Create knowledge base table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS knowledge_base (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT NOT NULL,
                        content TEXT NOT NULL,
                        source TEXT,
                        confidence REAL DEFAULT 1.0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        metadata TEXT
                    )
                """)
                
                conn.commit()
        except Exception as e:
            raise Exception(f"Failed to initialize memory database: {str(e)}")
    
    def store_conversation(
        self, 
        session_id: str, 
        user_input: str, 
        agent_response: str,
        context: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Store a conversation exchange."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversations 
                    (session_id, user_input, agent_response, context, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    session_id,
                    user_input,
                    agent_response,
                    context,
                    json.dumps(metadata) if metadata else None
                ))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            raise Exception(f"Failed to store conversation: {str(e)}")
    
    def get_conversation_history(
        self, 
        session_id: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, timestamp, user_input, agent_response, context, metadata
                    FROM conversations 
                    WHERE session_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                """, (session_id, limit))
                
                rows = cursor.fetchall()
                return [
                    {
                        'id': row[0],
                        'timestamp': row[1],
                        'user_input': row[2],
                        'agent_response': row[3],
                        'context': row[4],
                        'metadata': json.loads(row[5]) if row[5] else None
                    }
                    for row in rows
                ]
        except Exception as e:
            raise Exception(f"Failed to get conversation history: {str(e)}")
    
    def store_memory(
        self, 
        key: str, 
        value: Any, 
        memory_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Store a memory item."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO memories 
                    (key, value, memory_type, metadata, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    key,
                    json.dumps(value),
                    memory_type,
                    json.dumps(metadata) if metadata else None
                ))
                conn.commit()
                return True
        except Exception as e:
            raise Exception(f"Failed to store memory: {str(e)}")
    
    def get_memory(self, key: str) -> Optional[Any]:
        """Get a memory item by key."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT value FROM memories WHERE key = ?
                """, (key,))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row[0])
                return None
        except Exception as e:
            raise Exception(f"Failed to get memory: {str(e)}")
    
    def search_memories(
        self, 
        query: str, 
        memory_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search memories by content."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type:
                    cursor.execute("""
                        SELECT key, value, memory_type, created_at, metadata
                        FROM memories 
                        WHERE (key LIKE ? OR value LIKE ?) AND memory_type = ?
                        ORDER BY created_at DESC 
                        LIMIT ?
                    """, (f"%{query}%", f"%{query}%", memory_type, limit))
                else:
                    cursor.execute("""
                        SELECT key, value, memory_type, created_at, metadata
                        FROM memories 
                        WHERE key LIKE ? OR value LIKE ?
                        ORDER BY created_at DESC 
                        LIMIT ?
                    """, (f"%{query}%", f"%{query}%", limit))
                
                rows = cursor.fetchall()
                return [
                    {
                        'key': row[0],
                        'value': json.loads(row[1]),
                        'memory_type': row[2],
                        'created_at': row[3],
                        'metadata': json.loads(row[4]) if row[4] else None
                    }
                    for row in rows
                ]
        except Exception as e:
            raise Exception(f"Failed to search memories: {str(e)}")
    
    def store_knowledge(
        self, 
        topic: str, 
        content: str, 
        source: Optional[str] = None,
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Store knowledge in the knowledge base."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO knowledge_base 
                    (topic, content, source, confidence, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    topic,
                    content,
                    source,
                    confidence,
                    json.dumps(metadata) if metadata else None
                ))
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            raise Exception(f"Failed to store knowledge: {str(e)}")
    
    def search_knowledge(
        self, 
        query: str, 
        min_confidence: float = 0.0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search knowledge base."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, topic, content, source, confidence, created_at, metadata
                    FROM knowledge_base 
                    WHERE (topic LIKE ? OR content LIKE ?) AND confidence >= ?
                    ORDER BY confidence DESC, created_at DESC 
                    LIMIT ?
                """, (f"%{query}%", f"%{query}%", min_confidence, limit))
                
                rows = cursor.fetchall()
                return [
                    {
                        'id': row[0],
                        'topic': row[1],
                        'content': row[2],
                        'source': row[3],
                        'confidence': row[4],
                        'created_at': row[5],
                        'metadata': json.loads(row[6]) if row[6] else None
                    }
                    for row in rows
                ]
        except Exception as e:
            raise Exception(f"Failed to search knowledge: {str(e)}")
    
    def get_context_for_session(
        self, 
        session_id: str, 
        max_context_length: int = 2000
    ) -> str:
        """Get relevant context for a session."""
        try:
            # Get recent conversation history
            history = self.get_conversation_history(session_id, limit=5)
            
            # Get relevant memories
            memories = self.search_memories(session_id, limit=3)
            
            # Build context string
            context_parts = []
            
            if history:
                context_parts.append("Recent conversation:")
                for conv in reversed(history):  # Most recent first
                    context_parts.append(f"User: {conv['user_input']}")
                    context_parts.append(f"Agent: {conv['agent_response']}")
            
            if memories:
                context_parts.append("\nRelevant memories:")
                for memory in memories:
                    context_parts.append(f"- {memory['key']}: {memory['value']}")
            
            context = "\n".join(context_parts)
            
            # Truncate if too long
            if len(context) > max_context_length:
                context = context[:max_context_length] + "..."
            
            return context
        except Exception as e:
            return f"Error building context: {str(e)}"


# Global memory manager instance
memory_manager = MemoryManager()
