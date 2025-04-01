from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from datetime import date, datetime, timedelta

# Importer les modèles
from .models import (
    User, Patient, DossierMedical, MaladieRenaleChronique, Consultation,
    ResultatExamen, Traitement, ParametresCliniques, ParametresBiologiques,
    Workflow, EtapeWorkflow, Notification, RendezVous, Journal, HistoriqueStadeMRC
)

# Importer les formulaires (à créer dans forms.py)
from .forms import (
    PatientForm, DossierMedicalForm, MRCForm, ConsultationForm,
    ResultatExamenForm, TraitementForm, ParametresCliniqueForm,
    ParametresBiologiqueForm, WorkflowForm, EtapeWorkflowForm,
    NotificationForm, RendezVousForm
)

# Importer les serializers (à créer dans serializers.py)
from .serializers import (
    UserSerializer, PatientSerializer, DossierMedicalSerializer,
    MaladieRenaleChronicSerializer, ConsultationSerializer,
    ResultatExamenSerializer, TraitementSerializer,
    ParametresCliniqueSerializer, ParametresBiologiqueSerializer,
    WorkflowSerializer, EtapeWorkflowSerializer,
    NotificationSerializer, RendezVousSerializer
)

# Fonctions utilitaires
def log_action(request, action, entite, identifiant_entite, details=None):
    """Enregistre une action dans le journal d'audit"""
    Journal.objects.create(
        utilisateur=request.user,
        action=action,
        entite=entite,
        identifiant_entite=str(identifiant_entite),
        details=details,
        adresse_ip=request.META.get('REMOTE_ADDR', '0.0.0.0')
    )

# Vue d'accueil
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'mrc/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()
        
        # Statistiques
        context['nb_patients'] = Patient.objects.filter(status='ACTIF').count()
        context['patients_recents'] = Patient.objects.filter(status='ACTIF').order_by('-date_enregistrement')[:5]
        
        # Rendez-vous du jour
        context['rendez_vous_aujourdhui'] = RendezVous.objects.filter(
            date_heure__date=today,
            status__in=['PLANIFIE', 'CONFIRME']
        ).order_by('date_heure')
        
        # Notifications non lues
        context['notifications'] = Notification.objects.filter(
            destinataire=self.request.user,
            status__in=['ENVOYEE', 'ATTENTE'],
            date_envoi_prevue__lte=datetime.now()
        ).order_by('-priorite', '-date_envoi_prevue')[:10]
        
        # Consultations récentes
        context['consultations_recentes'] = Consultation.objects.filter(
            medecin=self.request.user
        ).order_by('-date_heure')[:5]
        
        return context

# Vues pour Patient
class PatientListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'mrc/patient_list.html'
    context_object_name = 'patients'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Patient.objects.all()
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', 'ACTIF')
        
        # Filtrer par statut
        if status != 'TOUS':
            queryset = queryset.filter(status=status)
        
        # Recherche par nom, prénom ou numéro de dossier
        if search:
            queryset = queryset.filter(
                Q(nom__icontains=search) | 
                Q(prenom__icontains=search) | 
                Q(numero_dossier__icontains=search)
            )
        
        return queryset.order_by('nom', 'prenom')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        context['status'] = self.request.GET.get('status', 'ACTIF')
        context['nb_total'] = Patient.objects.count()
        context['nb_actifs'] = Patient.objects.filter(status='ACTIF').count()
        return context

class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'mrc/patient_detail.html'
    context_object_name = 'patient'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object
        
        # Données médicales
        try:
            context['dossier_medical'] = patient.dossier_medical
        except DossierMedical.DoesNotExist:
            context['dossier_medical'] = None
            
        try:
            context['maladie_renale'] = patient.maladie_renale
        except MaladieRenaleChronique.DoesNotExist:
            context['maladie_renale'] = None
        
        # Consultations récentes
        context['consultations'] = patient.consultations.order_by('-date_heure')[:5]
        
        # Derniers examens
        context['examens'] = patient.resultats_examens.order_by('-date_examen')[:5]
        
        # Traitements actifs
        context['traitements'] = patient.traitements.filter(status='ACTIF').order_by('-date_debut')
        
        # Derniers paramètres cliniques
        context['parametres_cliniques'] = patient.parametres_cliniques.order_by('-date_mesure').first()
        
        # Derniers paramètres biologiques
        context['parametres_biologiques'] = patient.parametres_biologiques.order_by('-date_prelevement').first()
        
        # Prochains rendez-vous
        context['rendez_vous'] = patient.rendez_vous.filter(
            date_heure__gte=datetime.now(),
            status__in=['PLANIFIE', 'CONFIRME']
        ).order_by('date_heure')[:3]
        
        # Enregistrer la visite dans le journal
        log_action(self.request, 'CONSULTATION_FICHE', 'Patient', patient.id)
        
        return context

