from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render, HttpResponse,Http404
from django.views.generic import ListView, FormView, View,DeleteView
import razorpay
from book.models import reservation, Booking,payment
from book.forms import AvailabilityForms,PaymentForm
from book.booking_functions.availability import check_availability
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def Reserve_List(request):
    reserve = reservation.objects.all()[0]
    reserve_categories = dict(reserve.RESERVATION_CATEGORIES)
    
    reserve_values = reserve_categories.values()

    reserve_list = []
    
    for reserve_category in reserve_categories:
        reserve = reserve_categories.get(reserve_category)
        reserve_url = reverse('book:ReserveDetailView', kwargs=
                              {'category':reserve_category})
        
        reserve_list.append((reserve,reserve_url))
    
    context = { 
        'reserve_list':reserve_list,
    }
    return render(request, 'bookings/reserve_list_view.html', context)

class Booking_list(ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    def get_queryset(self,  *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list
        
class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'bookings/booking_cancel_view.html'
    success_url = reverse_lazy('book:Booking_list')

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Booking.DoesNotExist:
            raise Http404("Booking does not exist")

    def form_valid(self, form):
        return super().form_valid(form)
    
def book_location(request):
    if request.method == 'POST':
        location_name = request.POST.get("location")
        request.session['location'] = location_name
        booking_instance = Booking.objects.first()
        booking_instance.location = location_name
        booking_instance.save()
        
        return render(request, 'bookings/booking_confirmation.html', {'location_name': location_name})
    
def calculate_cost(check_in, check_out):
    # Assuming pricing logic is based on a fixed rate per hour
    # You may need to replace this with your actual pricing logic
    rate_per_hour = 1000  # Replace with your actual rate

    # Calculate the duration of stay
    duration = check_out - check_in

    # Convert duration to hours
    duration_hours = duration.total_seconds() / 3600

    # Calculate the cost based on the rate per hour
    cost = duration_hours * rate_per_hour

    return cost


class ReserveDetail_view(View):
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        reserve_List = reservation.objects.filter(category=category)
        form = AvailabilityForms

        if len(reserve_List) > 0:
            reserve = reserve_List.first()
            reserve_category = dict(reserve.RESERVATION_CATEGORIES).get(reserve.category,None)

            context = {
                'reserve_category': reserve_category,
                'form': form,   
                'reserve': reserve,
            }
            return render(request, 'bookings/reserve_detail_view.html', context)
        else:
            return HttpResponse("Category doesn't exist!")
        
    
        
        
    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        reserve_List = reservation.objects.filter(category=category)
        form = AvailabilityForms(request.POST)
        available_reserve = []
        data = {}

        if form.is_valid():
            data = form.cleaned_data
            location_name = request.session.get('location', None)
            check_in = data['check_in']
            check_out = data['check_out']
            cost = round(calculate_cost(check_in, check_out))

        for reserve in reserve_List:
            if check_availability(reserve, data.get('check_in'), data.get('check_out')):
                available_reserve.append(reserve)

        if len(available_reserve) > 0:
            reserve = available_reserve[0]
            booking = Booking.objects.create(
                user=self.request.user,
                reserve=reserve,
                check_in=check_in,
                check_out=check_out,
                location=location_name
            )
            booking.save()
            # return HttpResponse(booking)
            return render(request,"bookings/cost.html",{"cost":cost})
        else:
            return HttpResponse("This category's charging point is already booked!!! Try another Port")
    
@login_required
def handlerequest(request):
    if request.method == 'POST':
        amount = int(request.POST.get("amount")) * 100
        vehicle_number = request.POST.get("vehicle_number")
        Driving_license_number = request.POST.get("Driving_license_number")

        # create Razorpay client        
        client = razorpay.Client(auth=('rzp_test_zg7C24Itrm23JW', 'v3899ux55OZxtQHEGJ9cTbse'))

        # Create order
        response_payment = client.order.create(dict(amount=amount, currency='INR'))
        
        order_id = response_payment["id"]
        order_status = response_payment['status']
        if order_status == "created":
            user_first_name = request.user.first_name
            user_email = request.user.email 
            pay = payment(
                name=request.user,
                amount=amount,
                vehicle_number =vehicle_number,
                Driving_license_number = Driving_license_number,
                book_id = order_id
            )
            pay.save()
            response_payment["name"] = user_first_name

            form = PaymentForm(instance=pay)
            return render(request, "bookings/payment.html", {"form": form,"payment":response_payment,"email":user_email})

    form = PaymentForm()
    return render(request, "bookings/payment.html", {"form": form})

def payment_status(request):
    return render(request,"bookings/payment_status.html")