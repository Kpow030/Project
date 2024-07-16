from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from django.urls import reverse


class Post(models.Model):
    TYPE = (
        ('tank', 'Танки'),
        ('heal', 'Хилы'),
        ('dd', 'ДД'),
        ('buyers', 'Торговцы'),
        ('gildemaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('smith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('spellmaster', 'Мастера заклинаний'),
    )
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = SummernoteTextField('Text')
    category = models.CharField(max_length=11, choices=TYPE, default='tank')
    upload = models.FileField(upload_to='uploads/')
    dateCreation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}  |  {self.author}  |  {self.dateCreation}  |  {self.category}  |  {self.text[:64]}'

    def get_absolute_url(self):
        return reverse('post', args=(str(self.id)))

    def get_categories(self):
        cat_menu = [
            'tanks',
            'heals',
            'damage dealers',
            'merchants',
            'gild masters',
            'questgivers',
            'blacksmiths',
            'leatherworkers',
            'potions makers',
            'spell masters',
        ]
        return cat_menu


class UserResponse(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    resp_date = models.DateTimeField(auto_now_add=True)