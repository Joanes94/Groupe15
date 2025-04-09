from django.utils.timezone import now, timedelta
from .models import Consultation, Notification

def verifier_notifications():
    demain = now() + timedelta(days=1)
    
    # Rappels de RDV
    consultations_a_venir = Consultation.objects.filter(date_consultation__date=demain.date())
    for consultation in consultations_a_venir:
        Notification.objects.create(
            user=consultation.medecin.user,
            message=f"Rappel : Consultation avec {consultation.patient.nom} {consultation.patient.prenom} demain."
        )
    
    # Alertes pour suivis médicaux manqués
    suivis_attendus = SuiviMedical.objects.filter(date_consultation__lt=now() - timedelta(days=30))
    for suivi in suivis_attendus:
        Notification.objects.create(
            user=suivi.patient.user,
            message=f"Attention : Le suivi médical de {suivi.patient.nom} est en retard !"
        )
