from django.urls import path
from user.views import MainCreateView, RegistrationUserView, NotesUserView, AddNotesUserView, LoginUserView, LogoutView

app_name = 'user'

urlpatterns = [
    path('', MainCreateView.as_view(), name='home'),
    path('registration/', RegistrationUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('note/', NotesUserView.as_view(), name='notes_user'),
    path('add_note/', AddNotesUserView.as_view(), name='add_note'),
    path('logout/', LogoutView.as_view(), name='logout_user'),

]
