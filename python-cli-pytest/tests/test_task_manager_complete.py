# test_task_manager_complete.py - Tests complets pour toutes les User Stories
import sys
import os
import pytest
from datetime import datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.task_manager import TaskManager

class TestUS001CreateTask:
    """Tests pour US001 - Créer une tâche"""
    
    def setup_method(self):
        self.task_manager = TaskManager()
        self.task_manager.tasks = []
    
    def test_create_task_with_valid_title(self):
        """ÉTANT DONNÉ QUE je fournis un titre valide, LORSQUE je crée une tâche, ALORS elle est créée avec les bonnes valeurs"""
        task = self.task_manager.create_task("Tâche de test")
        
        assert task["id"] == 1
        assert task["title"] == "Tâche de test"
        assert task["description"] == ""
        assert task["status"] == "TODO"
        assert "created_at" in task
    
    def test_create_task_with_title_and_description(self):
        """ÉTANT DONNÉ QUE je fournis un titre et une description valide, LORSQUE je crée une tâche, ALORS elle est créée avec le titre et la description fournis"""
        task = self.task_manager.create_task("Tâche test", "Description test")
        
        assert task["title"] == "Tâche test"
        assert task["description"] == "Description test"
        assert task["status"] == "TODO"
    
    def test_create_task_empty_title_error(self):
        """ÉTANT DONNÉ QUE je fournis un titre vide, LORSQUE je tente de créer une tâche, ALORS j'obtiens une erreur "Title is required" """
        with pytest.raises(ValueError, match="Title is required"):
            self.task_manager.create_task("")
    
    def test_create_task_whitespace_title_error(self):
        """ÉTANT DONNÉ QUE je fournis un titre composé uniquement d'espaces, LORSQUE je tente de créer une tâche, ALORS j'obtiens une erreur "Title is required" """
        with pytest.raises(ValueError, match="Title is required"):
            self.task_manager.create_task("   ")
    
    def test_create_task_title_too_long_error(self):
        """ÉTANT DONNÉ QUE je fournis un titre de plus de 100 caractères, LORSQUE je tente de créer une tâche, ALORS j'obtiens une erreur "Title cannot exceed 100 characters" """
        long_title = "a" * 101
        with pytest.raises(ValueError, match="Title cannot exceed 100 characters"):
            self.task_manager.create_task(long_title)
    
    def test_create_task_description_too_long_error(self):
        """ÉTANT DONNÉ QUE je fournis une description de plus de 500 caractères, LORSQUE je tente de créer une tâche, ALORS j'obtiens une erreur "Description cannot exceed 500 characters" """
        long_description = "a" * 501
        with pytest.raises(ValueError, match="Description cannot exceed 500 characters"):
            self.task_manager.create_task("Titre", long_description)
    
    def test_create_task_trims_title(self):
        """ÉTANT DONNÉ QUE je fournis un titre qui commence et/ou termine par des espaces, LORSQUE je crée une tâche, ALORS elle est créée avec le titre sans espaces"""
        task = self.task_manager.create_task("  Tâche avec espaces  ")
        
        assert task["title"] == "Tâche avec espaces"
    
    def test_create_task_date_precision(self):
        """ÉTANT DONNÉ QUE j'ai une tâche nouvellement créée, LORSQUE je la consulte, ALORS sa date de création correspond au moment de création à la seconde près"""
        before = datetime.now()
        task = self.task_manager.create_task("Test date")
        after = datetime.now()
        
        created_at = datetime.fromisoformat(task["created_at"])
        assert before <= created_at <= after

