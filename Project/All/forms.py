from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


#Форма регистрации пользователей с подтверждением по электронной почты.
class SignUpForm(UserCreationForm):
    title = forms.ModelChoiceField(queryset=Title.objects.all())

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'title')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            profile = Profile(user=user, title=self.cleaned_data['title'])
            profile.save()
        return user


# Форма создания и редактирования объявлений с
# возможностью добавления картинок, видео и другого контента.
class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ('title', 'text', 'category', 'image', 'video')


# Форма отправки откликов на объявления с уведомлением пользователя на электронную почту.
class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text',)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class MessageForm(forms.Form):
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)


class UnsubscribeForm(forms.Form):
    pass


class ResponseFilterForm(forms.Form):
    SORT_CHOICES = (
        ('created_at', 'По дате'),
        ('user__username', 'По имени пользователя'),
    )
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, required=False)


