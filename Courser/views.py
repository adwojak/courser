from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetConfirmView
)
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import FormView

from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm
)
from .models import Course


class Login(LoginView, FormView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return resolve_url('home') # TODO zmienic


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm


class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm


class EditProfile(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('profile')
    template_name = 'edit.html'

    def get_object(self, queryset=None):
        return self.request.user


class MyProfile(LoginRequiredMixin, generic.DetailView):
    template_name = 'profile.html'
    context_object_name = 'user_object'

    def get_object(self, queryset=None):
        return self.request.user


class CoursesByCategoryListView(generic.ListView):
    model = Course
    template_name = 'coursesByCategory.html'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = Course.objects.filter(course_category__id=self.kwargs['pk'])
        context['coursesByCategory'] = query
        context['coursesCount'] = query.count()
        return context


class SearchListView(generic.ListView):
    model = Course
    template_name = 'coursesByCategory.html'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        r = self.request.GET.get('searchInput', '')
        query = Course.objects.filter(course_category__category_name__icontains=r)
        context['coursesByCategory'] = query
        context['coursesCount'] = query.count()
        return context


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'course.html'
