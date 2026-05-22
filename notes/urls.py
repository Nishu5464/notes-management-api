from django.urls import path
from .views import notes_list, note_detail, register_user, login_user

urlpatterns = [
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('notes/', notes_list, name='notes-list'),
    path('notes/<int:pk>/', note_detail, name='notes-detail'),
]