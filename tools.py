"""
Tools and utilities for the Gemini Agent.
"""
import json
import asyncio
from typing import Any, Dict, List, Optional, Union
from pathlib import Path
import google.generativeai as genai
from settings import get_settings


class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        self.tools: Dict[str, callable] = {}
        self._register_default_tools()
    
    def register(self, name: str, func: callable, description: str = ""):
        """Register a new tool."""
        self.tools[name] = {
            'function': func,
            'description': description
        }
    
    def get_tool(self, name: str) -> Optional[callable]:
        """Get a tool by name."""
        tool = self.tools.get(name)
        return tool['function'] if tool else None
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools with descriptions."""
        return {name: tool['description'] for name, tool in self.tools.items()}
    
    def _register_default_tools(self):
        """Register default tools."""
        self.register("file_read", self._file_read, "Read contents of a file")
        self.register("file_write", self._file_write, "Write content to a file")
        self.register("file_list", self._file_list, "List files in a directory")
        self.register("web_search", self._web_search, "Search the web for information")
        self.register("calculate", self._calculate, "Perform mathematical calculations")
        self.register("get_time", self._get_time, "Get current date and time")
    
    async def _file_read(self, file_path: str) -> str:
        """Read file contents."""
        try:
            path = Path(file_path)
            if not path.exists():
                return f"Error: File '{file_path}' does not exist"
            return path.read_text(encoding='utf-8')
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    async def _file_write(self, file_path: str, content: str) -> str:
        """Write content to file."""
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            return f"Successfully wrote to '{file_path}'"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    async def _file_list(self, directory: str = ".") -> str:
        """List files in directory."""
        try:
            path = Path(directory)
            if not path.exists():
                return f"Error: Directory '{directory}' does not exist"
            
            files = []
            for item in path.iterdir():
                files.append(f"{'[DIR]' if item.is_dir() else '[FILE]'} {item.name}")
            
            return "\n".join(files) if files else "Directory is empty"
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    async def _web_search(self, query: str) -> str:
        """Search the web (placeholder implementation)."""
        # This is a placeholder - in a real implementation, you'd use
        # a web search API like Google Search API, Bing API, etc.
        return f"Web search results for: '{query}'\n[This is a placeholder implementation]"
    
    async def _calculate(self, expression: str) -> str:
        """Perform mathematical calculations."""
        try:
            # Simple and safe evaluation for basic math
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid characters in expression"
            
            result = eval(expression)
            return f"Result: {result}"
        except Exception as e:
            return f"Error calculating: {str(e)}"
    
    async def _get_time(self) -> str:
        """Get current date and time."""
        from datetime import datetime
        return f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


class GeminiClient:
    """Client for interacting with Google Gemini API."""
    
    def __init__(self):
        self.settings = get_settings()
        self.model = None
        self._initialize()
    
    def _initialize(self):
        """Initialize the Gemini client."""
        try:
            genai.configure(api_key=self.settings.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            raise Exception(f"Failed to initialize Gemini client: {str(e)}")
    
    async def generate_response(
        self, 
        prompt: str, 
        tools: Optional[ToolRegistry] = None,
        context: Optional[str] = None
    ) -> str:
        """Generate a response using Gemini."""
        try:
            # Build the full prompt with context
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nPrompt: {prompt}"
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    async def generate_with_tools(
        self, 
        prompt: str, 
        tools: ToolRegistry,
        context: Optional[str] = None
    ) -> str:
        """Generate response with tool usage capability."""
        try:
            # This is a simplified implementation
            # In a real scenario, you'd need to implement proper tool calling
            # with the Gemini API
            
            response = await self.generate_response(prompt, tools, context)
            
            # Check if the response mentions any tools
            available_tools = tools.list_tools()
            for tool_name in available_tools.keys():
                if f"use {tool_name}" in response.lower() or f"call {tool_name}" in response.lower():
                    # Extract tool call from response (simplified)
                    # In practice, you'd need more sophisticated parsing
                    pass
            
            return response
        except Exception as e:
            return f"Error generating response with tools: {str(e)}"


# Global instances
tool_registry = ToolRegistry()
gemini_client = GeminiClient()
