# memory_manager.py
import json
import base64
from datetime import datetime
from github_integration import GitHubManager

class MemoryManager:
    def __init__(self, github_manager=None):
        self.memory_file = "agent_memory.json"
        self.github_manager = github_manager
        self.memory = self.load_memory()
    
    def load_memory(self):
        # Try to load from GitHub first
        if self.github_manager:
            github_memory = self.github_manager.get_file(self.memory_file)
            if github_memory:
                content = base64.b64decode(github_memory['content']).decode('utf-8')
                return json.loads(content)
        
        # Fall back to local file
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            default_memory = {
                "session_history": [],
                "project_status": {},
                "last_commands": [],
                "browser_sessions": [],
                "ai_knowledge_base": []
            }
            self.save_memory(default_memory)
            return default_memory
    
    def save_memory(self, memory_data=None):
        if memory_data is None:
            memory_data = self.memory
        
        # Save locally
        with open(self.memory_file, 'w') as f:
            json.dump(memory_data, f, indent=2)
        
        # Sync to GitHub if available
        if self.github_manager:
            content = json.dumps(memory_data, indent=2)
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            # Check if file exists on GitHub
            existing_file = self.github_manager.get_file(self.memory_file)
            if existing_file:
                self.github_manager.update_file(self.memory_file, encoded_content, 
                                              "Auto-update: Agent memory sync")
            else:
                self.github_manager.create_file(self.memory_file, encoded_content,
                                              "Auto-create: Agent memory initialization")
    
    def add_ai_knowledge(self, knowledge_text):
        """Add to the AI knowledge base for future sessions"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "knowledge": knowledge_text
        }
        self.memory["ai_knowledge_base"].append(entry)
        self.memory["ai_knowledge_base"] = self.memory["ai_knowledge_base"][-100:]  # Keep last 100
        self.save_memory()
    
    def get_recent_knowledge(self):
        """Get recent knowledge for AI context"""
        return self.memory["ai_knowledge_base"][-10:]  # Last 10 knowledge items