class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = 'mrc/patient_form.html'
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.id})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Créer un dossier médical vide
        DossierMedical.objects.create(patient=self.object)
        
        # Journal
        log_action(self.request, 'CREATION', 'Patient', self.object.id)
        messages.success(self.request, f"Le patient {self.object} a été créé avec succès.")
        return response

class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = 'mrc/patient_form.html'
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.id})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request, 'MODIFICATION', 'Patient', self.object.id)
        messages.success(self.request, f"Les informations du patient {self.object} ont été mises à jour.")
        return response

class PatientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Patient
    template_name = 'mrc/patient_confirm_delete.html'
    success_url = reverse_lazy('patient_list')
    
    def test_func(self):
        # Seuls les administrateurs peuvent supprimer les patients
        return self.request.user.role == 'ADMINISTRATEUR'
    
    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        log_action(request, 'SUPPRESSION', 'Patient', patient.id)
        messages.success(request, f"Le patient {patient} a été supprimé.")
        return super().delete(request, *args, **kwargs)

# Vues pour DossierMedical
class DossierMedicalUpdateView(LoginRequiredMixin, UpdateView):
    model = DossierMedical
    form_class = DossierMedicalForm
    template_name = 'mrc/dossier_medical_form.html'
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.id})
    
    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request, 'MODIFICATION', 'DossierMedical', self.object.id)
        messages.success(self.request, "Le dossier médical a été mis à jour.")
        return response

# Vues pour MaladieRenaleChronique
class MRCCreateView(LoginRequiredMixin, CreateView):
    model = MaladieRenaleChronique
    form_class = MRCForm
    template_name = 'mrc/mrc_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['patient'] = self.patient
        return kwargs
    
    def form_valid(self, form):
        form.instance.patient = self.patient
        
        # Transaction pour créer la MRC et son premier historique
        with transaction.atomic():
            response = super().form_valid(form)
            # Créer l'entrée dans l'historique
            HistoriqueStadeMRC.objects.create(
                maladie_renale=self.object,
                stade=self.object.stade,
                date_evaluation=self.object.date_diagnostic,
                note="Stade initial au diagnostic"
            )
        
        log_action(self.request, 'CREATION', 'MaladieRenaleChronique', self.object.id)
        messages.success(self.request, "Les informations sur la maladie rénale chronique ont été enregistrées.")
        return response
        
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.patient.id})

class MRCUpdateView(LoginRequiredMixin, UpdateView):
    model = MaladieRenaleChronique
    form_class = MRCForm
    template_name = 'mrc/mrc_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['patient'] = self.object.patient
        return kwargs
    
    def form_valid(self, form):
        old_stade = MaladieRenaleChronique.objects.get(pk=self.object.pk).stade
        response = super().form_valid(form)
        
        # Si le stade a changé, ajouter une entrée dans l'historique
        if old_stade != form.instance.stade:
            HistoriqueStadeMRC.objects.create(
                maladie_renale=self.object,
                stade=self.object.stade,
                date_evaluation=date.today(),
                note=f"Mise à jour du stade de {old_stade} à {self.object.stade}"
            )
        
        log_action(self.request, 'MODIFICATION', 'MaladieRenaleChronique', self.object.id)
        messages.success(self.request, "Les informations sur la maladie rénale chronique ont été mises à jour.")
        return response
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.object.patient.id})

# Vues pour Consultations
class ConsultationListView(LoginRequiredMixin, ListView):
    model = Consultation
    template_name = 'mrc/consultation_list.html'
    context_object_name = 'consultations'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return Consultation.objects.filter(patient=self.patient).order_by('-date_heure')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context

