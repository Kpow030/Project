from django.db import models
from django.contrib.auth.models import User, Group, Permission


# Модель  для хранения информации о пользователях, такой как имя, электронная почта, пароль и т.д.
class Title(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='titles/')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    profile_name = models.CharField(max_length=255, unique=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',
        related_query_name='custom_user',
    )


# Модель  для хранения информации о объявлениях, такой как заголовок, текст, категория и т.д.
class Advertisement(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='advertisements/images/', blank=True, null=True)
    video = models.FileField(upload_to='advertisements/videos/', blank=True, null=True)

# Модель  для хранения информации о откликах на объявления, такой как текст, пользователь,
# который отправил отклик и т.д.


class Response(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

# Модель  для хранения информации о категориях объявлений,
# такой как название категории и т.д.


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_message', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_date = models.DateTimeField(auto_now_add=True)


class Newsletter(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)