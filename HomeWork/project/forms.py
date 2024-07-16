from django import forms
from django.forms import ModelForm
from django_summernote.fields import SummernoteTextFormField
from .models import Post, UserResponse


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'text', 'author']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            # 'text': forms.Textarea(attrs={'class': 'form-control'}),
            'text': SummernoteTextFormField()
        }


class EditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserResponseForm(ModelForm):
    class Meta:
        model = UserResponse
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type comment text here ...'}),
        }