import random
import string


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count


from .utils import send_confirmation_code
from .models import *
from .forms import (SignUpForm, Subscription, MessageForm, UnsubscribeForm, AdvertisementForm, ResponseForm,
                               LoginForm, ResponseFilterForm)


# Генерация кода подтверждения
def generate_confirmation_code():
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return code


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                send_mail(
                    'Добро пожаловать на наш сайт!',
                    'Спасибо за регистрацию на нашем сайте. Мы рады видеть вас среди наших пользователей!',
                    'from@example.com',
                    [user.email],
                    fail_silently=False,
                )
                return redirect('home')
            else:
                # Обработка неудачной аутентификации
                error_message = ("Не удалось аутентифицировать пользователя. "
                                 "Пожалуйста, проверьте имя пользователя и пароль.")
                return render(request, 'signup.html',
                              {'form': form, 'error_message': error_message})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


#Представление для создания и
# редактирования объявлений с возможностью добавления картинок,
# видео и другого контента.


@login_required
def subscriptions(request):
    subscriptions = Subscription.objects.filter(user=request.user)
    return render(request, 'subscriptions.html', {'subscriptions': subscriptions})


@login_required
def unsubscribe(request, pk):
    subscription = Subscription.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = UnsubscribeForm(request.POST)
        if form.is_valid():
            subscription.delete()
            return redirect('subscriptions')
    else:
        form = UnsubscribeForm()
    return render(request, 'unsubscribe.html', {'form': form, 'subscription': subscription})


@login_required
def message_create(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            message = Message(subject=subject, body=body, sender=request.user, recipient=recipient)
            message.save()
            return redirect('home')
    else:
        form = MessageForm()
    return render(request, 'message_create.html', {'form': form, 'recipient': recipient})


@login_required()
def advertisement_create(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm()
    return render(request, 'advertisement_create.html', {'form': form})


@login_required
def advertisement_edit(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=advertisement)
        if form.is_valid():
            advertisement = form.save()
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = AdvertisementForm(instance=advertisement)
    return render(request, 'advertisement_edit.html', {'form': form, 'advertisement': advertisement})


#Представление для отправки откликов на объявления с уведомлением пользователя на электронную почту.
@login_required
def response_create(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.advertisement = advertisement
            response.save()
            send_mail(
                'Новый отклик на ваше объявление!',
                        f'если у вас появился новый отклик на ваше объявление '
                        f'"{advertisement.title}".'
                         'from@example.com',
                        [advertisement.user.email],
                        fail_silently = False,
            )
            return redirect('advertisement_detail', pk=advertisement.pk)
    else:
        form = ResponseForm()
    return render(request, 'response_created.html', {'form': form, 'advertisement': advertisement})


def responses(request, advertisement_id):
    responses = Response.objects.filter(advertisement_id=advertisement_id)
    form = ResponseFilterForm(request.GET)
    if form.is_valid():
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            responses = responses.order_by(sort_by)
    return render(request, 'responses.html', {'responses': responses, 'form': form})



def home(request):
    advertisements = Advertisement.objects.all()
    return render(request, 'home.html', {'advertisements': advertisements})


def advertisement_detail(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    return render(request, 'advertisement_detail.html', {'advertisement': advertisement})


def login_views(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Ошибка, проверьте логин и пароль')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def news(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'news.html', {'news_list': news_list})


def categories(request):
    categories = Category.objects.all()
    return render(request, 'categories.html', {'categories' : categories})


def filter(request):
    categories = Category.objects.all()
    advertisements =Advertisement.objects.all()
    category = request.GET.get('category')
    popularity = request.GET.get('popularity')
    date_added = request.GET.get('date_added')
    if category:
        advertisements = advertisements.filter(category=category)
    if popularity:
        if popularity == 'asc':
            advertisements = advertisements.annotate(num_responses=Count('response')).order_by('num_responses')
        elif popularity == 'desc':
            advertisements = advertisements.annotate(num_responses=Count('response')).order_by('-num_responses')
    if date_added:
        if date_added == 'asc':
            advertisements = advertisements.order_by('created_at')
        elif date_added == 'desc':
            advertisements = advertisements.order_by('-created_at')
    return render(request, 'filter.html', {'categories': categories,
                                           'advertisements': advertisements})
