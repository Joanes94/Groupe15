from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class User(AbstractUser):
    ROLE_CHOICES = (
        ('MEDECIN', 'Médecin'),
        ('INFIRMIER', 'Infirmier'),
        ('ADMINISTRATEUR', 'Administrateur'),
    )
    
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='MEDECIN')
    specialite = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"

class Patient(models.Model):
    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('A', 'Autre'),
    )
    
    STATUS_CHOICES = (
        ('ACTIF', 'Actif'),
        ('INACTIF', 'Inactif'),
        ('DECEDE', 'Décédé'),
    )
    
    numero_dossier = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIF')
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    medecin_referent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='patients')
    
    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
    
    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.numero_dossier})"
    
    def save(self, *args, **kwargs):
        if not self.numero_dossier:
            self.numero_dossier = f"MRC-{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)

class DossierMedical(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='dossier_medical')
    antecedents_medicaux = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    groupe_sanguin = models.CharField(max_length=10, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dossier Médical'
        verbose_name_plural = 'Dossiers Médicaux'
    
    def __str__(self):
        return f"Dossier de {self.patient}"

class MaladieRenaleChronique(models.Model):
    STADE_CHOICES = (
        (1, 'Stade 1 (DFG ≥ 90)'),
        (2, 'Stade 2 (DFG 60-89)'),
        (3, 'Stade 3a (DFG 45-59)'),
        (3.5, 'Stade 3b (DFG 30-44)'),
        (4, 'Stade 4 (DFG 15-29)'),
        (5, 'Stade 5 (DFG < 15)'),
    )
    
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='maladie_renale')
    stade = models.FloatField(choices=STADE_CHOICES, default=1)
    date_diagnostic = models.DateField()
    etiologie = models.CharField(max_length=200, blank=True, null=True)
    dialyse = models.BooleanField(default=False)
    date_debut_dialyse = models.DateField(blank=True, null=True)
    greffe = models.BooleanField(default=False)
    date_greffe = models.DateField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Maladie Rénale Chronique'
        verbose_name_plural = 'Maladies Rénales Chroniques'
    
    def __str__(self):
        return f"MRC Stade {self.stade} - {self.patient}"

class HistoriqueStadeMRC(models.Model):
    maladie_renale = models.ForeignKey(MaladieRenaleChronique, on_delete=models.CASCADE, related_name='historique_stades')
    stade = models.FloatField(choices=MaladieRenaleChronique.STADE_CHOICES)
    date_evaluation = models.DateField()
    note = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Historique de Stade MRC'
        verbose_name_plural = 'Historiques de Stades MRC'
        ordering = ['-date_evaluation']
    
    def __str__(self):
        return f"Stade {self.stade} ({self.date_evaluation}) - {self.maladie_renale.patient}"

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultations')
    medecin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='consultations_effectuees')
    date_heure = models.DateTimeField()
    motif = models.CharField(max_length=200)
    observations = models.TextField(blank=True, null=True)
    prescriptions = models.TextField(blank=True, null=True)
    recommandations = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'
        ordering = ['-date_heure']
    
    def __str__(self):
        return f"Consultation du {self.date_heure} - {self.patient}"

class ResultatExamen(models.Model):
    TYPE_CHOICES = (
        ('BIOLOGIE', 'Examen de biologie'),
        ('IMAGERIE', 'Examen d\'imagerie'),
        ('AUTRE', 'Autre type d\'examen'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='resultats_examens')
    type_examen = models.CharField(max_length=15, choices=TYPE_CHOICES)
    nom_examen = models.CharField(max_length=200)
    date_examen = models.DateField()
    resultats = models.TextField()
    interpretation = models.TextField(blank=True, null=True)
    fichier = models.FileField(upload_to='examens/', blank=True, null=True)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Résultat d\'Examen'
        verbose_name_plural = 'Résultats d\'Examens'
        ordering = ['-date_examen']
    
    def __str__(self):
        return f"{self.nom_examen} du {self.date_examen} - {self.patient}"

class Traitement(models.Model):
    STATUS_CHOICES = (
        ('ACTIF', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('INTERROMPU', 'Interrompu'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='traitements')
    medicament = models.CharField(max_length=200)
    posologie = models.CharField(max_length=200)
    frequence = models.CharField(max_length=100)
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ACTIF')
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Traitement'
        verbose_name_plural = 'Traitements'
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"{self.medicament} - {self.patient}"

class ParametresCliniques(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='parametres_cliniques')
    date_mesure = models.DateTimeField()
    tension_arterielle_systolique = models.IntegerField(validators=[MinValueValidator(60), MaxValueValidator(300)])
    tension_arterielle_diastolique = models.IntegerField(validators=[MinValueValidator(30), MaxValueValidator(200)])
    poids = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    taille = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(250)], help_text="Taille en cm")
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Paramètres Cliniques'
        verbose_name_plural = 'Paramètres Cliniques'
        ordering = ['-date_mesure']
    
    def __str__(self):
        return f"Paramètres du {self.date_mesure} - {self.patient}"
    
    @property
    def imc(self):
        """Calcul de l'IMC (Indice de Masse Corporelle)"""
        return round(self.poids / ((self.taille/100) ** 2), 2) if self.taille else None

class ParametresBiologiques(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='parametres_biologiques')
    date_prelevement = models.DateField()
    creatinine = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="µmol/L")
    dfg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="mL/min/1.73m²")
    proteinurie = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="g/24h")
    albuminurie = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="mg/g")
    sodium = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="mmol/L")
    potassium = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="mmol/L")
    uree = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="mmol/L")
    hemoglobine = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="g/dL")
    calcium = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="mmol/L")
    phosphore = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="mmol/L")
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Paramètres Biologiques'
        verbose_name_plural = 'Paramètres Biologiques'
        ordering = ['-date_prelevement']
    
    def __str__(self):
        return f"Bilan du {self.date_prelevement} - {self.patient}"

