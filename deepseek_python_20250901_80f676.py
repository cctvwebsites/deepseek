# github_integration.py
import os
import json
import requests
from pathlib import Path

class GitHubManager:
    def __init__(self, token, repo_owner, repo_name):
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_file(self, file_path):
        """Get a file from GitHub"""
        url = f"{self.base_url}/contents/{file_path}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None
    
    def update_file(self, file_path, content, message):
        """Update a file on GitHub"""
        # First get the current file to get its SHA
        current_file = self.get_file(file_path)
        sha = current_file['sha'] if current_file else None
        
        url = f"{self.base_url}/contents/{file_path}"
        data = {
            "message": message,
            "content": content,
            "sha": sha
        }
        response = requests.put(url, headers=self.headers, json=data)
        return response.status_code == 200
    
    def create_file(self, file_path, content, message):
        """Create a new file on GitHub"""
        url = f"{self.base_url}/contents/{file_path}"
        data = {
            "message": message,
            "content": content
        }
        response = requests.put(url, headers=self.headers, json=data)
        return response.status_code == 201