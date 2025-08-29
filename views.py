from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from python_stress import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage,send_mail
from .tokens import generate_token
from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse
from .models import BusInfo,AutorickshawInfo
import json
import folium
# Create your views here.

def home(request):
    return render(request,"index.html")

def signup(request):

    if request.method == "POST":
        name = request.POST['username']
        username = request.POST['email']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"this email id already registered. Try to login or use another email")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request,"passwords must match")
            return redirect('signup')
        
        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = name
        myuser.is_active = False

        myuser.save()
        messages.success(request,"Your account has been succesfully registered")

        # WELCOME EMAIL
        subject = "Welcome our website"
        message = "HELLO!" + myuser.first_name + "\nTHANK YOU for visiting our website \n We have also sent you a another email to  confirm your registration and activate account"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently =False)

        # Email Address Confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Tracking systems login"
        message_2 = render_to_string('email_confirmation.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })

        email = EmailMessage(
            email_subject,
            message_2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')


    return render(request,"signup.html")

def signin(request):
    if request.user.is_authenticated:
        return render(request, 'front_page.html', {'fname': request.user.first_name})

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)
        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "front_page.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signin')

    return render(request, "signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out succesfully")
    return redirect('home')

def signout2(request):
    if request.method == 'POST':
        # Retrieve the busNumber value from the POST data
        auto_number = request.POST.get('auto_number')
        try:
            bus_info = AutorickshawInfo.objects.get(vehicle_number=auto_number)
            # Update the existing record
            bus_info.pending_bookings_count = 0
            bus_info.is_running = False
            bus_info.save()
            logout(request)
            return redirect('home')
            
            
        except BusInfo.DoesNotExist:
            # Handle if the bus with the given bus number doesn't exist
            pass
        return HttpResponse("Error: Unable to Logout. Please try again.")



#def admin(request):
#    return render(request,"admin.html"
def front_page(request):
    return render(request,'front_page.html')


def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        return redirect('signin')
    else:
        render(request,'activation_failed.html')

def service(request):
    return render(request,'front2.html')

def service_provider(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1= request.POST['pass1']

        user = authenticate(username= username,password=pass1)
        if user is not None:
            login(request,user)
            return render(request, "bus_number.html")
        else:
            messages.error(request,"Bad Credentials!")
            redirect('home')


    return render(request,"service_provider.html")


def service_provider2(request):
    if request.method == "POST":
        vehicle_number = request.POST['username']
        key= request.POST['pass1']

        try:
            auto_info = AutorickshawInfo.objects.get(vehicle_number=vehicle_number)
            # Update the existing record
            if auto_info.vehicle_key == key:
                name = auto_info.driver_name
                auto_info.is_running = True
                return render(request, "auto_number.html",{'auto_number': vehicle_number, 'name':name})
            else:
                return render(request, "service_provider2.html")
        
        except AutorickshawInfo.DoesNotExist:
            # Handle if the bus with the given bus number doesn't exist
            pass

    return render(request, "service_provider2.html")




def update_bus_coordinates(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        bus_num = data.get('bus_number')
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        
        try:
            bus = BusInfo.objects.get(bus_number=bus_num)
            bus.latitude = latitude
            bus.longitude = longitude
            bus.save()
            return JsonResponse({'message': 'Coordinates updated successfully'})
        except BusInfo.DoesNotExist:
            return JsonResponse({'error': 'Bus not found'}, status=404)
        except ValueError:
            return JsonResponse({'error': 'Invalid latitude or longitude'}, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def update_auto_coordinates(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        auto_num = data.get('auto_number')
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        
        try:
            bus = AutorickshawInfo.objects.get(vehicle_number=auto_num)
            bus.latitude =latitude
            bus.longitude = longitude
            bus.save()
            return JsonResponse({'message': 'Coordinates updated successfully'})
        except AutorickshawInfo.DoesNotExist:
            return JsonResponse({'error': 'Auto not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def update_capacity(request):
    if request.method == 'POST':
        bus_number = request.POST.get('bus_number')
        capacity = request.POST.get('capacity')

        # Retrieve the bus object from the database
        try:
            bus = BusInfo.objects.get(bus_number=bus_number)
        except BusInfo.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Bus not found.'})

        # Update the capacity of the bus
        bus.seating_capacity = capacity
        bus.save()

        return JsonResponse({'success': True, 'message': 'Capacity updated successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})
    
def update_bookings(request):
    if request.method == 'POST':
        auto_number = request.POST.get('auto_number')
        num_bookings = request.POST.get('bookingsInput')

        # Retrieve the bus object from the database
        try:
            bus = AutorickshawInfo.objects.get(vehicle_number=auto_number)
        except AutorickshawInfo.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Bus not found.'})

        # Update the capacity of the bus
        bus.pending_bookings_count = num_bookings
        bus.save()

        return JsonResponse({'success': True, 'message': 'Capacity updated successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})

    
def save_bus_info(request):
    if request.method == 'POST':
        bus_number = request.POST.get('busNumber')
        start_point = request.POST.get('startPoint')
        destination = request.POST.get('destination')
        
        # Check if a bus with the given bus number already exists in the database
        try:
            bus_info = BusInfo.objects.get(bus_number=bus_number)
            # Update the existing record
            bus_info.starting_point = start_point
            bus_info.destination = destination
            bus_info.is_running = True
            bus_info.save()
        except BusInfo.DoesNotExist:
            # Handle if the bus with the given bus number doesn't exist
            pass
        
        # Store the data in session
        request.session['bus_number'] = bus_number
        request.session['start_point'] = start_point
        request.session['destination'] = destination
        
        # Redirect to the updater_page
        return redirect('updater_page')


def updater_page(request):
    # Retrieve data from session
    bus_number = request.session.get('bus_number')
    start_point = request.session.get('start_point')
    destination = request.session.get('destination')
    
    # Clear session data if needed
    # del request.session['bus_number']
    # del request.session['start_point']
    # del request.session['destination']
    
    # Pass data to the template
    return render(request, 'updater_page.html', {'bus_number': bus_number, 'start_point': start_point, 'destination': destination})

def bus_info(request):
    bus_info = BusInfo.objects.all()
    return render(request, 'bus_info.html', {'bus_info': bus_info})


def generate_map(request):
    if request.method == 'POST':
        # Retrieve the data from the POST request
        data = json.loads(request.body.decode('utf-8'))
        bus_number = data.get('bus_number')
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        try:
            bus_info = BusInfo.objects.get(bus_number=bus_number)
            #Update the existing record
            longitude2 = bus_info.longitude
            # longitude2 = 90.11
            latitude2 = bus_info.latitude
            # latitude2 = 26.11
            map_center = [latitude, longitude]
            map_loc = [latitude2, longitude2]
            my_map = folium.Map(location=map_loc, zoom_start=17)
            folium.Marker(
            location=map_center,
            popup='Your Location',
            icon=folium.Icon(color='red')
            ).add_to(my_map)
            folium.Marker(
            location=map_loc,
            popup='Bus Location',
            icon=folium.Icon(color='blue')
            ).add_to(my_map)
            my_map.save('templates\my_map2.html')
            print("yes")
            return render(request, 'my_map2.html')
            
            
            
        except BusInfo.DoesNotExist:
            # Handle if the bus with the given bus number doesn't exist
            print("Bus info is not found")
        
        return redirect('generate_map')
    
def map(request):
    return render(request, 'my_map2.html')
    
def generate_map2(request):
    if request.method == 'POST':
        # Retrieve the busNumber value from the POST data
        auto_number = request.POST.get('vehicleNumber')
        try:
            auto_info = AutorickshawInfo.objects.get(vehicle_number=auto_number)
            # Update the existing record
            longitude = auto_info.longitude
            latitude = auto_info.latitude
            map_center = [latitude, longitude]
            my_map = folium.Map(location=map_center, zoom_start=17)
            folium.Marker(
            location=map_center,
            popup='My Location',
            icon=folium.Icon(color='blue')
            ).add_to(my_map)
            my_map.save('templates\my_map.html')
            return render(request, 'my_map.html')
            
        except BusInfo.DoesNotExist:
            # Handle if the bus with the given bus number doesn't exist
            pass
        return redirect('generate_map2')
    
def end_trip(request):
     if request.method == 'POST':
        # Retrieve the busNumber value from the POST data
        bus_number = request.POST.get('bus_number')
        try:
            bus_info = BusInfo.objects.get(bus_number=bus_number)
            # Update the existing record
            bus_info.seating_capacity = 60
            bus_info.is_running = False
            bus_info.destination = "-"
            bus_info.starting_point="-"
            bus_info.save()
            return render(request,'end_trip.html')
            
            
        except BusInfo.DoesNotExist:
            # Handle if the bus with the given bus number doesn't exist
            pass
        return HttpResponse("Error: Unable to end trip. Please try again.")
    
    

def rickshaw_info(request):
    rickshaw_info = AutorickshawInfo.objects.all()
    return render(request, 'rickshaw_info.html', {'rickshaw_info': rickshaw_info})


'''def display_map(latitude,longitude):
    map_center = [latitude, longitude]  # Latitude and Longitude of New York City
    my_map = folium.Map(location=map_center, zoom_start=10)

    # Add a marker for the specific location
    folium.Marker(
        location=map_center,
        popup='My Location',
        icon=folium.Icon(color='blue')
    ).add_to(my_map)

    # Save the map to an HTML file
    my_map.save('my_map.html')

    # Open the HTML file in a web browser to view the map
    
    webbrowser.open('my_map.html')'''



