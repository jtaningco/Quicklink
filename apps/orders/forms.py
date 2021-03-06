from django import forms
from django.forms import ModelForm, inlineformset_factory
from apps.accounts.models import *
from apps.products.models import Product, Addon
from apps.orders.models import ProductOrder, OrderInformation
from django.utils.translation import ugettext_lazy as _

class PreviewOrderForm(ModelForm):
    class Meta: 
        model = ProductOrder
        fields = [ 
            'product',
            'quantity',
        ]
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.fields.NumberInput(attrs={
                'class':'quantity',
                'placeholder': '0'}),
        }
        labels = {
            'product': '',
            'quantity' : '',
        }

class OrderForm(ModelForm):
    class Meta: 
        model = ProductOrder
        fields = [
            'order',
            'product',
            'quantity',
            'instructions',
        ]
        required_fields = [
            'quantity',
        ]

        widgets = {
            'order': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'quantity': forms.fields.NumberInput(attrs={
                'class':'quantity',
                'placeholder': '0'}),
            'instructions': forms.Textarea(attrs={
                'class':'large-input default subtitle',
                'placeholder': 'Leave us a note! (Optional)'}),
        }

class CheckoutForm(forms.Form):
    BANKS = [
        ("Debit/Credit Card", _("Debit/Credit Card")),
        ("eWallet", _("eWallet")),
        ("Cash on Delivery", _("Cash on Delivery (COD)")),
    ]

    # Personal Details
    name = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Name'}),)
    email = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Email'}),)
    contact_number = forms.CharField(label='',  
        widget=forms.fields.TextInput(attrs={
        'class':'input default subtitle',
        'placeholder': 'Mobile Number'}),)

    # Shipping Address
    line1 = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'input default subtitle', 
        'placeholder': 'Address Line 1'}))
    line2 = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'input default subtitle', 
        'placeholder': 'Address Line 2'}))
    city = forms.ChoiceField(label='', 
        widget=forms.Select(attrs={
        'class': 'input default subtitle', 
        'placeholder': 'City'}),
        choices=Address.CITIES)
    province = forms.ChoiceField(label='', 
        widget=forms.Select(attrs={
        'class': 'small-input default subtitle', 
        'placeholder': 'Province'}),
        choices=Address.PROVINCES)
    postal_code = forms.CharField(label='', 
        widget=forms.fields.TextInput(attrs={
        'class': 'small-input default subtitle', 
        'placeholder': 'Postal Code'}))

    # Preferred Delivery Date
    delivery_date = forms.DateField(label='', 
        widget=forms.widgets.DateInput(attrs={
            'type': 'date'
        })
    )

    # Mode of Payment
    bank_name = forms.ChoiceField(label='', 
        widget=forms.RadioSelect(attrs={
        'class': 'default subtitle'}),
        choices=BANKS)

    # Updates
    notif_sms = forms.BooleanField(required=False, label='Receive SMS updates on order status',
        widget=forms.fields.CheckboxInput())
    notif_email = forms.BooleanField(required=False, label='Receive email updates on order status',
        widget=forms.fields.CheckboxInput())

    def __init__(self, min_date, user, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        self.fields['delivery_date'].widget.attrs.update({'min': min_date})

        if user:
            self.fields['email'].initial = user.email

            # Personal Details
            if user.role == "CUSTOMER":
                try:
                    self.fields['name'].initial = user.info_customer.customer_name
                    self.fields['contact_number'].initial = user.info_customer.customer_contact_number
                except:
                    pass
            else:
                try:
                    self.fields['name'].initial = user.info_shop.shop_name
                    self.fields['contact_number'].initial = user.info_shop.shop_contact_number
                except:
                    pass

            # Shipping Address
            try:
                self.fields['line1'].initial = user.user_address.line1
                self.fields['line2'].initial = user.user_address.line2
                self.fields['city'].initial = user.user_address.city
                self.fields['province'].initial = user.user_address.province
                self.fields['postal_code'].initial = user.user_address.postal_code
            except:
                pass   

            # Preferred Delivery Date
            try:
                self.fields['delivery_date'].initial = min_date
            except:
                pass 
    
    def save(self):
        data = self.cleaned_data
        try:
            sessionSender = CustomerInformation.objects.create(
                customer_name = data.get('name'),
                customer_email = data.get('email'),
                customer_contact_number = data.get('contact_number')
            )
            sessionSender.save()
                
            sessionAddress = Address.objects.create(
                line1 = data.get('line1'),
                line2 = data.get('line2'),                
                city = data.get('city'),
                province = data.get('province'),
                postal_code = data.get('postal_code'),
            )
            sessionAddress.save()

            orderNotifications = Notification.objects.create(
                sms = data.get('notif_sms'),
                email = data.get('notif_email')
            )
            orderNotifications.save()

            orderInfo = OrderInformation.objects.create(
                order = order,
                session_sender = sessionSender,
                session_address = sessionAddress,
                session_notifications = orderNotifications,
            )
            orderInfo.save()
        except:
            print("Form is valid, but can't save.")