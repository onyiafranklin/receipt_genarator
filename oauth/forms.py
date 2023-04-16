from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):

    password = forms.CharField(max_length=60, widget=forms.PasswordInput(attrs={
        "class": "border px-4 py-4 rounded-md font-lg placeholder-zinc-400 disabled:opacity-50 focus:outline-none focus:ring-1 w-full invalid:border-red-500 invalid:focus:border-red-500 invalid:focus:ring-red-500 focus:border-sky-500 focus:ring-sky-500 border-zinc-200",
        "placeholder": "Password"
    }))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "border px-4 py-4 rounded-md font-lg placeholder-zinc-400 disabled:opacity-50 focus:outline-none focus:ring-1 w-full invalid:border-red-500 invalid:focus:border-red-500 invalid:focus:ring-red-500 focus:border-sky-500 focus:ring-sky-500 border-zinc-200",
            "placeholder": "Username"
        }
    ), max_length=60)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        user = authenticate(self.request, username=username, password=password)

        if not user:
            raise ValidationError("Invalid Credentials")

        login(self.request, user)