class TestUS002GetTask:
    """Tests pour US002 - Consulter une tâche"""
    
    def setup_method(self):
        self.task_manager = TaskManager()
        self.task_manager.tasks = []
        self.test_task = self.task_manager.create_task("Tâche test", "Description test")
    
    def test_get_task_with_valid_id(self):
        """ÉTANT DONNÉ QUE j'ai une tâche existante avec ID valide, LORSQUE je consulte cette tâche, ALORS j'obtiens tous ses détails"""
        task = self.task_manager.get_task_by_id(self.test_task["id"])
        
        assert task["id"] == self.test_task["id"]
        assert task["title"] == "Tâche test"
        assert task["description"] == "Description test"
        assert task["status"] == "TODO"
        assert "created_at" in task
    
    def test_get_task_with_nonexistent_id(self):
        """ÉTANT DONNÉ QUE je consulte une tâche avec un ID inexistant, LORSQUE je fais la demande, ALORS j'obtiens une erreur "Task not found" """
        with pytest.raises(ValueError, match="Task not found"):
            self.task_manager.get_task_by_id(999)
    
    def test_get_task_with_invalid_id_format(self):
        """ÉTANT DONNÉ QUE je consulte une tâche avec un ID au mauvais format, LORSQUE je fais la demande, ALORS j'obtiens une erreur "Invalid ID format" """
        with pytest.raises(ValueError, match="Invalid ID format"):
            self.task_manager.get_task_by_id("invalid")

class TestUS003UpdateTask:
    """Tests pour US003 - Modifier une tâche"""
    
    def setup_method(self):
        self.task_manager = TaskManager()
        self.task_manager.tasks = []
        self.test_task = self.task_manager.create_task("Titre original", "Description originale")
    
    def test_update_task_title_only(self):
        """ÉTANT DONNÉ QUE j'ai une tâche existante, LORSQUE je modifie son titre avec une valeur valide, ALORS le nouveau titre est sauvegardé et les autres champs restent inchangés"""
        original_description = self.test_task["description"]
        original_status = self.test_task["status"]
        
        updated_task = self.task_manager.update_task(self.test_task["id"], title="Nouveau titre")
        
        assert updated_task["title"] == "Nouveau titre"
        assert updated_task["description"] == original_description
        assert updated_task["status"] == original_status
    
    def test_update_task_description_only(self):
        """ÉTANT DONNÉ QUE j'ai une tâche existante, LORSQUE je modifie sa description avec une valeur valide, ALORS la nouvelle description est sauvegardée et les autres champs restent inchangés"""
        original_title = self.test_task["title"]
        original_status = self.test_task["status"]
        
        updated_task = self.task_manager.update_task(self.test_task["id"], description="Nouvelle description")
        
        assert updated_task["title"] == original_title
        assert updated_task["description"] == "Nouvelle description"
        assert updated_task["status"] == original_status
    
    def test_update_task_both_title_and_description(self):
        """ÉTANT DONNÉ QUE j'ai une tâche existante, LORSQUE je modifie à la fois le titre et la description, ALORS les deux modifications sont sauvegardées"""
        updated_task = self.task_manager.update_task(
            self.test_task["id"], 
            title="Titre modifié", 
            description="Description modifiée"
        )
        
        assert updated_task["title"] == "Titre modifié"
        assert updated_task["description"] == "Description modifiée"
    
    def test_update_task_empty_title_error(self):
        """ÉTANT DONNÉ QUE je tente de modifier le titre d'une tâche avec une valeur vide, LORSQUE je soumets la modification, ALORS j'obtiens une erreur "Title is required" """
        with pytest.raises(ValueError, match="Title is required"):
            self.task_manager.update_task(self.test_task["id"], title="")
    
    def test_update_task_title_too_long_error(self):
        """ÉTANT DONNÉ QUE je tente de modifier une tâche avec un titre de plus de 100 caractères, LORSQUE je soumets, ALORS j'obtiens une erreur "Title cannot exceed 100 characters" """
        long_title = "a" * 101
        with pytest.raises(ValueError, match="Title cannot exceed 100 characters"):
            self.task_manager.update_task(self.test_task["id"], title=long_title)
    
    def test_update_task_description_too_long_error(self):
        """ÉTANT DONNÉ QUE je tente de modifier une tâche avec une description de plus de 500 caractères, LORSQUE je soumets, ALORS j'obtiens une erreur "Description cannot exceed 500 characters" """
        long_description = "a" * 501
        with pytest.raises(ValueError, match="Description cannot exceed 500 characters"):
            self.task_manager.update_task(self.test_task["id"], description=long_description)
    
    def test_update_nonexistent_task_error(self):
        """ÉTANT DONNÉ QUE je tente de modifier une tâche inexistante, LORSQUE j'utilise un ID invalide, ALORS j'obtiens une erreur "Task not found" """
        with pytest.raises(ValueError, match="Task not found"):
            self.task_manager.update_task(999, title="Nouveau titre")

