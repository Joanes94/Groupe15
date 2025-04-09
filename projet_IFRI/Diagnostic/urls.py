from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, SuiviMedicalViewSet, MedecinViewSet, NotificationViewSet
from .views import MedecinRegisterView, MedecinLoginView, MedecinLogoutView
from .views import rapport_patient, liste_medecins 
# Création du router pour générer automatiquement les routes
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'suivis', SuiviMedicalViewSet, basename='suivi-medical')
router.register(r'medecins', MedecinViewSet, basename='medecin')
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Inclure les routes de l'API
    path('api/medecins/', liste_medecins, name='liste_medecins'),
    path('auth/register/', MedecinRegisterView.as_view(), name='medecin-register'),
    path('auth/login/', MedecinLoginView.as_view(), name='medecin-login'),
    path('auth/logout/', MedecinLogoutView.as_view(), name='medecin-logout'),
    path('api/rapport/<int:patient_id>/', rapport_patient, name='rapport-patient'),

    path("auth/password_reset/", csrf_exempt(PasswordResetView.as_view()), name="password_reset"),
    path("auth/password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("auth/reset/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("auth/reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