class ConsultationCreateView(LoginRequiredMixin, CreateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'mrc/consultation_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['patient'] = self.patient
        initial['medecin'] = self.request.user
        initial['date_heure'] = datetime.now()
        return initial
    
    def form_valid(self, form):
        form.instance.patient = self.patient
        form.instance.medecin = self.request.user
        response = super().form_valid(form)
        log_action(self.request, 'CREATION', 'Consultation', self.object.id)
        messages.success(self.request, "La consultation a été enregistrée avec succès.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.patient.id})

class ConsultationDetailView(LoginRequiredMixin, DetailView):
    model = Consultation
    template_name = 'mrc/consultation_detail.html'
    context_object_name = 'consultation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        log_action(self.request, 'CONSULTATION_DETAILS', 'Consultation', self.object.id)
        return context

class ConsultationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Consultation
    form_class = ConsultationForm
    template_name = 'mrc/consultation_form.html'
    
    def test_func(self):
        # Seul le médecin qui a créé la consultation ou un administrateur peut la modifier
        consultation = self.get_object()
        return self.request.user == consultation.medecin or self.request.user.role == 'ADMINISTRATEUR'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request, 'MODIFICATION', 'Consultation', self.object.id)
        messages.success(self.request, "La consultation a été mise à jour avec succès.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('consultation_detail', kwargs={'pk': self.object.id})

# Vues pour ResultatExamen
class ResultatExamenListView(LoginRequiredMixin, ListView):
    model = ResultatExamen
    template_name = 'mrc/examen_list.html'
    context_object_name = 'examens'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return ResultatExamen.objects.filter(patient=self.patient).order_by('-date_examen')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context

class ResultatExamenCreateView(LoginRequiredMixin, CreateView):
    model = ResultatExamen
    form_class = ResultatExamenForm
    template_name = 'mrc/examen_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['patient'] = self.patient
        initial['date_examen'] = date.today()
        return initial
    
    def form_valid(self, form):
        form.instance.patient = self.patient
        response = super().form_valid(form)
        log_action(self.request, 'CREATION', 'ResultatExamen', self.object.id)
        messages.success(self.request, "Le résultat d'examen a été enregistré avec succès.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('examen_list', kwargs={'patient_id': self.patient.id})

class ResultatExamenDetailView(LoginRequiredMixin, DetailView):
    model = ResultatExamen
    template_name = 'mrc/examen_detail.html'
    context_object_name = 'examen'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        log_action(self.request, 'CONSULTATION_DETAILS', 'ResultatExamen', self.object.id)
        return context

class ResultatExamenUpdateView(LoginRequiredMixin, UpdateView):
    model = ResultatExamen
    form_class = ResultatExamenForm
    template_name = 'mrc/examen_form.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request, 'MODIFICATION', 'ResultatExamen', self.object.id)
        messages.success(self.request, "Le résultat d'examen a été mis à jour avec succès.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('examen_detail', kwargs={'pk': self.object.id})

# Vues pour Traitement
class TraitementListView(LoginRequiredMixin, ListView):
    model = Traitement
    template_name = 'mrc/traitement_list.html'
    context_object_name = 'traitements'
    paginate_by = 10
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        status = self.request.GET.get('status', 'TOUS')
        queryset = Traitement.objects.filter(patient=self.patient)
        
        if status != 'TOUS':
            queryset = queryset.filter(status=status)
            
        return queryset.order_by('-date_debut')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        context['status'] = self.request.GET.get('status', 'TOUS')
        return context

class TraitementCreateView(LoginRequiredMixin, CreateView):
    model = Traitement
    form_class = TraitementForm
    template_name = 'mrc/traitement_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['patient'] = self.patient
        initial['date_debut'] = date.today()
        return initial
    
    def form_valid(self, form):
        form.instance.patient = self.patient
        response = super().form_valid(form)
        log_action(self.request, 'CREATION', 'Traitement', self.object.id)
        messages.success(self.request, "Le traitement a été enregistré avec succès.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('traitement_list', kwargs={'patient_id': self.patient.id})

class TraitementUpdateView(LoginRequiredMixin, UpdateView):
    model = Traitement
    form_class = TraitementForm
    template_name = 'mrc/traitement_form.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        log_action(self.request, 'MODIFICATION', 'Traitement', self.object.id)
        messages.success(self.request, "Le traitement a été mis à jour avec succès.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.object.patient
        return context
    
    def get_success_url(self):
        return reverse_lazy('traitement_list', kwargs={'patient_id': self.object.patient.id})

# Vues pour ParametresCliniques
class ParametresCliniqueCreateView(LoginRequiredMixin, CreateView):
    model = ParametresCliniques
    form_class = ParametresCliniqueForm
    template_name = 'mrc/parametres_clinique_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['patient'] = self.patient
        initial['date_mesure'] = datetime.now()
        
        # Récupérer les derniers paramètres pour pré-remplir le formulaire
        derniers_params = ParametresCliniques.objects.filter(patient=self.patient).order_by('-date_mesure').first()
        if derniers_params:
            initial['taille'] = derniers_params.taille
        
        return initial
    
    def form_valid(self, form):
        form.instance.patient = self.patient
        response = super().form_valid(form)
        log_action(self.request, 'CREATION', 'ParametresCliniques', self.object.id)
        messages.success(self.request, "Les paramètres cliniques ont été enregistrés avec succès.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        context['historique'] = ParametresCliniques.objects.filter(
            patient=self.patient
        ).order_by('-date_mesure')[:5]
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.patient.id})

# Vues pour ParametresBiologiques
class ParametresBiologiqueCreateView(LoginRequiredMixin, CreateView):
    model = ParametresBiologiques
    form_class = ParametresBiologiqueForm
    template_name = 'mrc/parametres_biologique_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.patient = get_object_or_404(Patient, pk=kwargs['patient_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['patient'] = self.patient
        initial['date_prelevement'] = date.today()
        return initial
    
    def form_valid(self, form):
        form.instance.patient = self.patient
        response = super().form_valid(form)
        
        # Si DFG est renseigné, vérifier s'il faut mettre à jour le stade MRC
        if form.instance.dfg:
            try:
                mrc = self.patient.maladie_renale
                nouveau_stade = None
                
                if form.instance.dfg >= 90:
                    nouveau_stade = 1
                elif form.instance.dfg >= 60:
                    nouveau_stade = 2
                elif form.instance.dfg >= 45:
                    nouveau_stade = 3
                elif form.instance.dfg >= 30:
                    nouveau_stade = 3.5
                elif form.instance.dfg >= 15:
                    nouveau_stade = 4
                else:
                    nouveau_stade = 5
                
                # Si le stade a changé, mettre à jour et créer une notification
                if nouveau_stade and nouveau_stade != mrc.stade:
                    ancien_stade = mrc.stade
                    mrc.stade = nouveau_stade
                    mrc.save()
                    
                    # Ajouter à l'historique
                    HistoriqueStadeMRC.objects.create(
                        maladie_renale=mrc,
                        stade=nouveau_stade,
                        date_evaluation=form.instance.date_prelevement,
                        note=f"Mise à jour automatique basée sur DFG de {form.instance.dfg}"
                    )
                    
                    # Créer une notification
                    Notification.objects.create(
                        patient=self.patient,
                        destinataire=self.request.user,
                        type='ALERTE',
                        titre=f"Changement de stade MRC pour {self.patient}",
                        message=f"Le stade MRC a changé de {ancien_stade} à {nouveau_stade} suite à un DFG de {form.instance.dfg}.",
                        date_envoi_prevue=datetime.now(),
                        priorite='HAUTE',
                        status='ENVOYEE'
                    )
                    
                    messages.warning(
                        self.request,
                        f"Le stade MRC a été automatiquement mis à jour de {ancien_stade} à {nouveau_stade} suite au DFG de {form.instance.dfg}."
                    )
            except MaladieRenaleChronique.DoesNotExist:
                pass
        
        log_action(self.request, 'CREATION', 'ParametresBiologiques', self.object.id)
        messages.success(self.request, "Les paramètres biologiques ont été enregistrés avec succès.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['patient'] = self.patient
        context['historique'] = ParametresBiologiques.objects.filter(
            patient=self.patient
        ).order_by('-date_prelevement')[:5]
        return context
    
    def get_success_url(self):
        return reverse_lazy('patient_detail', kwargs={'pk': self.patient.id})

# Vues pour Workflow
class WorkflowListView(LoginRequiredMixin, ListView):
    model = Workflow
    template_name = 'mrc/workflow_list.html'
    context_object_name = 'workflows'
    
    def get_queryset(self):
        return Workflow.objects.filter(actif=True).order_by('nom')

class WorkflowDetailView(LoginRequiredMixin, DetailView):
    model = Workflow
    template_name = 'mrc/workflow_detail.html'
    context_object_name = 'workflow'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['etapes'] = self.object.etapes.all().order_by('ordre')
        return context

class WorkflowCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Workflow
    form_class = WorkflowForm
    template_name = 'mrc/workflow_form.html'
    success_url = reverse_lazy('workflow_list')
    
    def test_func(self):
        # Seuls les médecins et les administrateurs peuvent créer des workflows
        return self.request.user.role in ['MEDECIN', 'ADMINISTRATEUR']
    
    def form_valid(self, form):
        form.instance.createur = self.request.user
        response = super().form_valid(form)
        log_action(self.request, 'CREATION', 'Workflow', self.object.id)
        messages.success(self.request, "Le workflow a été créé avec succès.")
        return response

class EtapeWorkflowCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EtapeWorkflow
    form_class = EtapeWorkflowForm
    template_name = 'mrc/et