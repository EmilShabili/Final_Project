from .seralizer import (
    ProfileEditSerializer, ProfileSerializer, ExperienceSerializer, EducationSerializer, CertificationsSerializer,
    SkillsSerializer
)
from ..models import Profile, Experience, Education, Certifications, Skills
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class SkillsUpdateView(generics.UpdateAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ExperienceCreateView(generics.CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ExperienceUpdateView(generics.UpdateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ExperienceDeleteView(generics.DestroyAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    # def perform_destroy(self, instance):
    #     instance.delete()


class EducationCreateView(generics.CreateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class EducationUpdateView(generics.UpdateAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CertificationCreateView(generics.CreateAPIView):
    queryset = Certifications.objects.all()
    serializer_class = CertificationsSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class CertificationUpdateView(generics.UpdateAPIView):
    queryset = Certifications.objects.all()
    serializer_class = CertificationsSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(user=self.request.user)


class ProfileEditView(generics.UpdateAPIView):
    serializer_class = ProfileEditSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user.profile
