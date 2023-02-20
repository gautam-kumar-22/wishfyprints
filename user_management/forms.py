from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from address.forms import AddressField
from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=20, widget=forms.TextInput(attrs={
        'class': "box", 'placeholder': "enter your email", 'autocomplete': "off"}))
    phone_no = forms.CharField(label="Phone Number", max_length=20, widget=forms.TextInput(attrs={
        'class': "box", 'placeholder': "enter your phone number", 'autocomplete': "off"}))
    first_name = forms.CharField(label="First Name", max_length=20, widget=forms.TextInput(attrs={
        'class': "box", 'placeholder': "enter your first name", 'autocomplete': "off"}))
    last_name = forms.CharField(label="Last Name", max_length=20, widget=forms.TextInput(attrs={
        'class': "box", 'placeholder': "enter your last name", 'autocomplete': "off"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'password1', 'password2']


class AddressForm(forms.Form):
  address = AddressField()


class PaypalFormView(FormView):
    template_name = 'paypal_form.html'
    form_class = PayPalPaymentsForm

    def get_initial(self):
        return {
            "business": 'your-paypal-business-address@example.com',
            "amount": 20,
            "currency_code": "INR",
            "item_name": "Example item",
            "invoice": 1234,
            "notify_url": self.request.build_absolute_uri(reverse('paypal-ipn')),
            "return_url": self.request.build_absolute_uri(reverse('paypal-return')),
            "cancel_return": self.request.build_absolute_uri(reverse('paypal-cancel')),
            "lc": 'EN',
            "no_shipping": '1',
        }