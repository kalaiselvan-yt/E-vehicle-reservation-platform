from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .location import all_locations
from book.models import Booking 
from .calculation import calculate_capacity


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsRegressor

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist , try with another Username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email is already in use. Please use a different email.")
            return redirect('home')

        my_user = User.objects.create_user(username, email, pass1)
        my_user.first_name = fname
        my_user.last_name = lname

        my_user.save()

        messages.success(request, "you are Account as been successfully created.")

        return redirect('home')


    return render(request, "authentication/signup.html")

def signin(request):
    
    if request.method == 'POST':
        username = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        selected_source = request.POST.get('source')
        selected_destination = request.POST.get('destination')
        vehicle_name = request.POST.get('vehicle')
        charge = request.POST.get('userInput')
        Predicted_range = calculate_capacity(vehicle_name, charge)
        
        df = pd.read_excel("C:\\Users\\kalai\\Desktop\\projects for iv year\\dataset\\FEV data.xlsx")

        # Separate numeric and non-numeric columns
        numeric_cols = df.select_dtypes(include='number').columns
        non_numeric_cols = df.columns.difference(numeric_cols)

        # Handle NaN values for numeric columns
        imputer = SimpleImputer(strategy='mean')
        df_imputed_numeric = pd.DataFrame(imputer.fit_transform(df[numeric_cols]), columns=numeric_cols)

        # Combine imputed numeric columns with non-numeric columns
        df_imputed = pd.concat([df[non_numeric_cols], df_imputed_numeric], axis=1)

        # Features and target variable
        features = [
            'Battery capacity [kWh]', 'Engine power [KM]', 'Maximum torque [Nm]',
            'Wheelbase [cm]', 'Length [cm]', 'Width [cm]', 'Height [cm]',
            'Minimal empty weight [kg]','Permissable gross weight [kg]',
            'Maximum load capacity [kg]', 'Number of seats', 'Number of doors',
            'Tire size [in]', 'Maximum speed [kph]', 'Boot capacity (VDA) [l]',
            'Acceleration 0-100 kph [s]', 'Maximum DC charging power [kW]',
            'mean - Energy consumption [kWh/100 km]'
        ]

        target = 'Range (WLTP) [km]'

        X = df_imputed[features]
        y = df_imputed[target]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        knn_regressor = KNeighborsRegressor(n_neighbors=5)
        knn_regressor.fit(X_train_scaled, y_train)

        def predict_ev_range(capacity,leng,power,torque,base,wid,hei,min_wei,gross_wei,mean,max_char,
                            max_load,seat,door,size,max_speed,boost_capacity,accel):
            user_input = pd.DataFrame({
                'Battery capacity [kWh]': capacity,
                'Engine power [KM]': power,
                'Maximum torque [Nm]': torque,
                'Wheelbase [cm]': base,
                'Length [cm]': leng,
                'Width [cm]': wid,
                'Height [cm]': hei,
                'Minimal empty weight [kg]': min_wei,
                'Permissable gross weight [kg]':gross_wei,
                'Maximum load capacity [kg]': max_load,
                'Number of seats': seat,
                'Number of doors': door,
                'Tire size [in]': size,
                'Maximum speed [kph]': max_speed,
                'Boot capacity (VDA) [l]': boost_capacity,
                'Acceleration 0-100 kph [s]': accel,
                'Maximum DC charging power [kW]': max_char,
                'mean - Energy consumption [kWh/100 km]': mean,
            }, index=[0])

            user_input_scaled = scaler.transform(user_input)

            predicted_range = knn_regressor.predict(user_input_scaled)[0]
        
        if selected_source in all_locations and selected_destination in all_locations[selected_source]:
            location_data = all_locations[selected_source][selected_destination]
            max_distance = max([data['distance'] for data in location_data.values()])
            return render(request, "authentication/locations.html", {'source': selected_source, 'destination': selected_destination, 'location_data': location_data ,'index':Predicted_range, 'max_distance': max_distance})

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name 
            if not fname:
                fname = username
            return redirect('confirm', fname=fname)
        else:
            messages.error(request, "Bad credentials!")
            return redirect('home')  

    return render(request, "authentication/signin.html")


def confirm(request, fname):
    return render(request, "authentication/confirm.html", {"fname": fname})

def book_location(request):
    if request.method == 'POST':
        location_name = request.POST.get("location")
        request.session['location'] = location_name
        booking_instance = Booking.objects.first()
        if booking_instance:
            booking_instance.location = location_name
            booking_instance.save()
            
            return render(request, 'bookings/booking_confirmation.html', {'location_name': location_name})
        else:
            return HttpResponse("Booking instance not found!")
    return redirect('home')


def signout(request):
    logout(request)
    messages.success(request, "Logged Out successfully")
    return redirect('home')

def about(request):
    return render(request,"authentication/about.html")

def service(request):
    return render(request,"authentication/service.html")

def contact(request):
    return render(request,"authentication/contact.html")

