from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.
class reservation(models.Model):
    RESERVATION_CATEGORIES = (
        ("Level_1", "Slow"),
        ("Level_2", "Normal"),  
        ("Level_3", "Fast"),
    )
    charging_Port_number = models.IntegerField()
    category = models.CharField(max_length=11, choices=RESERVATION_CATEGORIES)

    def __str__(self):
        return f"  {self.category} with a Port no:{self.charging_Port_number}"

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reserve = models.ForeignKey(reservation, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, null=True)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()

    def __str__(self):
        return f"{self.user} Booked in location {self.location} " \
               f"From = {self.check_in.strftime('%d-%b-%Y %H:%M')} To = {self.check_out.strftime('%d-%b-%Y %H:%M')}"
    
    def get_reserve_category(self):
        reserve_categories = dict(self.reserve.RESERVATION_CATEGORIES)
        reserve_category = reserve_categories.get(self.reserve.category)
        return reserve_category
    
    def get_cancel_booking_url(self):
        return reverse_lazy('book:CancelBookingView', args=[self.pk, ])

class payment(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.CharField(max_length=100)
    vehicle_number = models.CharField(max_length=100)
    Driving_license_number = models.CharField(max_length=100)
    book_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} is paid {self.amount} with booking Id :{self.book_id}"