class TestUS004ChangeStatus:
    """Tests pour US004 - Changer le statut d'une tâche"""
    
    def setup_method(self):
        self.task_manager = TaskManager()
        self.task_manager.tasks = []
        self.test_task = self.task_manager.create_task("Tâche test")
    
    def test_change_status_to_todo(self):
        """ÉTANT DONNÉ QUE j'ai une tâche existante, LORSQUE je change son statut vers "TODO", ALORS le statut est mis à jour avec succès"""
        updated_task = self.task_manager.change_task_status(self.test_task["id"], "TODO")
        assert updated_task["status"] == "TODO"
    
    def test_change_status_to_ongoing(self):
        """ÉTANT DONNÉ QUE j'ai une tâche existante, LORSQUE je change son statut vers "ONGOING", ALORS le statut est mis à jour avec succès"""
        updated_task = self.task_manager.change_task_status(self.test_task["id"], "ONGOING")
        assert updated_task["status"] == "ONGOING"
    
    def test_change_status_to_done(self):
        """ÉTANT DONNÉ QUE j'ai une tâche existante, LORSQUE je change son statut vers "DONE", ALORS le statut est mis à jour avec succès"""
        updated_task = self.task_manager.change_task_status(self.test_task["id"], "DONE")
        assert updated_task["status"] == "DONE"
    
    def test_change_status_invalid_value_error(self):
        """ÉTANT DONNÉ QUE je tente de changer le statut d'une tâche vers une valeur invalide, LORSQUE je soumets le changement, ALORS j'obtiens une erreur "Invalid status. Allowed values: TODO, ONGOING, DONE" """
        with pytest.raises(ValueError, match="Invalid status. Allowed values: TODO, ONGOING, DONE"):
            self.task_manager.change_task_status(self.test_task["id"], "INVALID")
    
    def test_change_status_nonexistent_task_error(self):
        """ÉTANT DONNÉ QUE je tente de changer le statut d'une tâche inexistante, LORSQUE j'utilise un ID invalide, ALORS j'obtiens une erreur "Task not found" """
        with pytest.raises(ValueError, match="Task not found"):
            self.task_manager.change_task_status(999, "DONE")

class TestUS005DeleteTask:
    """Tests pour US005 - Supprimer une tâche"""
    
    def setup_method(self):
        self.task_manager = TaskManager()
        self.task_manager.tasks = []
        self.test_task = self.task_manager.create_task("Tâche à supprimer")
    
    def test_delete_existing_task(self):
        """ÉTANT DONNÉ QUE j'ai une tâche existante, LORSQUE je la supprime, ALORS elle n'apparaît plus dans la liste des tâches"""
        task_id = self.test_task["id"]
        
        result = self.task_manager.delete_task(task_id)
        assert result is True
        
        tasks_result = self.task_manager.get_tasks()
        task_ids = [task["id"] for task in tasks_result["tasks"]]
        assert task_id not in task_ids
    
    def test_deleted_task_operations_error(self):
        """ÉTANT DONNÉ QUE j'ai supprimé une tâche, LORSQUE je tente de la consulter, de la supprimer, de la modifier ou de changer son statut par son ID, ALORS j'obtiens une erreur "Task not found" """
        task_id = self.test_task["id"]
        self.task_manager.delete_task(task_id)
        
        with pytest.raises(ValueError, match="Task not found"):
            self.task_manager.get_task_by_id(task_id)
        
        with pytest.raises(ValueError, match="Task not found"):
            self.task_manager.delete_task(task_id)
        
        with pytest.raises(ValueError, match="Task not found"):
            self.task_manager.update_task(task_id, title="Nouveau titre")
        
        with pytest.raises(ValueError, match="Task not found"):
            self.task_manager.change_task_status(task_id, "DONE")

