from django import forms


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
