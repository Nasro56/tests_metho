# Gestionnaire de Tâches - CLI Python

## Description du Projet

Ce projet implémente un **gestionnaire de tâches en ligne de commande** développé en Python avec une architecture robuste et des tests unitaires complets utilisant pytest. L'application permet de gérer des tâches avec toutes les opérations CRUD (Create, Read, Update, Delete) ainsi que des fonctionnalités avancées comme la pagination et la recherche.

## User Stories Implémentées

### Phase 1 - Opérations de base

#### US001 - Créer une tâche
- ✅ Création de tâches avec titre obligatoire (max 100 caractères)
- ✅ Description optionnelle (max 500 caractères)
- ✅ Validation des données d'entrée
- ✅ Nettoyage automatique des espaces en début/fin de titre
- ✅ Attribution d'ID unique et date de création automatique

#### US002 - Consulter une tâche
- ✅ Affichage des détails complets d'une tâche par ID
- ✅ Gestion des erreurs pour ID inexistant ou invalide

#### US003 - Modifier une tâche
- ✅ Modification du titre et/ou de la description
- ✅ Validation des données lors de la modification
- ✅ Préservation des autres champs lors de la modification partielle

#### US004 - Changer le statut d'une tâche
- ✅ Support des statuts : TODO, ONGOING, DONE
- ✅ Validation des statuts autorisés

#### US005 - Supprimer une tâche
- ✅ Suppression définitive d'une tâche
- ✅ Vérification que la tâche supprimée n'est plus accessible

#### US006 - Lister mes tâches avec pagination
- ✅ Pagination configurable (taille par défaut : 20)
- ✅ Informations de pagination complètes
- ✅ Gestion des pages vides et des paramètres invalides

### Phase - Organisation et recherche

#### US007 - Rechercher des tâches
- ✅ Recherche dans le titre et la description
- ✅ Recherche insensible à la casse
- ✅ Pagination des résultats de recherche
- ✅ Gestion des recherches vides

## Architecture du Projet

```
python-cli-pytest/
├── src/
│   ├── main.py              # Interface CLI avec Click
│   └── task_manager.py      # Logique métier et gestion des données
├── tests/
│   ├── test_task_manager.py          # Tests de base existants
│   └── test_task_manager_complete.py # Tests complets pour toutes les US
├── requirements.txt         # Dépendances Python
├── pytest.ini             # Configuration pytest
├── tasks.json              # Stockage des données (généré automatiquement)
└── README.md               # Cette documentation
```

### Composants Principaux

#### 1. `TaskManager` (task_manager.py)
- **Responsabilité** : Logique métier et persistance des données
- **Stockage** : Fichier JSON (`tasks.json`)
- **Méthodes principales** :
  - `create_task()` : Création avec validation
  - `get_task_by_id()` : Récupération par ID
  - `update_task()` : Modification partielle
  - `change_task_status()` : Changement de statut
  - `delete_task()` : Suppression
  - `get_tasks()` : Liste paginée
  - `search_tasks()` : Recherche paginée

#### 2. Interface CLI (main.py)
- **Framework** : Click pour l'interface en ligne de commande
- **Affichage** : Rich pour les tableaux et la colorisation
- **Commandes disponibles** :
  - `create` : Créer une tâche
  - `list` : Lister avec pagination
  - `show` : Afficher une tâche
  - `update` : Modifier une tâche
  - `status` : Changer le statut
  - `delete` : Supprimer (avec confirmation)
  - `search` : Rechercher

## 🧪 Tests et Qualité

### Structure des Tests

Les tests sont organisés par User Story dans `test_task_manager_complete.py` :

- **TestUS001CreateTask** : 8 tests pour la création
- **TestUS002GetTask** : 3 tests pour la consultation
- **TestUS003UpdateTask** : 6 tests pour la modification
- **TestUS004ChangeStatus** : 5 tests pour le changement de statut
- **TestUS005DeleteTask** : 2 tests pour la suppression
- **TestUS006ListTasksPagination** : 6 tests pour la pagination
- **TestUS007SearchTasks** : 7 tests pour la recherche

### Couverture des Tests

**Total : 37 tests** couvrant tous les critères d'acceptation des User Stories.

### Exécution des Tests

```bash
# Tous les tests
python -m pytest

# Tests détaillés avec verbose
python -m pytest -v

# Tests spécifiques
python -m pytest tests/test_task_manager_complete.py -v

# Tests avec couverture
python -m pytest --cov=src
```

