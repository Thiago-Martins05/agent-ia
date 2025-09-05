"""
Command-line interface for the Gemini Agent.
"""
import asyncio
import sys
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.markdown import Markdown
from agent import create_agent
from settings import get_settings, ensure_directories


console = Console()


class CLIManager:
    """Manages the CLI interface."""
    
    def __init__(self):
        self.settings = get_settings()
        self.agent = None
        self.running = False
    
    def initialize(self):
        """Initialize the CLI and agent."""
        try:
            # Ensure directories exist
            ensure_directories()
            
            # Create agent
            self.agent = create_agent()
            
            # Display welcome message
            self.display_welcome()
            
        except Exception as e:
            console.print(f"[red]Error initializing agent: {str(e)}[/red]")
            sys.exit(1)
    
    def display_welcome(self):
        """Display welcome message."""
        welcome_text = f"""
# {self.settings.agent_name}

{self.settings.agent_description}

## Available Commands:
- Type your message and press Enter to chat
- `/help` - Show this help message
- `/info` - Show agent information
- `/history` - Show conversation history
- `/tools` - List available tools
- `/memory` - Show memory information
- `/clear` - Clear conversation history
- `/quit` or `/exit` - Exit the application

## Getting Started:
Just start typing your questions or requests!
        """
        
        console.print(Panel(
            Markdown(welcome_text),
            title="Welcome",
            border_style="blue"
        ))
    
    def display_help(self):
        """Display help information."""
        help_text = """
## Available Commands:

**Chat Commands:**
- Just type your message to start chatting
- The agent will respond using Google Gemini AI

**System Commands:**
- `/help` - Show this help message
- `/info` - Display agent information and status
- `/history [n]` - Show last n conversations (default: 5)
- `/tools` - List all available tools
- `/memory` - Show memory statistics
- `/clear` - Clear current session memory
- `/quit` or `/exit` - Exit the application

**Tool Usage:**
- The agent can use various tools to help you
- Tools include file operations, calculations, web search, etc.
- The agent will automatically use tools when appropriate
        """
        
        console.print(Panel(
            Markdown(help_text),
            title="Help",
            border_style="green"
        ))
    
    def display_agent_info(self):
        """Display agent information."""
        if not self.agent:
            console.print("[red]Agent not initialized[/red]")
            return
        
        info = self.agent.get_agent_info()
        
        info_text = f"""
**Agent Name:** {info['name']}
**Description:** {info['description']}
**Session ID:** {info['session_id']}
**Conversation Count:** {info['conversation_count']}
**Memory Type:** {info['memory_type']}

**Available Tools:**
{', '.join(info['available_tools'])}
        """
        
        console.print(Panel(
            Markdown(info_text),
            title="Agent Information",
            border_style="yellow"
        ))
    
    async def display_history(self, limit: int = 5):
        """Display conversation history."""
        if not self.agent:
            console.print("[red]Agent not initialized[/red]")
            return
        
        history = await self.agent.get_conversation_history(limit=limit)
        
        if not history:
            console.print("[yellow]No conversation history found[/yellow]")
            return
        
        console.print(f"\n[bold]Last {len(history)} conversations:[/bold]")
        
        for i, conv in enumerate(history, 1):
            console.print(f"\n[bold blue]Conversation {i}:[/bold blue]")
            console.print(f"[green]User:[/green] {conv['user_input']}")
            console.print(f"[blue]Agent:[/blue] {conv['agent_response']}")
            console.print(f"[dim]Time: {conv['timestamp']}[/dim]")
    
    def display_tools(self):
        """Display available tools."""
        if not self.agent:
            console.print("[red]Agent not initialized[/red]")
            return
        
        tools = self.agent.tools.list_tools()
        
        tools_text = "**Available Tools:**\n\n"
        for name, description in tools.items():
            tools_text += f"- **{name}**: {description}\n"
        
        console.print(Panel(
            Markdown(tools_text),
            title="Available Tools",
            border_style="cyan"
        ))
    
    async def display_memory_info(self):
        """Display memory information."""
        if not self.agent:
            console.print("[red]Agent not initialized[/red]")
            return
        
        # This would require additional methods in the agent
        console.print("[yellow]Memory information display not yet implemented[/yellow]")
    
    async def clear_memory(self):
        """Clear agent memory."""
        if not self.agent:
            console.print("[red]Agent not initialized[/red]")
            return
        
        confirmed = Prompt.ask(
            "Are you sure you want to clear the memory? This action cannot be undone",
            choices=["y", "n"],
            default="n"
        )
        
        if confirmed.lower() == "y":
            success = await self.agent.clear_memory()
            if success:
                console.print("[green]Memory cleared successfully[/green]")
            else:
                console.print("[red]Failed to clear memory[/red]")
        else:
            console.print("[yellow]Memory clear cancelled[/yellow]")
    
    async def process_command(self, command: str) -> bool:
        """Process a command. Returns True if should continue, False if should exit."""
        command = command.strip()
        
        if not command:
            return True
        
        # Handle system commands
        if command.startswith("/"):
            parts = command.split()
            cmd = parts[0].lower()
            
            if cmd in ["/quit", "/exit"]:
                return False
            elif cmd == "/help":
                self.display_help()
            elif cmd == "/info":
                self.display_agent_info()
            elif cmd == "/history":
                limit = int(parts[1]) if len(parts) > 1 else 5
                await self.display_history(limit)
            elif cmd == "/tools":
                self.display_tools()
            elif cmd == "/memory":
                await self.display_memory_info()
            elif cmd == "/clear":
                await self.clear_memory()
            else:
                console.print(f"[red]Unknown command: {cmd}[/red]")
                console.print("Type `/help` for available commands")
        
        else:
            # Process as regular chat input
            if not self.agent:
                console.print("[red]Agent not initialized[/red]")
                return True
            
            # Show typing indicator
            with console.status("[bold green]Thinking..."):
                response = await self.agent.process_input(command)
            
            # Display response
            console.print(f"\n[bold blue]{self.settings.agent_name}:[/bold blue]")
            console.print(Markdown(response))
        
        return True
    
    async def run(self):
        """Run the CLI interface."""
        self.initialize()
        self.running = True
        
        console.print("\n[bold green]Agent is ready! Type your message or use /help for commands.[/bold green]\n")
        
        try:
            while self.running:
                try:
                    user_input = Prompt.ask("[bold green]You[/bold green]")
                    
                    if not await self.process_command(user_input):
                        break
                        
                except KeyboardInterrupt:
                    console.print("\n[yellow]Use /quit or /exit to properly exit the application[/yellow]")
                except EOFError:
                    break
                except Exception as e:
                    console.print(f"[red]Error: {str(e)}[/red]")
        
        except Exception as e:
            console.print(f"[red]Fatal error: {str(e)}[/red]")
        
        finally:
            console.print("\n[bold blue]Goodbye![/bold blue]")


@click.command()
@click.option("--session-id", help="Use a specific session ID")
def main(session_id: Optional[str] = None):
    """Run the Gemini Agent CLI."""
    cli_manager = CLIManager()
    if session_id:
        cli_manager.agent = create_agent(session_id=session_id)
    
    asyncio.run(cli_manager.run())


if __name__ == "__main__":
    main()
