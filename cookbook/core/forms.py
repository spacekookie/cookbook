from django import forms

class UserForm(forms.Form):

	username = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True)
	password_confirm = forms.CharField(required=True)

	