## Installation et Utilisation

### Prérequis
- Python 3.8+
- pip

### Installation

```bash
# Cloner le projet
git clone <url-du-projet>
cd python-cli-pytest

# Installer les dépendances
pip install -r requirements.txt
```

### Utilisation de l'Application

#### Commandes de Base

```bash
# Afficher l'aide
python src/main.py --help

# Créer une tâche
python src/main.py create -t "Acheter du pain" -d "Aller à la boulangerie"

# Lister les tâches (pagination par défaut : 20)
python src/main.py list

# Lister avec pagination personnalisée
python src/main.py list --page 1 --size 10

# Afficher une tâche spécifique
python src/main.py show 1

# Modifier une tâche
python src/main.py update 1 -t "Nouveau titre" -d "Nouvelle description"

# Changer le statut
python src/main.py status 1 ONGOING

# Rechercher des tâches
python src/main.py search "pain"
python src/main.py search --page 1 --size 5

# Supprimer une tâche (avec confirmation)
python src/main.py delete 1
```

#### Exemples d'Utilisation

```bash
# Workflow complet
python src/main.py create -t "Développer l'API" -d "Créer les endpoints REST"
python src/main.py create -t "Écrire les tests" -d "Tests unitaires et d'intégration"
python src/main.py list
python src/main.py status 1 ONGOING
python src/main.py search "test"
python src/main.py update 2 -d "Tests unitaires, d'intégration et end-to-end"
```

## Validation des Critères d'Acceptation

### US001 - Créer une tâche ✅
- [x] Titre valide → tâche créée avec ID unique, statut TODO, date de création
- [x] Titre + description valide → tâche créée avec les deux champs
- [x] Titre vide → erreur "Title is required"
- [x] Titre > 100 caractères → erreur "Title cannot exceed 100 characters"
- [x] Description > 500 caractères → erreur "Description cannot exceed 500 characters"
- [x] Titre avec espaces → nettoyage automatique
- [x] Date de création précise à la seconde

### US002 - Consulter une tâche ✅
- [x] ID valide → tous les détails retournés
- [x] ID inexistant → erreur "Task not found"
- [x] ID invalide → erreur "Invalid ID format"

### US003 - Modifier une tâche ✅
- [x] Modification titre seul → titre mis à jour, autres champs inchangés
- [x] Modification description seule → description mise à jour, autres champs inchangés
- [x] Modification titre ET description → les deux champs mis à jour
- [x] Titre vide → erreur "Title is required"
- [x] Titre > 100 caractères → erreur appropriée
- [x] Description > 500 caractères → erreur appropriée
- [x] ID inexistant → erreur "Task not found"

### US004 - Changer le statut ✅
- [x] Statuts TODO, ONGOING, DONE → mise à jour réussie
- [x] Statut invalide → erreur "Invalid status. Allowed values: TODO, ONGOING, DONE"
- [x] ID inexistant → erreur "Task not found"

### US005 - Supprimer une tâche ✅
- [x] Tâche existante → suppression et disparition de la liste
- [x] Opérations sur tâche supprimée → erreur "Task not found"

### US006 - Pagination ✅
- [x] Page 1, taille 10 → max 10 tâches + infos pagination
- [x] Page 2 → tâches suivantes + infos correctes
- [x] Page au-delà → liste vide + infos correctes
- [x] Paramètres par défaut → page 1, taille 20
- [x] Taille invalide → erreur "Invalid page size"
- [x] Liste vide → 0 éléments, 0 pages

### US007 - Rechercher ✅
- [x] Mot-clé dans titre → tâches correspondantes
- [x] Mot-clé dans description → tâches correspondantes
- [x] Mot-clé dans titre ET description → toutes les tâches (sans doublon)
- [x] Terme inexistant → liste vide
- [x] Chaîne vide → toutes les tâches
- [x] Insensible à la casse → résultats identiques
- [x] Nombreux résultats → pagination appliquée



## 🔧 Configuration et Personnalisation

### Fichier pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
```

### Dépendances (requirements.txt)
- **click==8.1.7** : Interface CLI
- **pytest==7.4.4** : Framework de tests
- **pytest-cov==4.1.0** : Couverture de code
- **rich==13.7.0** : Interface utilisateur enrichie
