from django import forms

class UserForm(forms.Form):
  username = forms.CharField(required=True)
  email = forms.EmailField(required=True)
  password = forms.CharField(required=True)
  password_confirm = forms.CharField(required=True)

  real_name = forms.CharField(required=False)
  real_surname = forms.CharField(required=False)
  birthday = forms.DateField(required=False)
  avatar = forms.FileField(required=False)


class LoginForm(forms.Form):
  username = forms.CharField(required=True)
  password = forms.CharField(required=True)
