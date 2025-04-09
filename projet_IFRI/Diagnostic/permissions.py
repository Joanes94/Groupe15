from rest_framework import permissions

class IsMedecin(permissions.BasePermission):
    """
    Permission pour s'assurer que seul un médecin peut accéder aux données des patients.
    """

    def has_permission(self, request, view):
        # Vérifie si l'utilisateur est authentifié et est un médecin
        return request.user.is_authenticated and hasattr(request.user, 'specialite')
