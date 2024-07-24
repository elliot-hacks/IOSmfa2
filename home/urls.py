from django.urls import path
from . import views

urlpatterns = [
    path('register_fingerprints/<int:person_id>/', views.register_fingerprints, name='register_fingerprints'),
    path('authenticate/', views.authenticate, name='authenticate'),
    path('success/', views.attendance_success, name='attendance_success'),
]
