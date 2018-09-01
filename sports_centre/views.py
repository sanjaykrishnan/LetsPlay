from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .forms import BookingForm
from .models import Booking, SportsCentre


class CreateGroundView(UserPassesTestMixin, CreateView):
    """
    Used to create a SportsCentre Object.

    Renders a form to the specified template_name on GET request.

    The Form will contain all the fields specified in the fields attribute.
    """
    login_url = 'sports_centre:home'
    model = SportsCentre
    fields = ['name', 'description', 'address',
              'opening_time', 'closing_time', 'image']
    template_name = 'sports_centre/create.html'
    success_url = reverse_lazy('sports_centre:home')

    def form_valid(self, form):
        """
        Add the currently logged-in user as creator and
        redirect to success_url if form is valid.
        """
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def test_func(self):
        """
        Checks whether the user trying to access the url is a staff member,
        if not redirect to login_url.
        """
        return self.request.user.is_staff


class EditGroundView(UserPassesTestMixin, UpdateView):
    """
    Used to edit a SportsCentre Object with primary key given in url.

    Renders a form to the specified template_name on GET request.

    The Form will contain all the fields specified in the fields attribute.

    A POST request will save the  edit and redirect to success_url.
    """
    login_url = 'sports_centre:home'
    model = SportsCentre
    fields = ['name', 'description', 'address',
              'opening_time', 'closing_time', 'image']
    template_name = 'sports_centre/edit.html'
    success_url = reverse_lazy('sports_centre:home')

    def test_func(self):
        """
        Checks whether the user trying to access the url
        is the creator of the sports centre,if not redirect to login_url.
        """
        return self.request.user == self.get_object().creator


class DeleteGroundView(UserPassesTestMixin, DeleteView):
    """
    Used to delete a SportsCentre Object with primary key given in url.

    Renders a confirmation message to the specified template_name
    on GET request.

    A POST request will confirm deletion and redirect to success_url.
    """
    model = SportsCentre
    success_url = reverse_lazy('sports_centre:home')
    login_url = 'sports_centre:home'
    template_name = 'sports_centre/delete.html'
    context_object_name = 'sports_centre'

    def test_func(self):
        """
        Checks whether the user trying to access the url
        is the creator of the sports centre,if not redirect to login_url.
        """
        return self.request.user == self.get_object().creator


class HomeView(ListView):
    """
    Used to list all SportsCentre Objects.

    Passes all the objects as a list to template_name on GET request.
    """
    template_name = 'sports_centre/list.html'
    context_object_name = 'sports_centre_list'

    def get(self, request):
        """
        qry is the name of the search box used to search
        objects having name,description,address same as the
        value in search box.
        """
        sports_centre_list = SportsCentre.objects.all()
        query = request.GET.get("qry")
        if query:
            sports_centre_list = sports_centre_list.filter(
                                         Q(name__contains=query) |
                                         Q(description__contains=query) |
                                         Q(address__contains=query))

        return render(request, self.template_name,
                      {'sports_centre_list': sports_centre_list})


class SportsCentreDetailView(DetailView):
    """
    Show the detail page of the SportsCentre Object
    having primary key given in url.
    """
    model = SportsCentre
    template_name = 'sports_centre/detail.html'
    context_object_name = 'sports_centre'


class BookingView(View):
    """Booking page"""
    template_name = "sports_centre/booking.html"

    def get(self, request, pk):
        """
        Pass the primary key of the sports centre to
        be booked, so that time slots can be pre-populated.
        """
        form = BookingForm(pk)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        """
        Save the bookings in multiple rows for each time slot,
        then show success message in same page.
        """
        slot_list = request.POST.getlist('slot')
        name = request.POST['name']
        date = request.POST['date']
        phone_number = request.POST['phone_number']
        for timeslot in slot_list:
            booking = Booking(name=name, slot=timeslot, date=date,
                              phone_number=phone_number)
            booking.sports_centre = SportsCentre.objects.get(pk=pk)
            booking.save()
        success_message = ("Thank you " + name + " for booking " +
                           booking.sports_centre.name + " on " + date +
                           " for time slots:<br>")
        for t in slot_list:
            success_message += t+"<br>"
        messages.success(request, success_message)
        return HttpResponseRedirect(reverse_lazy('sports_centre:book',
                                                 args=(pk,)))


class BookingListing(UserPassesTestMixin, ListView):
    """Show all the bookings in the template specified in template_name."""
    template_name = 'sports_centre/bookinglist.html'
    context_object_name = 'booking_list'
    login_url = 'accounts:profile'

    def get_queryset(self):
        """Return all Bookings."""
        return Booking.objects.all().order_by('-date')

    def test_func(self):
        """
        Checks whether the user trying to access the url
        is a staff member,if not redirect to login_url.
        """
        return self.request.user.is_staff
