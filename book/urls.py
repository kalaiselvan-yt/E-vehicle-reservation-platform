from django.urls import path
from .views import Reserve_List,Booking_list,ReserveDetail_view,CancelBookingView,book_location,handlerequest,payment_status

app_name = 'book'

urlpatterns = [
    path("reserve_list/", Reserve_List, name='Reserve_list'),
    path("booking_list/", Booking_list.as_view(), name='Booking_list'),
    path('reserve/<category>/', ReserveDetail_view.as_view(), name='ReserveDetailView'),
    path('booking/cancel/<int:pk>/', CancelBookingView.as_view(), name='CancelBookingView'),
    path('book_location/', book_location, name='book_location'),
    path('handlerequest/',handlerequest,name='HandleRequest'),
    path('payment_status/',payment_status,name="payment_status")

]

