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
from django.views import generic
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from django.contrib import messages
from .decorators import anonymous_required

from .forms import (
    CustomUserCreationForm,
    CustomEditProfileForm,
    CustomEditPaymentForm,
    CustomAuthenticationForm,
    CustomPasswordResetForm,
    CustomSetPasswordForm,
    CustomPasswordChangeForm
)
from .models import (
    Course,
    Category,
    Cart
)


@method_decorator(anonymous_required, name='dispatch')
class Login(LoginView, FormView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return resolve_url('home') # TODO zmienic


@method_decorator(login_required(login_url='login'), name='dispatch')
class Logout(LogoutView):
    pass


@method_decorator(anonymous_required, name='dispatch')
class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordResetDone(PasswordResetDoneView):
    pass


@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordResetConfirm(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordResetComplete(PasswordResetCompleteView):
    pass


@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordChange(PasswordChangeView):
    form_class = CustomPasswordChangeForm


@method_decorator(login_required(login_url='login'), name='dispatch')
class PasswordChangeDone(PasswordChangeDoneView):
    pass


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditBasicInformation(LoginRequiredMixin, generic.UpdateView):
    form_class = CustomEditProfileForm
    success_url = reverse_lazy('profile')
    template_name = 'editBasicInfo.html'

    def get_object(self, queryset=None):
        return self.request.user


@method_decorator(login_required(login_url='login'), name='dispatch')
class EditPaymentInformation(EditBasicInformation):
    form_class = CustomEditPaymentForm
    template_name = 'editPaymentInfo.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
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
        context['topic'] = r
        return context


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'course.html'


class HomeView(generic.TemplateView):
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


@method_decorator(login_required(login_url='login'), name='dispatch')
class MyCart(generic.ListView):
    model = Cart
    template_name = 'myCart.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = self.get_total_price(self.model)
        return context

    def get_total_price(self, model):
        total_price = 0
        for course in model.objects.all():
            total_price += course.course_price
        return total_price


@method_decorator(login_required(login_url='login'), name='dispatch')
class Payment(generic.TemplateView):
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment_fulfilled = self.request.user.is_payment_fulfilled()
        context['user_payment_info'] = payment_fulfilled
        if payment_fulfilled:
            self.delete_objects()
        return context

    def delete_objects(self):
        ss = Cart.objects.all()
        ss.delete()


def delete_from_cart(request, pk):
    course_to_delete = Cart.objects.filter(pk=pk)
    if course_to_delete.exists():
        course_to_delete[0].delete()
        messages.success(request, "Item has been deleted from cart")
    return redirect(reverse_lazy('myCart'))


def add_to_cart(request, pk):
    try:
        course = Course.objects.filter(pk=pk)[0]
        course_id = course.id
        course_name = course.course_name
        course_price = course.course_price
        cart = Cart(course_id=course_id, course_name=course_name, course_price=course_price)
        cart.save()
        message_text = "Course has been added to cart"
    except:
        message_text = "There was an error with adding course do cart. Please try again"

    messages.success(request, message_text)
    return redirect(reverse_lazy('course', kwargs={'pk': course_id}))