class TestUS006ListTasksPagination:
    """Tests pour US006 - Lister mes tâches avec pagination"""
    
    def setup_method(self):
        self.task_manager = TaskManager()
        self.task_manager.tasks = []
        
        for i in range(25):
            self.task_manager.create_task(f"Tâche {i+1}")
    
    def test_first_page_with_size_10(self):
        """ÉTANT DONNÉ QUE j'ai plusieurs tâches, LORSQUE je demande la première page avec une taille de 10, ALORS j'obtiens au maximum 10 tâches et les informations de pagination"""
        result = self.task_manager.get_tasks(page=1, page_size=10)
        
        assert len(result["tasks"]) == 10
        assert result["pagination"]["current_page"] == 1
        assert result["pagination"]["total_pages"] == 3
        assert result["pagination"]["total_tasks"] == 25
        assert result["pagination"]["page_size"] == 10
    
    def test_second_page(self):
        """ÉTANT DONNÉ QUE j'ai plus de 10 tâches, LORSQUE je demande la deuxième page, ALORS j'obtiens les tâches suivantes avec les bonnes informations de pagination"""
        result = self.task_manager.get_tasks(page=2, page_size=10)
        
        assert len(result["tasks"]) == 10
        assert result["pagination"]["current_page"] == 2
        assert result["pagination"]["total_pages"] == 3
        assert result["pagination"]["total_tasks"] == 25
    
    def test_page_beyond_total_pages(self):
        """ÉTANT DONNÉ QUE je demande une page au-delà du nombre total de pages, LORSQUE j'exécute la requête, ALORS j'obtiens une liste vide avec les informations de pagination correctes"""
        result = self.task_manager.get_tasks(page=10, page_size=10)
        
        assert len(result["tasks"]) == 0
        assert result["pagination"]["current_page"] == 10
        assert result["pagination"]["total_pages"] == 3
        assert result["pagination"]["total_tasks"] == 25
    
    def test_default_pagination_parameters(self):
        """ÉTANT DONNÉ QUE je ne spécifie pas de paramètres de pagination, LORSQUE je demande la liste, ALORS j'obtiens la première page avec une taille par défaut de 20 éléments"""
        result = self.task_manager.get_tasks()
        
        assert len(result["tasks"]) == 20
        assert result["pagination"]["current_page"] == 1
        assert result["pagination"]["page_size"] == 20
    
    def test_invalid_page_size_error(self):
        """ÉTANT DONNÉ QUE je spécifie une taille de page invalide (négative ou zéro), LORSQUE je fais la demande, ALORS j'obtiens une erreur "Invalid page size" """
        with pytest.raises(ValueError, match="Invalid page size"):
            self.task_manager.get_tasks(page=1, page_size=0)
        
        with pytest.raises(ValueError, match="Invalid page size"):
            self.task_manager.get_tasks(page=1, page_size=-1)
    
    def test_empty_task_list_pagination(self):
        """ÉTANT DONNÉ QUE j'ai aucune tâche, LORSQUE je demande la liste, ALORS j'obtiens une liste vide avec les informations de pagination (0 éléments, 0 pages)"""
        empty_manager = TaskManager()
        empty_manager.tasks = []
        
        result = empty_manager.get_tasks()
        
        assert len(result["tasks"]) == 0
        assert result["pagination"]["total_tasks"] == 0
        assert result["pagination"]["total_pages"] == 0

