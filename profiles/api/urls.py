from django.urls import path
from . import views

urlpatterns = [
    path('experience/', views.ExperienceCreateView.as_view(), name='create-experience'),
    path('experience/update/<id>/', views.ExperienceUpdateView.as_view(), name='update-experience'),
    path('experience/delete/<id>/', views.ExperienceDeleteView.as_view(), name='delete-experience'),
    path('education/', views.EducationCreateView.as_view(), name='create-education'),
    path('education/<id>/', views.EducationUpdateView.as_view(), name='update-education'),
    path('certification/', views.CertificationCreateView.as_view(), name='create-certification'),
    path('certification/<id>/', views.CertificationUpdateView.as_view(), name='update-certification'),
    path('skills/<id>/', views.SkillsUpdateView.as_view(), name='update-skills'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update/', views.ProfileEditView.as_view(), name='update'),
]
