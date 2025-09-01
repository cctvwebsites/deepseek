# unified_agent.py
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from learning_module import LearningModule
from task_recognition import TaskRecognizer
from tools.path_tool import interpret_path
from tools.file_tool import create_file

# Load environment
env_path = os.path.join(os.path.dirname(__file__), 'auth', '.env')
load_dotenv(dotenv_path=env_path)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("ERROR: GEMINI_API_KEY not found")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

class UnifiedAgent:
    def __init__(self):
        self.learning = LearningModule()
        self.task_recognizer = TaskRecognizer()
        self.is_active = True
    
    def process_command(self, user_input):
        print(f"Processing: {user_input}")
        
        # Learn from every interaction
        self.learning.record_conversation(user_input, "")
        
        # Recognize task type
        task_type = self.task_recognizer.recognize_task(user_input)
        
        if task_type != "conversation":
            return self.handle_task(user_input, task_type)
        else:
            return self.generate_response(user_input)
    
    def handle_task(self, user_input, task_type):
        print(f"Detected task type: {task_type}")
        
        if task_type == "create_file":
            return self.handle_file_creation(user_input)
        else:
            return f"I recognize this as a {task_type} task. I'll handle it."
    
    def handle_file_creation(self, user_input):
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            response = model.generate_content(f"""
            Create a file based on this request: {user_input}
            Respond with this exact format:
            [INTENT: CREATE_FILE]
            [PATH: suggested_path]
            [FILENAME: suggested_filename]
            ```file_content
            content_here
            ```
            """)
            
            return self.execute_file_creation(response.text)
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def execute_file_creation(self, response_text):
        # Parse and execute file creation (existing logic)
        lines = response_text.split('\n')
        intent = path = filename = None
        
        for line in lines:
            if line.startswith('[INTENT:'):
                intent = line.split(':')[1].strip().rstrip(']')
            elif line.startswith('[PATH:'):
                path = line.split(':')[1].strip().rstrip(']')
            elif line.startswith('[FILENAME:'):
                filename = line.split(':')[1].strip().rstrip(']')
        
        if intent == "CREATE_FILE" and filename:
            # Extract code content
            code_match = re.search(r'```(?:\w+)?\s*(.*?)```', response_text, re.DOTALL)
            if code_match:
                content = code_match.group(1).strip()
                full_path = interpret_path(path or "desktop", filename)
                create_file(full_path, content)
                return f"SUCCESS: Created {filename} at {full_path}"
        
        return "Could not parse the file creation instructions."
    
    def generate_response(self, user_input):
        try:
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            response = model.generate_content(user_input)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"

def main():
    print("🤖 Unified AI Agent Activated!")
    agent = UnifiedAgent()
    
    while True:
        user_input = input("\nYour command: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        response = agent.process_command(user_input)
        print(f"Agent: {response}")

if __name__ == "__main__":
    main()