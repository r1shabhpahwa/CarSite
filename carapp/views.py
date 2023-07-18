from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.urls import reverse

from .forms import OrderVehicleForm, VehicleSearch
from .models import CarType, Vehicle, LabMember, OrderVehicle
from django.shortcuts import get_object_or_404, render


def homepage(request):
    cartype_list = CarType.objects.all().order_by('-id')[:10]
    response = render(request, 'carapp/homepage.html', {'cartype_list': cartype_list})
    return response


def aboutus(request):
    session_counter = request.session.get('aboutus_counter', 0)
    session_counter += 1
    request.session['aboutus_counter'] = session_counter

    response = render(request, 'carapp/aboutus.html', {'session_counter': session_counter})
    response.set_cookie('cookie_counter', 10, max_age=10)

    return response



def cardetail(request, cartype_no):
    cartype = get_object_or_404(CarType, id=cartype_no)
    vehicle_list = cartype.vehicles.all()

    # Pass the context variables to the template
    context = {
        'car_type': cartype,
        'vehicle_list': vehicle_list
    }

    return render(request, 'carapp/cardetail.html', context=context)


class LabMembersView(View):
    def get(self, request):
        members = LabMember.objects.all()
        context = {'members': members}
        return render(request, 'carapp/lab_members.html', context)


def vehicles(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'carapp/vehicles.html', {'vehicles': vehicles})


def orderhere(request):
    msg = ''
    vehiclelist = Vehicle.objects.all()

    if request.method == 'POST':
        form = OrderVehicleForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            if order.vehicles_ordered <= order.vehicle.inventory:
                order.save()

                # Update the inventory field of the sold vehicle
                order.vehicle.inventory -= order.vehicles_ordered
                order.vehicle.save()

                msg = 'Your vehicle has been ordered'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'carapp/nosuccess_order.html', {'msg': msg})
    else:
        form = OrderVehicleForm()

    return render(request, 'carapp/orderhere.html', {'form': form, 'msg': msg, 'vehiclelist': vehiclelist})


def search_vehicle(request):
    vehicles = Vehicle.objects.all()
    selected_vehicle = None

    if request.method == 'POST':
        form = VehicleSearch(request.POST)

        if form.is_valid():
            car_name = form.cleaned_data['vehicle']
            selected_vehicle = get_object_or_404(Vehicle, car_name=car_name)

    else:
        form = VehicleSearch()

    return render(request, 'carapp/search_vehicle.html', {'form': form, 'vehicles': vehicles, 'selected_vehicle': selected_vehicle})


def login_here(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('carapp:homepage'))
            else:
                return HttpResponse('Your account is disabled')
        else:
            return HttpResponse('Login details are incorrect')
    else:
        return render(request, 'carapp/login_here.html')


@login_required
def logout_here(request):
    logout(request)
    return HttpResponseRedirect(reverse('carapp:homepage'))


@login_required
def list_of_orders(request):
    user = request.user
    if hasattr(user, 'buyer'):
        orders = OrderVehicle.objects.filter(buyer=user.buyer)
        return render(request, 'carapp/list_of_orders.html', {'orders': orders})
    else:
        return render(request, 'carapp/list_of_orders.html', {'message': 'You are not registered'})