class TestUS007SearchTasks:
    """Tests pour US007 - Rechercher des tâches"""
    
    def setup_method(self):
        self.task_manager = TaskManager()
        self.task_manager.tasks = []
        
        self.task_manager.create_task("Acheter du pain", "Aller à la boulangerie")
        self.task_manager.create_task("Projet Python", "Développer une application")
        self.task_manager.create_task("Appeler le client", "Discuter du projet")
        self.task_manager.create_task("Faire du sport")
        self.task_manager.create_task("PROJET Web", "Créer un site internet")
    
    def test_search_tasks_by_title(self):
        """ÉTANT DONNÉ QUE j'ai des tâches contenant un mot-clé dans le titre, LORSQUE je recherche ce terme, ALORS seules les tâches correspondantes sont retournées"""
        result = self.task_manager.search_tasks("projet")
        
        found_titles = [task["title"] for task in result["tasks"]]
        assert "Projet Python" in found_titles
        assert "PROJET Web" in found_titles
        assert "Appeler le client" in found_titles
        assert len(result["tasks"]) == 3
    
    def test_search_tasks_by_description(self):
        """ÉTANT DONNÉ QUE j'ai des tâches contenant un mot-clé dans la description, LORSQUE je recherche ce terme, ALORS seules les tâches correspondantes sont retournées"""
        result = self.task_manager.search_tasks("boulangerie")
        
        found_titles = [task["title"] for task in result["tasks"]]
        assert "Acheter du pain" in found_titles
        assert len(result["tasks"]) == 1
    
    def test_search_tasks_in_title_and_description(self):
        """ÉTANT DONNÉ QUE j'ai des tâches contenant un mot-clé dans le titre ET la description, LORSQUE je recherche ce terme, ALORS toutes ces tâches sont retournées (sans doublon)"""
        result = self.task_manager.search_tasks("projet")
        
        found_titles = [task["title"] for task in result["tasks"]]
        assert "Projet Python" in found_titles
        assert "Appeler le client" in found_titles
        assert "PROJET Web" in found_titles
        assert len(result["tasks"]) == 3
    
    def test_search_nonexistent_term(self):
        """ÉTANT DONNÉ QUE je recherche un terme inexistant, LORSQUE j'exécute la recherche, ALORS j'obtiens une liste vide"""
        result = self.task_manager.search_tasks("inexistant")
        
        assert len(result["tasks"]) == 0
        assert result["pagination"]["total_tasks"] == 0
    
    def test_search_empty_string_returns_all(self):
        """ÉTANT DONNÉ QUE je recherche avec une chaîne vide, LORSQUE j'exécute la recherche, ALORS toutes les tâches sont retournées"""
        result = self.task_manager.search_tasks("")
        
        assert len(result["tasks"]) == 5
        assert result["pagination"]["total_tasks"] == 5
    
    def test_search_case_insensitive(self):
        """ÉTANT DONNÉ QUE je recherche avec des majuscules/minuscules, LORSQUE j'exécute la recherche, ALORS la recherche est insensible à la casse"""
        result_lower = self.task_manager.search_tasks("projet")
        result_upper = self.task_manager.search_tasks("PROJET")
        result_mixed = self.task_manager.search_tasks("ProJet")
        
        assert len(result_lower["tasks"]) == len(result_upper["tasks"]) == len(result_mixed["tasks"])
        assert len(result_lower["tasks"]) == 3
    
    def test_search_with_pagination(self):
        """ÉTANT DONNÉ QUE j'ai de nombreux résultats de recherche, LORSQUE je fais la recherche, ALORS les résultats sont paginés comme la liste normale"""
        for i in range(15):
            self.task_manager.create_task(f"Test numéro {i}")
        
        result = self.task_manager.search_tasks("test", page=1, page_size=10)
        
        assert len(result["tasks"]) == 10
        assert result["pagination"]["current_page"] == 1
        assert result["pagination"]["total_tasks"] == 15
        assert result["pagination"]["page_size"] == 10