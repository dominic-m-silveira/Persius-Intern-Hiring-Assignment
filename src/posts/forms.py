from django import forms

from .models import Post


class PostModelForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': "Your message", 'rows': "5"}
    ))
    image = forms.ImageField(label='', widget=forms.FileInput())

    class Meta:
        model = Post
        fields = [
            # "user",
            "content",
            "image",
        ]