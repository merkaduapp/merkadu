from django import forms

from app.models import Product, Order, Market, ProdutoCatalogo
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

User = CustomUser

class UserForm(UserCreationForm):
    email = forms.CharField(max_length = 254, required = True, widget = forms.EmailInput())
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )


class ProductForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        ('', '---------'),
        ('drinks', 'Bebidas'),
        ('grocery_store', 'Mercearia'),
        ('cleaning_products', 'Produtos de Limpeza'),
        ('personal_hygiene', 'Higiene Pessoal'),
        ('medicines', 'Medicamentos'),
    )
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)
    class Meta:
        model = Product
        fields = ('category', 'market','name', 'is_active' ,'descript', 'value', 'offer_value', 'quantity_in_stock', 'image',  'produto_catalogo')
        exclude = ['market']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == "market":
                visible.field.widget.attrs['class'] = 'hidden'

    produto_catalogo = forms.ModelChoiceField(queryset=ProdutoCatalogo.objects.all(), required=False)



class OrderForm(forms.ModelForm):    
    STATUS_CHOICES =(
        ("Pendente", "Pendente"),
        ("Em entrega", "Em entrega"),
        ("Finalizado", "Finalizado"),
    )
  
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    class Meta:
        model = Order
        fields = (
            'status',
        )

class MarketForm(forms.ModelForm):
    latitude = forms.CharField(widget=forms.TextInput(attrs={'id':'latitude'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'id':'longitude'}))
    class Meta:
        model = Market
        fields = (
            'name', 
            'cnpj', 
            'bank', 
            'bank_account', 
            'bank_agency', 
            'pix',
            'phone_number',
            'delivery_fee',
            'min_order_value',
            'adress_street',
            'adress_number',
            'adress_district',
            'city',
            'state',
            'latitude',
            'longitude',
            'logotipo',
        )


class CustomUserCreationForm(UserCreationForm):
    # Adicione campos adicionais, se necessário
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
