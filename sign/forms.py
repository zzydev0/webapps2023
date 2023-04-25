from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=128, widget=forms.TextInput)
    password = forms.CharField(label='password', max_length=256, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=128, widget=forms.TextInput)
    first_name = forms.CharField(label='first_name', max_length=128, widget=forms.TextInput)
    last_name = forms.CharField(label='last_name', max_length=128, widget=forms.TextInput)
    email = forms.EmailField(label='email', widget=forms.EmailInput)
    currency = forms.CharField(label='currency')
    password = forms.CharField(label='password', max_length=256, widget=forms.PasswordInput)
    confirmed_password = forms.CharField(label='confirmed_password', max_length=256, widget=forms.PasswordInput)
