from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from allauth.account.forms import SignupForm
from django import forms
from PIL import Image
from django.core.files import File
from .models import Profile


# UserForm,AddEmailForm


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        password1_help_text = '<ul>' \
                              '<li>Your password can\'t be too similar to your other personal information.</li>' \
                              '<li>Your password must contain at least 8 characters.</li>' \
                              '<li>Your password can\'t be a commonly used password.</li>' \
                              '<li>Your password can\'t be entirely numeric.</li>' \
                              '</ul>'
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'] = forms.CharField(max_length=30, required=True, label='First name',
                                                    widget=forms.TextInput(attrs={'placeholder': 'First name'}))
        self.fields['last_name'] = forms.CharField(max_length=30, required=True, label='Last name',
                                                   widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
        self.fields['email'] = forms.EmailField(max_length=254, required=True,
                                                help_text='Required. Enter a valid email address.',
                                                label='E-mail', widget=forms.TextInput(attrs={'placeholder': 'E-mail'}))
        self.fields['username'] = forms.CharField(required=True,
                                                  help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                                                  label='Username',
                                                  widget=forms.TextInput(attrs={'placeholder': 'Username'}))
        self.fields['password1'] = forms.CharField(required=True, help_text=password1_help_text, label='Password',
                                                   widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
        self.fields['password2'] = forms.CharField(required=True,
                                                   help_text='Enter the same password as before, for verification.',
                                                   label='Confirm Password',
                                                   widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
        self.fields['location'] = forms.CharField(max_length=30, required=False, label='Location',
                                                  widget=forms.TextInput(attrs={'placeholder': 'Location'}))
        self.fields['image'] = forms.ImageField(required=False)

        self.fields['x'] = forms.FloatField(required=False, widget=forms.HiddenInput())
        self.fields['y'] = forms.FloatField(required=False, widget=forms.HiddenInput())
        self.fields['width'] = forms.FloatField(required=False, widget=forms.HiddenInput())
        self.fields['height'] = forms.FloatField(required=False, widget=forms.HiddenInput())

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        # Add your own processing here.
        # You must return the original result.
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.set_password(self.cleaned_data['password1'])
        user.profile.location = self.cleaned_data['location']
        user.profile.image = self.cleaned_data['image']
        user.save()
        if user.profile.image:
            print('image present')
            x = self.cleaned_data.get('x')
            y = self.cleaned_data.get('y')
            w = self.cleaned_data.get('width')
            h = self.cleaned_data.get('height')
            print(x, y, w, h)
            images = Image.open(user.profile.image)
            cropped_image = images.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((600, 600), Image.ANTIALIAS)
            resized_image.save(user.profile.image.path)
        return user

    field_order = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'location', 'image', 'x',
                   'y', 'width', 'height', ]


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='First name',
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=30, required=False, label='Last name',
                                widget=forms.TextInput(attrs={'placeholder': 'Last name'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', ]


class UpdateProfileForm(forms.ModelForm):
    x = forms.FloatField(required=False, widget=forms.HiddenInput())
    y = forms.FloatField(required=False, widget=forms.HiddenInput())
    width = forms.FloatField(required=False, widget=forms.HiddenInput())
    height = forms.FloatField(required=False, widget=forms.HiddenInput())
    location = forms.CharField(max_length=30, required=False, label='Location',
                               widget=forms.TextInput(attrs={'placeholder': 'Location'}))
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['location', 'image', ]

    def save(self):
        user = super(UpdateProfileForm, self).save()
        user.location = self.cleaned_data.get('location')
        print("locations is", user.location)
        if not user.location:
            user.location = ""
        user.image = self.cleaned_data.get('image')
        print(user.image)
        user.save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        if x or y or w or h:
            print('image present')
            image = Image.open(user.image)
            cropped_image = image.crop((x, y, w + x, h + y))
            resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
            resized_image.save(user.image.path)

        return user
