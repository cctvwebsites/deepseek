# ultimate_agent.py
import os
import json
import subprocess
from pathlib import Path
from memory_manager import MemoryManager
from github_integration import GitHubManager

class UltimateAgent:
    def __init__(self):
        # Load config first
        self.config = self.load_config()
        
        # Setup GitHub integration
        self.github_manager = None
        if all(k in self.config for k in ['GITHUB_TOKEN', 'GITHUB_REPO_OWNER', 'GITHUB_REPO_NAME']):
            self.github_manager = GitHubManager(
                self.config['GITHUB_TOKEN'],
                self.config['GITHUB_REPO_OWNER'],
                self.config['GITHUB_REPO_NAME']
            )
        
        # Setup memory with GitHub integration
        self.memory = MemoryManager(self.github_manager)
        
        # Learn from previous sessions
        self.learn_from_memory()
        
        print("🤖 Self-Learning AI Agent Initialized!")
        print(f"📁 Working directory: {os.getcwd()}")
        print(f"💾 Memory: {'GitHub Sync Enabled' if self.github_manager else 'Local Only'}")
        self.show_recent_activity()
    
    def learn_from_memory(self):
        """Learn from previous sessions' knowledge"""
        recent_knowledge = self.memory.get_recent_knowledge()
        if recent_knowledge:
            print("🧠 Learning from previous sessions:")
            for knowledge in recent_knowledge:
                print(f"   - {knowledge['knowledge']}")
    
    def add_knowledge(self, text):
        """Add knowledge for future sessions"""
        self.memory.add_ai_knowledge(text)
        print(f"💡 Knowledge saved for future sessions: {text}")
    
    # [Keep the rest of your methods from previous version]
    # load_config, show_recent_activity, run, execute_command, etc.
    
    def execute_command(self, command):
        print(f"🤖 Executing: {command}")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
            if result.returncode == 0:
                print(f"✅ Success: {result.stdout}")
                self.memory.add_command(command, result.stdout)
                
                # Auto-learn from successful commands
                if "git" in command:
                    self.add_knowledge(f"Git command successful: {command}")
                
            else:
                print(f"❌ Error: {result.stderr}")
                self.memory.add_command(command, f"Error: {result.stderr}")
                
                # Learn from errors too
                self.add_knowledge(f"Command failed: {command}. Error: {result.stderr}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")
            self.memory.add_command(command, f"Exception: {e}")
            self.add_knowledge(f"Command exception: {command}. Exception: {e}")

if __name__ == "__main__":
    agent = UltimateAgent()
    agent.add_knowledge("Agent started new session with GitHub memory integration")
    agent.run()