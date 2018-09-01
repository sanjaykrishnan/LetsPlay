"""
Accounts Views.
"""
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm, ProfileForm, UserForm


class SignUpView(View):
    """Show the signup page."""
    form_class = UserForm
    template_name = 'accounts/signup.html'

    def get(self, request):
        """
        Renders the UserForm in template specified in template_name.
        """
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Save the user object in the model."""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:profile')

        return render(request, self.template_name, {'form': form})


@login_required(login_url='accounts:login')
def profile_view(request):
    """Profile Page with user details."""
    template_name = 'accounts/profile.html'
    return render(request, template_name)


def logout_view(request):
    """Logout the current user."""
    logout(request)

    return redirect('sports_centre:home')


class ProfileUpdate(LoginRequiredMixin, View):
    """
    Edit the Profile details of current user.
    """
    login_url = 'accounts:login'
    form_class = ProfileForm
    template_name = "accounts/update.html"
    # success_url = 'accounts:profile'

    def get(self, request):
        """Render the form to the template."""
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form': form}, )

    def post(self, request):
        """Save the changes and redirect to profile page."""
        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile")


class ContactView(View):
    """ Contact Page."""
    form_class = ContactForm
    template_name = 'accounts/contact.html'

    def get(self, request):
        """Show the Contact Page."""
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Send email notification to both admin and customer."""
        form = self.form_class(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            feedback = form.cleaned_data['feedback']

            subject = "Let's Play:Feedback"
            from_email = settings.EMAIL_HOST_USER
            to_email = [email]
            message = ("Hi "+name+",\nThank you for your feedback.\nRegards," +
                       "\nLet's Play")

            send_mail(subject, message, from_email, to_email,
                      fail_silently=False,)
            to_email = [settings.EMAIL_HOST_USER]
            message = ("Hi Admin,\nName:"+name+"\nPhone Number:"+phone +
                       "\nEmail: "+email+"\nFeedback:"+feedback+"\nthank you")

            send_mail(subject, message, from_email, to_email,
                      fail_silently=False,)
            success_message = "Thank you for your valuable feedback "+name+"!!"
            messages.success(request, success_message)
            return HttpResponseRedirect(reverse_lazy('accounts:contact'))

        return render(request, self.template_name, {'form': form})
