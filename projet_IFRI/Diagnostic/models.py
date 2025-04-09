from django.contrib.auth.models import AbstractUser, User, Group, Permission
from django.db import models

class Medecin(AbstractUser):
    """ Modèle de médecin personnalisé basé sur AbstractUser """
    specialite = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        swappable = "AUTH_USER_MODEL"  # Permet de remplacer auth.User

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.specialite}"

   

class Patient(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=10, choices=[("M", "Masculin"), ("F", "Féminin")])
    adresse = models.TextField()
    telephone = models.CharField(max_length=15, blank=True, null=True)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name="patients")

    def __str__(self):
        return f"{self.nom} {self.prenom}"

class SuiviMedical(models.Model):
    STADES_MRC = [
        (1, "Stade 1 : Dommages rénaux légers"),
        (2, "Stade 2 : Légère réduction de la fonction rénale"),
        (3, "Stade 3 : Diminution modérée de la fonction rénale"),
        (4, "Stade 4 : Diminution sévère de la fonction rénale"),
        (5, "Stade 5 : Insuffisance rénale terminale"),
    ]

    TRAITEMENTS = {
        1: "Surveillance et mode de vie sain.",
        2: "Contrôle des maladies sous-jacentes.",
        3: "Médicaments pour ralentir la progression.",
        4: "Préparation à la dialyse ou greffe.",
        5: "Dialyse ou transplantation nécessaire.",
    }

    SYMPTOMES = {
        1: "Fatigue légère.",
        2: "Légère rétention d’eau, fatigue.",
        3: "Gonflement des pieds, nausées.",
        4: "Problèmes de sommeil, perte d’appétit.",
        5: "Insuffisance rénale avancée.",
    }

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="suivis")
    date_consultation = models.DateTimeField(auto_now_add=True)
    stade_mrc = models.IntegerField(default=0)
    diagnostic = models.TextField(blank=True)
    traitement = models.TextField(blank=True)
    notes = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Générer automatiquement le diagnostic et le traitement selon le stade MRC."""
        self.diagnostic = f"Stade {self.stade_mrc}: {self.SYMPTOMES.get(self.stade_mrc, 'Non défini')}"
        self.traitement = self.TRAITEMENTS.get(self.stade_mrc, "Traitement inconnu.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Consultation de {self.patient.nom} {self.patient.prenom} - {self.date_consultation.strftime('%d-%m-%Y')}"

class Notification(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE, related_name="notifications")
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    lue = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification pour {self.medecin.username} - {self.message[:50]}"


