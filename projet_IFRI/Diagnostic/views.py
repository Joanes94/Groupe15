from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets, permissions, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Patient, SuiviMedical, Medecin, Notification
from .serializers import (
    PatientSerializer, SuiviMedicalSerializer, MedecinSerializer, 
    NotificationSerializer, PasswordResetSerializer, MedecinRegistrationSerializer, MedecinLoginSerializer
)
from .permissions import IsMedecin
from django.contrib.auth import get_user_model


Medecin = get_user_model()

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsMedecin]

    def get_queryset(self):
        return self.queryset.filter(medecin=self.request.user)

    def perform_create(self, serializer):
        serializer.save(medecin=self.request.user)

class SuiviMedicalViewSet(viewsets.ModelViewSet):
    queryset = SuiviMedical.objects.all()
    serializer_class = SuiviMedicalSerializer
    permission_classes = [permissions.IsAuthenticated, IsMedecin]

    def get_queryset(self):
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            return SuiviMedical.objects.filter(patient_id=patient_id).order_by('-date_consultation')
        return SuiviMedical.objects.none()

class MedecinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer
    permission_classes = [permissions.IsAuthenticated]

def liste_medecins(request):
    if request.method == "GET":
        query = request.GET.get("nom", "")  # Récupérer le paramètre 'nom' depuis l'URL
        medecins = User.objects.filter(is_staff=True)

        # Appliquer le filtre si un nom est fourni
        if query:
            medecins = medecins.filter(first_name__icontains=query) | medecins.filter(last_name__icontains=query)

        medecins_list = medecins.values("id", "username", "email", "first_name", "last_name")
        return JsonResponse(list(medecins_list), safe=False)


# Inscription, Connexion et Déconnexion des médecins

class MedecinRegisterView(generics.CreateAPIView):
    queryset = Medecin.objects.all()
    serializer_class = MedecinRegistrationSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class MedecinLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = MedecinLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class MedecinLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Déconnexion réussie"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Token invalide"}, status=status.HTTP_400_BAD_REQUEST)

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('-date_creation')
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'medecin'):
            return Notification.objects.filter(medecin=user.medecin)
        elif hasattr(user, 'patient'):
            return Notification.objects.filter(patient=user.patient)
        return Notification.objects.none()

@api_view(['GET'])
@csrf_exempt  # Désactiver CSRF pour cette vue
@permission_classes([IsAuthenticated])
def rapport_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    suivis = SuiviMedical.objects.filter(patient=patient)

    rapport = {
        "patient": f"{patient.nom} {patient.prenom}",
        "nombre_suivis": suivis.count(),
        "dernier_diagnostic": suivis.last().diagnostic if suivis.exists() else "Aucun suivi",
        "dernier_traitement": suivis.last().traitement if suivis.exists() else "Aucun traitement",
    }
    return Response(rapport)

@method_decorator(csrf_exempt, name='dispatch')
class PasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()
            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"http://127.0.0.1:8000/auth/reset/{uid}/{token}/"
                send_mail(
                    "Réinitialisation de votre mot de passe",
                    f"Utilisez ce lien pour réinitialiser votre mot de passe : {reset_url}",
                    "noreply@tonsite.com",
                    [email],
                    fail_silently=False,
                )
            return Response({"message": "Un email a été envoyé si l'adresse existe."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
