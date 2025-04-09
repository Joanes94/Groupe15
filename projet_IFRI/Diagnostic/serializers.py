from rest_framework import serializers
from .models import Patient, Medecin, SuiviMedical, Notification
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Patient
from datetime import datetime


Medecin = get_user_model()

class PatientSerializer(serializers.ModelSerializer):
    date_naissance = serializers.DateField(format="%d/%m/%Y", input_formats=['%d/%m/%Y'])
    class Meta:
        model = Patient
        fields = ['id', 'nom', 'prenom', 'date_naissance', 'sexe', 'adresse' , 'telephone', 'medecin']
        read_only_fields = ['medecin']  # Le médecin ne doit pas être modifiable via l'API

    def create(self, validated_data):
        # Associer automatiquement le patient au médecin connecté
        request = self.context.get('request')
        validated_data['medecin'] = request.user
        return super().create(validated_data)

class SuiviMedicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuiviMedical
        fields = ['id', 'patient', 'date_consultation', 'stade_mrc', 'diagnostic', 'traitement', 'notes']
        read_only_fields = ['diagnostic', 'traitement']


class MedecinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medecin
        fields = ['id', 'username', 'first_name', 'last_name', 'specialite', 'telephone']


# Gestion de comptes médécins #

class MedecinSerializer(serializers.ModelSerializer):
    """ Serializer pour afficher les informations du médecin """
    class Meta:
        model = Medecin
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'specialite', 'telephone']

class MedecinRegistrationSerializer(serializers.ModelSerializer):
    """ Serializer pour l'inscription des médecins """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Medecin
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'specialite', 'telephone']

    def create(self, validated_data):
        """ Création du médecin avec mot de passe haché """
        user = Medecin.objects.create_user(**validated_data)
        return user

class MedecinLoginSerializer(serializers.Serializer):
    """ Serializer pour la connexion des médecins """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """ Vérification des identifiants et génération du token JWT """
        from django.contrib.auth import authenticate

        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Nom d'utilisateur ou mot de passe incorrect")

        # Génération des tokens JWT
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': MedecinSerializer(user).data
        }


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'medecin','patient', 'message', 'date_creation', 'lue']



class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Aucun utilisateur avec cet email.")
        return value        