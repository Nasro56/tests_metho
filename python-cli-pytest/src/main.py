#!/usr/bin/env python3

import click
from rich.console import Console
from rich.table import Table

from task_manager import get_tasks, create_task, get_task_by_id, update_task, change_task_status, delete_task, search_tasks

console = Console()

@click.group()
def cli():
    """Gestionnaire de Tâches - Version CLI Python"""
    pass

@cli.command()
@click.option('--page', '-p', default=1, type=int, help='Numéro de page')
@click.option('--size', '-s', default=20, type=int, help='Taille de page')
def list(page, size):
    """Lister les tâches avec pagination"""
    try:
        result = get_tasks(page, size)
        tasks = result["tasks"]
        pagination = result["pagination"]
        
        if not tasks:
            console.print("Aucune tâche trouvée.", style="yellow")
            return
        
        table = Table(title=f"Liste des tâches - Page {pagination['current_page']}/{pagination['total_pages']}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Statut", style="green")
        table.add_column("Titre", style="white")
        table.add_column("Description", style="dim")
        table.add_column("Créée le", style="magenta")
        
        for task in tasks:
            created_at = task.get("created_at", "")
            if created_at:
                created_at = created_at.split("T")[0]
            
            table.add_row(
                str(task["id"]),
                task['status'],
                task["title"],
                task["description"] if task["description"] else "-",
                created_at
            )
        
        console.print(table)
        console.print(f"Total: {pagination['total_tasks']} tâches | Page {pagination['current_page']}/{pagination['total_pages']}", style="dim")
    
    except ValueError as e:
        console.print(f"❌ Erreur: {str(e)}", style="red")

@cli.command()
@click.option('--title', '-t', required=True, help='Titre de la tâche')
@click.option('--description', '-d', default='', help='Description de la tâche (optionnelle)')
def create(title, description):
    """Créer une nouvelle tâche"""
    try:
        task = create_task(title, description)
        console.print(f"✅ Tâche créée avec succès (ID: {task['id']})", style="green")
        console.print(f"Titre: {task['title']}")
        if task['description']:
            console.print(f"Description: {task['description']}")
        console.print(f"Statut: {task['status']}")
        console.print(f"Créée le: {task['created_at']}")
    except ValueError as e:
        console.print(f"❌ Erreur: {str(e)}", style="red")

@cli.command()
@click.argument('task_id', type=int)
def show(task_id):
    """Afficher les détails d'une tâche"""
    try:
        task = get_task_by_id(task_id)
        
        console.print(f"[bold cyan]Tâche #{task['id']}[/bold cyan]")
        console.print(f"Titre: {task['title']}")
        console.print(f"Description: {task['description'] if task['description'] else 'Aucune description'}")
        console.print(f"Statut: [green]{task['status']}[/green]")
        console.print(f"Créée le: {task['created_at']}")
        
    except ValueError as e:
        console.print(f"❌ Erreur: {str(e)}", style="red")

@cli.command()
@click.argument('task_id', type=int)
@click.option('--title', '-t', help='Nouveau titre de la tâche')
@click.option('--description', '-d', help='Nouvelle description de la tâche')
def update(task_id, title, description):
    """Modifier une tâche"""
    try:
        if not title and description is None:
            console.print("❌ Erreur: Au moins un paramètre (titre ou description) doit être fourni", style="red")
            return
        
        updated_task = update_task(task_id, title, description)
        console.print(f"✅ Tâche {task_id} modifiée avec succès", style="green")
        console.print(f"Titre: {updated_task['title']}")
        console.print(f"Description: {updated_task['description']}")
        
    except ValueError as e:
        console.print(f"❌ Erreur: {str(e)}", style="red")

@cli.command()
@click.argument('task_id', type=int)
@click.argument('status', type=click.Choice(['TODO', 'ONGOING', 'DONE']))
def status(task_id, status):
    """Changer le statut d'une tâche"""
    try:
        updated_task = change_task_status(task_id, status)
        console.print(f"✅ Statut de la tâche {task_id} changé vers {status}", style="green")
        console.print(f"Titre: {updated_task['title']}")
        console.print(f"Statut: [green]{updated_task['status']}[/green]")
        
    except ValueError as e:
        console.print(f"❌ Erreur: {str(e)}", style="red")

@cli.command()
@click.argument('task_id', type=int)
@click.confirmation_option(prompt='Êtes-vous sûr de vouloir supprimer cette tâche ?')
def delete(task_id):
    """Supprimer une tâche"""
    try:
        delete_task(task_id)
        console.print(f"✅ Tâche {task_id} supprimée avec succès", style="green")
        
    except ValueError as e:
        console.print(f"❌ Erreur: {str(e)}", style="red")

@cli.command()
@click.argument('query', required=False, default='')
@click.option('--page', '-p', default=1, type=int, help='Numéro de page')
@click.option('--size', '-s', default=20, type=int, help='Taille de page')
def search(query, page, size):
    """Rechercher des tâches par mots-clés"""
    try:
        if not query:
            query = click.prompt('Entrez votre recherche', default='', show_default=False)
        
        result = search_tasks(query, page, size)
        tasks = result["tasks"]
        pagination = result["pagination"]
        
        if not tasks:
            console.print(f"Aucune tâche trouvée pour '{query}'", style="yellow")
            return
        
        table = Table(title=f"Résultats de recherche pour '{query}' - Page {pagination['current_page']}/{pagination['total_pages']}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Statut", style="green")
        table.add_column("Titre", style="white")
        table.add_column("Description", style="dim")
        table.add_column("Créée le", style="magenta")
        
        for task in tasks:
            created_at = task.get("created_at", "")
            if created_at:
                created_at = created_at.split("T")[0]
            
            table.add_row(
                str(task["id"]),
                task['status'],
                task["title"],
                task["description"] if task["description"] else "-",
                created_at
            )
        
        console.print(table)
        console.print(f"Total: {pagination['total_tasks']} résultats | Page {pagination['current_page']}/{pagination['total_pages']}", style="dim")
    
    except ValueError as e:
        console.print(f"❌ Erreur: {str(e)}", style="red")

if __name__ == '__main__':
    console.print("Gestionnaire de Tâches - Version CLI Python\n", style="bold blue")
    cli()
