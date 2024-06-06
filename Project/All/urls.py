from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_views, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('advertisements/create/', views.advertisement_create, name='advertisement_create'),
    path('advertisements/<int:pk>/', views.advertisement_detail, name='advertisement_detail'),
    path('advertisements/<int:pk>/edit/', views.advertisement_edit, name='advertisement_edit'),
    path('advertisements/<int:pk>/responses/create/', views.response_create, name='response_create'),
    path('users/<int:pk>/messages/create/', views.message_create, name='message_create'),
    path('news/', views.news, name='news'),
    path('categories/', views.categories, name='categories'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('filter/', views.filter, name='filter'),
]
