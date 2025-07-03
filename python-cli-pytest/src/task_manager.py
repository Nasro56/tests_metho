# task_manager.py - Logique métier du gestionnaire de tâches

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from uuid import uuid4

DATA_FILE = "tasks.json"

class TaskManager:
    def __init__(self):
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict]:
        """Charge les tâches depuis le fichier JSON"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_tasks(self):
        """Sauvegarde les tâches dans le fichier JSON"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except IOError:
            pass
    
    def _get_next_id(self) -> int:
        """Génère le prochain ID unique"""
        if not self.tasks:
            return 1
        return max(task["id"] for task in self.tasks) + 1
    
    def _find_task_by_id(self, task_id: int) -> Optional[Dict]:
        """Trouve une tâche par son ID"""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def _validate_id(self, task_id) -> int:
        """Valide et convertit un ID"""
        try:
            return int(task_id)
        except (ValueError, TypeError):
            raise ValueError("Invalid ID format")
    
    def _validate_status(self, status: str):
        """Valide un statut"""
        valid_statuses = ["TODO", "ONGOING", "DONE"]
        if status not in valid_statuses:
            raise ValueError("Invalid status. Allowed values: TODO, ONGOING, DONE")
    
    def create_task(self, title: str, description: str = "") -> Dict:
        """Crée une nouvelle tâche avec validation"""
        if not title or not title.strip():
            raise ValueError("Title is required")
        
        title = title.strip()
        
        if len(title) > 100:
            raise ValueError("Title cannot exceed 100 characters")
        
        if len(description) > 500:
            raise ValueError("Description cannot exceed 500 characters")
        
        task = {
            "id": self._get_next_id(),
            "title": title,
            "description": description,
            "status": "TODO",
            "created_at": datetime.now().isoformat()
        }
        
        self.tasks.append(task)
        self._save_tasks()
        return task
    
    def get_task_by_id(self, task_id) -> Dict:
        """Récupère une tâche par son ID"""
        task_id = self._validate_id(task_id)
        task = self._find_task_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        return task
    
    def update_task(self, task_id, title: Optional[str] = None, description: Optional[str] = None) -> Dict:
        """Met à jour une tâche"""
        task_id = self._validate_id(task_id)
        task = self._find_task_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        
        if title is not None:
            if not title.strip():
                raise ValueError("Title is required")
            title = title.strip()
            if len(title) > 100:
                raise ValueError("Title cannot exceed 100 characters")
            task["title"] = title
        
        if description is not None:
            if len(description) > 500:
                raise ValueError("Description cannot exceed 500 characters")
            task["description"] = description
        
        self._save_tasks()
        return task
    
    def change_task_status(self, task_id, status: str) -> Dict:
        """Change le statut d'une tâche"""
        task_id = self._validate_id(task_id)
        task = self._find_task_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        
        self._validate_status(status)
        task["status"] = status
        self._save_tasks()
        return task
    
    def delete_task(self, task_id) -> bool:
        """Supprime une tâche"""
        task_id = self._validate_id(task_id)
        task = self._find_task_by_id(task_id)
        if not task:
            raise ValueError("Task not found")
        
        self.tasks.remove(task)
        self._save_tasks()
        return True
    
    def get_tasks(self, page: int = 1, page_size: int = 20) -> Dict:
        """Récupère la liste des tâches avec pagination"""
        if page_size <= 0:
            raise ValueError("Invalid page size")
        
        total_tasks = len(self.tasks)
        total_pages = (total_tasks + page_size - 1) // page_size if total_tasks > 0 else 0
        
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        page_tasks = self.tasks[start_index:end_index] if page <= total_pages else []
        
        return {
            "tasks": page_tasks,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_tasks": total_tasks,
                "page_size": page_size
            }
        }
    
    def search_tasks(self, query: str = "", page: int = 1, page_size: int = 20) -> Dict:
        """Recherche des tâches par mots-clés"""
        if page_size <= 0:
            raise ValueError("Invalid page size")
        
        if not query:
            return self.get_tasks(page, page_size)
        
        query_lower = query.lower()
        filtered_tasks = []
        
        for task in self.tasks:
            title_match = query_lower in task["title"].lower()
            description_match = query_lower in task["description"].lower()
            
            if title_match or description_match:
                filtered_tasks.append(task)
        
        total_tasks = len(filtered_tasks)
        total_pages = (total_tasks + page_size - 1) // page_size if total_tasks > 0 else 0
        
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        
        page_tasks = filtered_tasks[start_index:end_index] if page <= total_pages else []
        
        return {
            "tasks": page_tasks,
            "pagination": {
                "current_page": page,
                "total_pages": total_pages,
                "total_tasks": total_tasks,
                "page_size": page_size
            }
        }

# Instance globale pour rétrocompatibilité
_task_manager = TaskManager()

def get_tasks(page: int = 1, page_size: int = 20) -> Dict:
    """Récupère la liste des tâches avec pagination (fonction globale)"""
    return _task_manager.get_tasks(page, page_size)

def create_task(title: str, description: str = "") -> Dict:
    """Crée une nouvelle tâche (fonction globale)"""
    return _task_manager.create_task(title, description)

def get_task_by_id(task_id) -> Dict:
    """Récupère une tâche par son ID (fonction globale)"""
    return _task_manager.get_task_by_id(task_id)

def update_task(task_id, title: Optional[str] = None, description: Optional[str] = None) -> Dict:
    """Met à jour une tâche (fonction globale)"""
    return _task_manager.update_task(task_id, title, description)

def change_task_status(task_id, status: str) -> Dict:
    """Change le statut d'une tâche (fonction globale)"""
    return _task_manager.change_task_status(task_id, status)

def delete_task(task_id) -> bool:
    """Supprime une tâche (fonction globale)"""
    return _task_manager.delete_task(task_id)

def search_tasks(query: str = "", page: int = 1, page_size: int = 20) -> Dict:
    """Recherche des tâches par mots-clés (fonction globale)"""
    return _task_manager.search_tasks(query, page, page_size)
