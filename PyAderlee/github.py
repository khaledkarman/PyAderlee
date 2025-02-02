"""
PyAderlee - Python Data Processing Library
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

GitHub integration module for PyAderlee.
"""
import requests, json, os, base64
from typing import Dict, List, Optional, Union
from pathlib import Path

class GitHub:
    """
    A class to handle GitHub API operations with built-in support for
    common repository management tasks.

    Features:
    - Repository operations (create, delete, list)
    - File management (read, write, delete)
    - Issue tracking
    - Pull request handling
    - Release management
    """

    def __init__(self, token: str, owner: Optional[str] = None):
        """
        Initialize GitHub manager with authentication token.

        Args:
            token: GitHub personal access token
            owner: GitHub username or organization (optional)
        """
        self.token = token
        self.owner = owner
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def create_repo(self, name: str, private: bool = False, 
                   description: str = "") -> Dict:
        """
        Create a new GitHub repository.

        Args:
            name: Repository name
            private: Whether the repository should be private
            description: Repository description

        Returns:
            Repository data dictionary

        Example:
            >>> github = GitHub(token)
            >>> repo = github.create_repo("my-project", description="A test project")
        """
        url = f"{self.base_url}/user/repos"
        data = {
            "name": name,
            "private": private,
            "description": description
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def list_repos(self, type: str = "all") -> List[Dict]:
        """
        List repositories for the authenticated user.

        Args:
            type: Type of repositories to list (all, owner, public, private)

        Returns:
            List of repository data dictionaries
        """
        url = f"{self.base_url}/user/repos"
        params = {"type": type}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def get_repo(self, repo: str) -> Dict:
        """
        Get repository information.

        Args:
            repo: Repository name

        Returns:
            Repository data dictionary
        """
        owner = self.owner or self.get_authenticated_user()["login"]
        url = f"{self.base_url}/repos/{owner}/{repo}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_file(self, repo: str, path: str, content: str, 
                   message: str = "Add file") -> Dict:
        """
        Create a file in a repository.

        Args:
            repo: Repository name
            path: File path in repository
            content: File content
            message: Commit message

        Returns:
            Response data dictionary
        """
        owner = self.owner or self.get_authenticated_user()["login"]
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        
        data = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode()
        }
        
        response = requests.put(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_file(self, repo: str, path: str) -> str:
        """
        Get file content from a repository.

        Args:
            repo: Repository name
            path: File path in repository

        Returns:
            File content as string
        """
        owner = self.owner or self.get_authenticated_user()["login"]
        url = f"{self.base_url}/repos/{owner}/{repo}/contents/{path}"
        
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        
        content = response.json()["content"]
        return base64.b64decode(content).decode()

    def create_issue(self, repo: str, title: str, body: str = "", 
                    labels: List[str] = None) -> Dict:
        """
        Create an issue in a repository.

        Args:
            repo: Repository name
            title: Issue title
            body: Issue description
            labels: List of label names

        Returns:
            Issue data dictionary
        """
        owner = self.owner or self.get_authenticated_user()["login"]
        url = f"{self.base_url}/repos/{owner}/{repo}/issues"
        
        data = {
            "title": title,
            "body": body,
            "labels": labels or []
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def create_release(self, repo: str, tag_name: str, name: str = None, 
                      body: str = "", draft: bool = False) -> Dict:
        """
        Create a release for a repository.

        Args:
            repo: Repository name
            tag_name: Tag name for the release
            name: Release name (optional)
            body: Release description
            draft: Whether this is a draft release

        Returns:
            Release data dictionary
        """
        owner = self.owner or self.get_authenticated_user()["login"]
        url = f"{self.base_url}/repos/{owner}/{repo}/releases"
        
        data = {
            "tag_name": tag_name,
            "name": name or tag_name,
            "body": body,
            "draft": draft
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_authenticated_user(self) -> Dict:
        """
        Get information about the authenticated user.

        Returns:
            User data dictionary
        """
        url = f"{self.base_url}/user"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def clone_org_repos(self, org_name: str, output_dir: str = ".") -> None:
        """
        Clone all repositories from a GitHub organization.
        
        Args:
            org_name: Name of the GitHub organization
            output_dir: Directory to clone repositories into (default: current directory)
        """
        
        # Set up headers with token if provided
        headers = {
            "Accept": GITHUB_ACCEPT,
            "X-GitHub-Api-Version": GITHUB_API_VERSION,

        }
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        # API endpoint for org repos
        page = 1
        api_url = f"https://api.github.com/orgs/{org_name}/repos?per_page=100&page={page}"
        
        # Get list of repos
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200:
            print(f"Error accessing organization: {response.status_code}")
            return
            
        repos = json.loads(response.text)
        repos_len = len(repos)

        # Clone each repository
        print(f"Cloning repositories from {org_name}... Total:", len(repos))
        for repo in repos:
            repo_name = repo["name"]
            clone_url = repo["clone_url"]
            
            # Use auth in clone URL if token provided
            if self.token:
                clone_url = clone_url.replace("https://", f"https://{self.token}@")
                
            target_dir = os.path.join(output_dir, repo_name)
            
            if os.path.exists(target_dir):
                # print(f"Repository {repo_name} already exists, skipping...")
                continue
            command = f"git clone {clone_url} {target_dir}"
            command = f"git clone {repo['git_url']} {target_dir}"
            print(repo['name'])
            os.system(f"git clone {clone_url} {target_dir}")
        while repos_len == 100:
            page += 1
            api_url = f"https://api.github.com/orgs/{org_name}/repos?per_page=100&page={page}"
            response = requests.get(api_url, headers=headers)
            repos = json.loads(response.text)
            repos_len = len(repos)
            print(f"Cloning repositories from {org_name}... Total:", len(repos))
            for repo in repos:
                repo_name = repo["name"]
                clone_url = repo["clone_url"]
                # Use auth in clone URL if token provided
                if self.token:
                    clone_url = clone_url.replace("https://", f"https://{self.token}@")
                    
                target_dir = os.path.join(output_dir, repo_name)
                
                if os.path.exists(target_dir):
                    # print(f"Repository {repo_name} already exists, skipping...")
                    continue
                command = f"git clone {clone_url} {target_dir}"
                command = f"git clone {repo['git_url']} {target_dir}"
                print(repo['name'])
                os.system(f"git clone {clone_url} {target_dir}")
