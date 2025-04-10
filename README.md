1. Installation et Configuration
    *Prérequis : Node.js, Python, Django
    *Instructions d'installation :
      -Cloner le repo :git clone <url-du-repo>
      -Frontend:cd frontend
                npm install
                npm start
      -Pour le backend:cd backend
                       pip install -r requirements.txt
                       python manage.py migrate
                       python manage.py runserver

2. Fonctionnalités
Gestion des dossiers patients : Création, lecture, mise à jour et suppression (CRUD).
Gestion des diagnostics : Ajout de diagnostics aux dossiers patients.
Authentification et autorisation : Système de connexion pour les utilisateurs (médecins, administrateurs).

3. API Documentation
Endpoints : Liste des endpoints de l'API avec des descriptions, méthodes HTTP, et exemples de requêtes/réponses.
Exemple :
GET /api/patients/ : Récupérer la liste des patients.
POST /api/patients/ : Ajouter un nouveau patient.

4. Gestion des Données
Modèles de données : Description des modèles utilisés dans Django (par exemple, Patient, Diagnostic).
Base de données : Système de gestion de base de données utilisé (PostgreSQL, SQLite, etc.).

5. Déploiement
Instructions de déploiement : Comment déployer l'application sur un serveur (par exemple, Heroku, AWS).
Configuration de la production : Paramètres spécifiques pour l'environnement de production.
