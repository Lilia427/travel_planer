from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, TravelForm
from .models import City, Event, Hotel, Transport, Order, Planner

def home(request):
    # Головна сторінка із трьома опціями для користувача
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Неправильний логін або пароль.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def select_city(request):
    if request.method == "POST":
        form = TravelForm(request.POST)
        if form.is_valid():
            request.session['city'] = form.cleaned_data['city']
            request.session['start_date'] = str(form.cleaned_data['start_date'])
            request.session['end_date'] = str(form.cleaned_data['end_date'])
            return redirect('select_events')
    else:
        form = TravelForm()
    return render(request, 'select_city.html', {'form': form})

@login_required
def select_events(request):
    city_name = request.session.get('city')
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')

    # Логування для діагностики
    print(f"City from session: {city_name}")
    print(f"Start date: {start_date}")
    print(f"End date: {end_date}")
    print(f"Available cities: {[city.name for city in City.objects.all()]}")

    if not city_name or not start_date or not end_date:
        return redirect('select_city')

    city = get_object_or_404(City, name__iexact=city_name)
    events = Event.objects.filter(city=city, date__range=[start_date, end_date])
    hotels = Hotel.objects.filter(city=city)
    transport_options = Transport.objects.filter(city=city)

    return render(request, 'select_events.html', {
        'events': events,
        'hotels': hotels,
        'transport_options': transport_options,
    })

@login_required
def planner(request):
    # Планер для збережених подій
    planner = Planner.objects.filter(user=request.user).first()
    return render(request, 'planner.html', {'planner': planner})

@login_required
def checkout(request):
    # Сторінка оплати
    user = request.user
    order = Order.objects.filter(user=user, is_paid=False).first()

    if not order:
        return redirect('home')

    # Обчислення загальної вартості
    total_price = 0
    if order.hotel:
        total_price += order.hotel.price_per_night
    if order.transport:
        total_price += order.transport.price
    total_price += sum(event.price for event in order.events.all())
    
    # Оновлення ціни замовлення
    order.total_price = total_price
    order.save()

    return render(request, 'checkout.html', {
        'order': order,
        'total_price': total_price,
    })

@login_required
def success(request):
    # Логіка завершення оплати
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    if order:
        order.is_paid = True
        order.save()
    return render(request, 'success.html')

@login_required
def add_event_to_order(request, event_id):
    # Отримуємо замовлення користувача або створюємо нове
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)

    # Отримуємо подію
    event = get_object_or_404(Event, id=event_id)

    # Додаємо подію до замовлення
    order.events.add(event)

    # Перенаправляємо користувача на сторінку вибору подій
    return redirect('select_events')

@login_required
def add_event_to_planner(request, event_id):
    # Отримуємо планер користувача або створюємо новий
    planner, created = Planner.objects.get_or_create(user=request.user)

    # Отримуємо подію
    event = get_object_or_404(Event, id=event_id)

    # Додаємо подію до планера
    planner.events.add(event)

    # Перенаправляємо користувача на сторінку планера
    return redirect('planner')

@login_required
def add_hotel_to_order(request, hotel_id):
    # Отримуємо замовлення користувача або створюємо нове
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)

    # Отримуємо готель
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # Додаємо готель до замовлення
    order.hotel = hotel
    order.save()

    # Перенаправляємо користувача на сторінку вибору подій
    return redirect('select_events')

@login_required
def add_transport_to_order(request, transport_id):
    # Отримуємо замовлення користувача або створюємо нове
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)

    # Отримуємо транспорт
    transport = get_object_or_404(Transport, id=transport_id)

    # Додаємо транспорт до замовлення
    order.transport = transport
    order.save()

    # Перенаправляємо користувача на сторінку вибору подій
    return redirect('select_events')
