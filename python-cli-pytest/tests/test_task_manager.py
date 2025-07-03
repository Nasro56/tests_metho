# test_task_manager.py - Tests pour la logique métier
import sys
import os
import pytest
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.task_manager import TaskManager, create_task

class TestTaskManager:
    
    def setup_method(self):
        """Initialise les données de test avant chaque test"""
        self.task_manager = TaskManager()
        self.task_manager.tasks = []
    
    def test_create_task_with_valid_title(self):
        """Test création d'une tâche avec un titre valide"""
        task = self.task_manager.create_task("Tâche de test")
        
        assert task["id"] == 1
        assert task["title"] == "Tâche de test"
        assert task["description"] == ""
        assert task["status"] == "TODO"
        assert "created_at" in task
        assert len(self.task_manager.tasks) == 1
    
    def test_create_task_with_title_and_description(self):
        """Test création d'une tâche avec titre et description"""
        task = self.task_manager.create_task("Tâche de test", "Description de test")
        
        assert task["title"] == "Tâche de test"
        assert task["description"] == "Description de test"
        assert task["status"] == "TODO"
    
    def test_create_task_with_empty_title_raises_error(self):
        """Test qu'un titre vide lève une erreur"""
        with pytest.raises(ValueError, match="Title is required"):
            self.task_manager.create_task("")
    
    def test_create_task_with_whitespace_only_title_raises_error(self):
        """Test qu'un titre avec seulement des espaces lève une erreur"""
        with pytest.raises(ValueError, match="Title is required"):
            self.task_manager.create_task("   ")
    
    def test_create_task_with_title_too_long_raises_error(self):
        """Test qu'un titre trop long lève une erreur"""
        long_title = "a" * 101
        with pytest.raises(ValueError, match="Title cannot exceed 100 characters"):
            self.task_manager.create_task(long_title)
    
    def test_create_task_with_description_too_long_raises_error(self):
        """Test qu'une description trop longue lève une erreur"""
        long_description = "a" * 501
        with pytest.raises(ValueError, match="Description cannot exceed 500 characters"):
            self.task_manager.create_task("Titre", long_description)
    
    def test_create_task_trims_title_whitespace(self):
        """Test que les espaces en début/fin de titre sont supprimés"""
        task = self.task_manager.create_task("  Tâche avec espaces  ")
        
        assert task["title"] == "Tâche avec espaces"
    
    def test_create_task_creation_date_is_current(self):
        """Test que la date de création correspond au moment de création"""
        before_creation = datetime.now()
        task = self.task_manager.create_task("Tâche test date")
        after_creation = datetime.now()
        
        created_at = datetime.fromisoformat(task["created_at"])
        assert before_creation <= created_at <= after_creation
    
    def test_create_task_generates_unique_ids(self):
        """Test que les IDs générés sont uniques"""
        task1 = self.task_manager.create_task("Tâche 1")
        task2 = self.task_manager.create_task("Tâche 2")
        
        assert task1["id"] != task2["id"]
        assert task1["id"] == 1
        assert task2["id"] == 2
    
    def test_get_tasks_returns_list(self):
        """Test que get_tasks retourne une liste"""
        tasks = self.task_manager.get_tasks()
        
        assert isinstance(tasks, list)
    
    def test_get_tasks_returns_created_tasks(self):
        """Test que get_tasks retourne les tâches créées"""
        self.task_manager.create_task("Tâche 1")
        self.task_manager.create_task("Tâche 2")
        
        tasks = self.task_manager.get_tasks()
        assert len(tasks) == 2
        assert tasks[0]["title"] == "Tâche 1"
        assert tasks[1]["title"] == "Tâche 2"

class TestTaskManagerGlobalFunctions:
    """Tests pour les fonctions globales"""
    
    def test_global_create_task_function(self):
        """Test de la fonction globale create_task"""
        task = create_task("Tâche globale")
        
        assert task["title"] == "Tâche globale"
        assert task["status"] == "TODO"
        assert "created_at" in task
