from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetCompleteView,
    PasswordResetDoneView
)
from django.shortcuts import resolve_url, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    DetailView,
    CreateView,
    UpdateView,
    ListView,
    TemplateView
)
from django.contrib import messages
from django.http import HttpResponseRedirect
from PIL import Image
from resizeimage import resizeimage
from math import floor

from .forms import (
    CustomUserCreationForm,
    CustomEditProfileForm,
    CustomEditPaymentForm,
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomPasswordChangeForm,
    AddCourseForm
)
from .models import (
    Course,
    Category,
    Cart
)
from .mixins import AnonymousRequiredMixin


class Login(AnonymousRequiredMixin, LoginView, FormView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return resolve_url('home')


class Logout(LoginRequiredMixin, LogoutView):
    pass


class SignUp(AnonymousRequiredMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class PasswordReset(AnonymousRequiredMixin, PasswordResetView):
    form_class = CustomPasswordResetForm


class PasswordResetDone(AnonymousRequiredMixin, PasswordResetDoneView):
    pass


class PasswordResetConfirm(AnonymousRequiredMixin, PasswordResetConfirmView):
    form_class = CustomSetPasswordForm


class PasswordResetComplete(AnonymousRequiredMixin, PasswordResetCompleteView):
    pass


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    pass


class EditBasicInformation(LoginRequiredMixin, UpdateView):
    form_class = CustomEditProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'editBasicInfo.html'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        obj = form.save(commit=False)
        zip_code_prefix = form['zip_code_prefix'].value()
        zip_code_suffix = form['zip_code_suffix'].value()
        obj.zip_code = zip_code_prefix + "-" + zip_code_suffix
        obj.save()
        return HttpResponseRedirect(self.success_url)


class EditPaymentInformation(EditBasicInformation):
    form_class = CustomEditPaymentForm
    template_name = 'editPaymentInfo.html'


class MyProfile(LoginRequiredMixin, DetailView):
    template_name = 'profile.html'
    context_object_name = 'user_object'

    def get_object(self, queryset=None):
        return self.request.user


class CoursesByCategoryListView(ListView):
    model = Course
    template_name = 'coursesByCategory.html'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = Course.objects.filter(course_category__id=self.kwargs['pk'])
        context['coursesByCategory'] = query
        context['coursesCount'] = query.count()
        return context


class SearchListView(ListView):
    model = Course
    template_name = 'coursesByCategory.html'
    paginate_by = 12

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        search_text = self.request.GET.get('searchInput', '')
        query = Course.objects.filter(course_name__icontains=search_text)
        context['coursesByCategory'] = query
        context['coursesCount'] = query.count()
        context['topic'] = search_text
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'course.html'


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_courses = Course.objects.all()[:6]
        context['lastCourses'] = query_courses
        query_courses_in_category = Course.objects.all()[:6]
        context['lastCoursesInCategory'] = query_courses_in_category
        query_categories = Category.objects.all()[:4]
        context['lastCategories'] = query_categories
        return context


class MyCart(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'myCart.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_list'] = self.model.objects.filter(user=self.request.user)
        context['total_price'] = self.get_total_price(self.model)
        return context

    def get_total_price(self, model):
        total_price = 0
        for cart_element in model.objects.all():
            total_price += cart_element.course.course_price
        return total_price


class Payment(LoginRequiredMixin, TemplateView):
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_fulfilled = self.request.user.is_payment_fulfilled()
        context['user_payment_info'] = payment_fulfilled
        if payment_fulfilled:
            self.delete_objects(self.request.user)
        return context

    def delete_objects(self, user):
        objects_to_delete = Cart.objects.filter(user=user)
        objects_to_delete.delete()


class AddCourse(LoginRequiredMixin, CreateView):
    form_class = AddCourseForm
    template_name = 'addCourse.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.course_author = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)


@login_required
def delete_from_cart(request, pk):
    course_to_delete = Cart.objects.filter(pk=pk)
    if course_to_delete.exists():
        course_to_delete[0].delete()
        messages.success(request, "Item has been deleted from cart")
    return redirect(reverse_lazy('myCart'))


@login_required
def add_to_cart(request, pk):
    try:
        course = Course.objects.filter(pk=pk)[0]
        course_id = course.id
        user = request.user
        cart = Cart(user=user, course=course)
        cart.save()
        message_text = "Course has been added to cart"
    except:
        message_text = "There was an error with adding course do cart. Please try again"

    messages.success(request, message_text)
    return redirect(reverse_lazy('course', kwargs={'pk': course_id}))
