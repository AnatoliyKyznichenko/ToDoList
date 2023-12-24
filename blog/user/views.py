from django.contrib import auth
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user.forms import RegisterFormView, NoteForm
from user.models import Note
from user.forms import UserLoginForm


class MainCreateView(View):
    template_name = 'user/main.html'
    template_name2 = 'user/notes.html'

    #  Проверка на авторизацию и в зависимости от этого вывод той или иной страницы
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name2)
        else:
            # Пользователь не аутентифицирован
            return render(request, self.template_name)


class RegistrationUserView(View):
    template_name = 'user/register_user.html'

    def get(self, request, *args, **kwargs):
        form = RegisterFormView()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterFormView(request.POST)
        if form.is_valid():
            user = form.save()
            #username = form.cleaned_data['username'] получения любого поля с формы
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('user:notes_user'))
        else:
            print(form.errors)

        return render(request, self.template_name, {'form': form})


class NotesUserView(View):
    template_name = 'user/notes.html'

    def get(self, request):
        notes = Note.objects.filter(user=request.user)
        return render(request, self.template_name, {'result_notes_get': notes})


class AddNotesUserView(View):
    template_name = 'user/add_note.html'

    def get(self, request, *args, **kwargs):
        form = NoteForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()  # Теперь сохраняем измененный объект note в базе данных
            return HttpResponseRedirect(reverse('user:notes_user'))
        else:
            return render(request, 'add_note.html', {'form': form})


class LoginUserView(View):
    template_name = 'user/login_user.html'
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            print(request.user.is_authenticated)
            if user:
                #auth.login(request, user)
                login(request, user)
                return HttpResponseRedirect(reverse('user:notes_user'))
        context = {'form': form}
        return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request):
        print('hi')
        logout(request)
        return redirect('user:home')