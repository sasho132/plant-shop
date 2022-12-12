from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views, get_user_model, login
from plant_shop.accounts.forms import SignInForm, SignUpForm, UserForm, UserProfileForm
from plant_shop.accounts.models import UserProfile
from plant_shop.orders.models import Order, OrderProduct
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings

UserModel = get_user_model()


class SignInView(auth_views.LoginView):
    template_name = 'accounts/sign-in-page.html'
    success_url = reverse_lazy('store')
    form_class = SignInForm


class SignUpView(views.CreateView):
    template_name = 'accounts/sign-up-page.html'
    model = UserModel
    success_url = reverse_lazy('store')
    form_class = SignUpForm

    def form_valid(self, form):
        """If the form is valid, save the associated model and log the user in."""
        user = form.save()
        login(self.request, user)

        return redirect(self.success_url)


class SignOutView(auth_views.LogoutView):
    next_page = reverse_lazy('home-page')


@login_required
def dashboard_view(request):
    orders = Order.objects.order_by('-created_at') \
        .filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    context = {
        'order_count': orders_count,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def my_orders_view(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'accounts/my-orders.html', context)


@login_required
def profile_edit_view(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile-edit')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': user_profile,
    }
    return render(request, 'accounts/profile-edit.html', context)


@login_required
def change_password_view(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = UserModel.objects.filter(email=request.user.email).get()

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password updated successfully.')
                return redirect('profile-password-change')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('profile-password-change')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/profile-change-password.html')


@login_required
def order_detail_view(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)

    context = {
        'order_detail': order_detail,
        'order': order,
    }
    return render(request, 'accounts/order-detail.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if UserModel.objects.filter(email=email).exists():
            user = UserModel.objects.filter(email__exact=email).get()
            current_site = get_current_site(request)

            email_content = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                subject='Reset Your Password',
                message=strip_tags(email_content),
                html_message=email_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=(user.email,),
            )

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login-user')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset-password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login-user')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = UserModel.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login-user')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset-password')
    else:
        return render(request, 'accounts/reset_password.html')
