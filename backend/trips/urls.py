from django.urls import path
from . import views

urlpatterns = [
    # Головна сторінка
    path('', views.home, name='home'),
    
    # Реєстрація, вхід, вихід
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Вибір міста і подій
    path('select-city/', views.select_city, name='select_city'),
    path('select-events/', views.select_events, name='select_events'),
    
    # Планер для збереження подій
    path('planner/', views.planner, name='planner'),
    
    # Оплата
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success, name='success'),

    # Додавання до замовлення
    path('add-event-to-order/<int:event_id>/', views.add_event_to_order, name='add_event_to_order'),
    path('add-event-to-planner/<int:event_id>/', views.add_event_to_planner, name='add_event_to_planner'),
    path('add-hotel-to-order/<int:hotel_id>/', views.add_hotel_to_order, name='add_hotel_to_order'),
    path('add-transport-to-order/<int:transport_id>/', views.add_transport_to_order, name='add_transport_to_order'),
]