class Workflow(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    createur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workflows_crees')
    stade_mrc_cible = models.FloatField(choices=MaladieRenaleChronique.STADE_CHOICES, null=True, blank=True)
    actif = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflows'
    
    def __str__(self):
        return f"{self.nom} (Stade {self.stade_mrc_cible if self.stade_mrc_cible else 'tous'})"

class EtapeWorkflow(models.Model):
    TYPE_CHOICES = (
        ('EXAMEN', 'Examen médical'),
        ('RENDEZ_VOUS', 'Rendez-vous'),
        ('TRAITEMENT', 'Traitement'),
        ('SURVEILLANCE', 'Surveillance'),
        ('EDUCATION', 'Éducation thérapeutique'),
    )
    
    PERIODICITE_CHOICES = (
        ('UNIQUE', 'Une seule fois'),
        ('QUOTIDIEN', 'Quotidien'),
        ('HEBDOMADAIRE', 'Hebdomadaire'),
        ('MENSUEL', 'Mensuel'),
        ('TRIMESTRIEL', 'Trimestriel'),
        ('SEMESTRIEL', 'Semestriel'),
        ('ANNUEL', 'Annuel'),
    )
    
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='etapes')
    ordre = models.PositiveIntegerField()
    nom = models.CharField(max_length=100)
    description = models.TextField()
    type_action = models.CharField(max_length=15, choices=TYPE_CHOICES)
    periodicite = models.CharField(max_length=15, choices=PERIODICITE_CHOICES, default='UNIQUE')
    conditions_declenchement = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Étape de Workflow'
        verbose_name_plural = 'Étapes de Workflow'
        ordering = ['workflow', 'ordre']
    
    def __str__(self):
        return f"{self.workflow.nom} - Étape {self.ordre}: {self.nom}"

class Notification(models.Model):
    TYPE_CHOICES = (
        ('ALERTE', 'Alerte'),
        ('RAPPEL', 'Rappel'),
        ('INFO', 'Information'),
    )
    
    PRIORITE_CHOICES = (
        ('HAUTE', 'Haute'),
        ('MOYENNE', 'Moyenne'),
        ('BASSE', 'Basse'),
    )
    
    STATUS_CHOICES = (
        ('ATTENTE', 'En attente'),
        ('ENVOYEE', 'Envoyée'),
        ('LUE', 'Lue'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notifications')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_recues')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    titre = models.CharField(max_length=200)
    message = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_envoi_prevue = models.DateTimeField()
    date_lecture = models.DateTimeField(null=True, blank=True)
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='MOYENNE')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ATTENTE')
    
    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-date_envoi_prevue', '-priorite']
    
    def __str__(self):
        return f"{self.type} - {self.titre} ({self.patient})"

class RendezVous(models.Model):
    TYPE_CHOICES = (
        ('CONSULTATION', 'Consultation'),
        ('EXAMEN', 'Examen médical'),
        ('DIALYSE', 'Séance de dialyse'),
        ('EDUCATION', 'Éducation thérapeutique'),
        ('AUTRE', 'Autre type de rendez-vous'),
    )
    
    STATUS_CHOICES = (
        ('PLANIFIE', 'Planifié'),
        ('CONFIRME', 'Confirmé'),
        ('ANNULE', 'Annulé'),
        ('REALISE', 'Réalisé'),
        ('MANQUE', 'Non présenté'),
    )
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='rendez_vous')
    medecin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rendez_vous_programmes')
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    date_heure = models.DateTimeField()
    duree_minutes = models.PositiveIntegerField(default=30)
    motif = models.CharField(max_length=200)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PLANIFIE')
    date_creation = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Rendez-vous'
        verbose_name_plural = 'Rendez-vous'
        ordering = ['-date_heure']
    
    def __str__(self):
        return f"{self.type} le {self.date_heure} - {self.patient}"

class Journal(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions_journal')
    action = models.CharField(max_length=200)
    entite = models.CharField(max_length=100)
    identifiant_entite = models.CharField(max_length=100)
    details = models.TextField(blank=True, null=True)
    date_heure = models.DateTimeField(auto_now_add=True)
    adresse_ip = models.GenericIPAddressField()
    
    class Meta:
        verbose_name = 'Journal d\'Audit'
        verbose_name_plural = 'Journal d\'Audit'
        ordering = ['-date_heure']
    
    def __str__(self):
        return f"{self.utilisateur} - {self.action} {self.entite} ({self.date_heure})"