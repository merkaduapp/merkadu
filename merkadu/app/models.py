from django.db import models
# from core.models import User
# from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser, Permission, BaseUserManager
import uuid
import os
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_webp_extension(value):
    """
    Valida se o arquivo possui a extensão .webp.
    """
    if not value.name.endswith('.webp'):
        raise ValidationError(_('Apenas arquivos WebP são permitidos.'))

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo Email é obrigatório.')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='customuser_set'  # Adicione o related_name
    )

    objects = CustomUserManager()

    def __str__(self):
        return self.username

# class Parceiro(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     nome = models.CharField(max_length=100)
#     cidade = models.CharField(max_length=50)
#     email = models.EmailField()
#     telefone = models.CharField(max_length=15)
#     descricao = models.TextField()
#     data_cadastro = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nome
    
# class Lojista(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     nome = models.CharField(max_length=100)
#     cidade = models.CharField(max_length=50)
#     email = models.EmailField()
#     telefone = models.CharField(max_length=15)
#     descricao = models.TextField()
#     data_cadastro = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.nome

def image_dir_path_products(instance, filename):
    extension = filename.split('.')[-1]
    print(">>>>>>>", extension)
    filename = str(instance.pk) + '.' + str(extension)
    return os.path.join('product_images/', filename)


# ToDo --> Fields de Dinheiro, Endereço e coordenadas
class BaseConfiguration(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merkadu_tax = models.FloatField('taxa do merkadu', null=True)
    delivery_fee_percent = models.IntegerField('percentual da taxa de entrega', null=True, blank=True)
    pix_cost_percent = models.FloatField('porcentagem de custo com o pix', null=True)
    
    class Meta:
        db_table = 'base_configuration'
        verbose_name_plural = 'configuração'
        verbose_name = 'configuração'

    def __str__(self):
        return str("Configuração merkadu")


class Market(models.Model):
    partner = models.ForeignKey(CustomUser, related_name="parceiro", null=True ,on_delete=models.CASCADE, verbose_name='parceiro', blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, verbose_name='usuário')
    name = models.CharField('nome do estabelecimento', null=False, blank=False, max_length=250)
    cnpj = models.CharField('cnpj', null=True, max_length=14)
    bank = models.CharField('banco', null=True, max_length=250)
    bank_account = models.CharField('conta do banco', null=True, max_length=250)
    bank_agency = models.CharField('agência do banco', null=True,  max_length=250)
    pix = models.CharField('pix', null=True, max_length=250)
    delivery_fee = models.FloatField('taxa de entrega', null=True)
    delivery_time = models.FloatField('tempo de entrega (hs)', null=True)
    min_order_value = models.FloatField('valor mínimo do pedido', null=True)
    phone_number = models.CharField('telefone', max_length=18)
    adress_street = models.CharField('rua', null=True, max_length=250)
    adress_number = models.IntegerField('numero', null=True)
    adress_district = models.CharField('bairro', null=True, max_length=250)
    city = models.CharField('cidade', null=True, max_length=250)
    state = models.CharField('estado', null=True, max_length=250)
    latitude = models.CharField('latitude', null=True, max_length=250)
    longitude = models.CharField('longitude', null=True, max_length=250)
    logotipo = models.ImageField('logomarca', upload_to='media/', max_length=250)
    is_active = models.BooleanField('ativo', default=False)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

    class Meta:
        db_table = 'market'
        verbose_name_plural = 'mercados'
        verbose_name = 'mercado'

    def __str__(self):
        return str(self.name)
        
CATEGORY_CHOICES = (
    ('drinks', 'Bebidas'),
    ('grocery_store', 'Mercearia'),
    ('cleaning_products', 'Produtos de Limpeza'),
    ('personal_hygiene', 'Higiene Pessoal'),
    ('medicines', 'Medicamentos'),
)

class ProdutoCatalogo(models.Model):
    category = models.CharField('categoria', max_length=50, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.FileField(upload_to='imagens_catalogo/', null=True, blank=True)


    def __str__(self):
        return self.name
    
class Product(models.Model):
    produto_catalogo = models.ForeignKey(ProdutoCatalogo, on_delete=models.CASCADE, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('nome', max_length=250)
    market = models.ForeignKey(Market, related_name="market", null=False ,on_delete=models.CASCADE, verbose_name='mercado')
    descript = models.CharField('descrição', max_length=250)
    value = models.FloatField('valor')
    offer_value = models.FloatField('valor de oferta')
    quantity_in_stock = models.IntegerField('quantidade em estoque')
    # image = models.ImageField('imagem do produto', upload_to=image_dir_path_products, max_length=250, default='default.png') ##max_length=100) ##default='default.png')
    category = models.CharField('categoria', max_length=50, choices=CATEGORY_CHOICES)
# upload_to='product_images/'
    image = models.FileField(upload_to='product_images/', blank=True, null=True, validators=[validate_webp_extension])
    is_active = models.BooleanField('ativo', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

    class Meta:
        db_table = 'product'
        verbose_name_plural = 'produtos'
        verbose_name = 'produto'

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    market = models.ForeignKey(Market, null=False ,on_delete=models.CASCADE, verbose_name='mercado')
    client = models.ForeignKey(CustomUser, null=False ,on_delete=models.CASCADE, verbose_name='cliente')
    client_name = models.CharField('client_name', max_length=100 , null=True)
    client_cpf = models.CharField('cpf', max_length=100 , null=True)
    client_phone = models.CharField('phone', max_length=100 , null=True)

    address_number = models.CharField('número', max_length=100 , null=True)
    address_street = models.CharField('rua', max_length=100 , null=True)
    address_district = models.CharField('bairro', max_length=100 , null=True)

    total = models.FloatField('total', null=True)

    merkadu_tax = models.FloatField('taxa do merkadu', null=True)
    delivery_fee_percent = models.FloatField('percentual da taxa de entrega para o merkadu', null=True)
    pix_cost_percent = models.FloatField('porcentagem de custo com o pix no pedido', null=True)

    delivery_fee = models.FloatField('taxa de entrega', null=True)

    pix_cost = models.FloatField('custo com o pix no pedido', null=True)
    market_receivable = models.FloatField('recebível do mercado', null=True)
    merkadu_receivable = models.FloatField('recebível do merkadu', null=True)
    
    products = JSONField()

    status = models.CharField('status', max_length=50 ,default='Pendente')

    market_payed = models.BooleanField('o supermercado já foi pago por esse pedido?', null=True, default=False)
    finalized_at = models.DateTimeField('finalizado em ', null=True)

    is_active = models.BooleanField('ativo', default=True)
    created_at = models.DateTimeField('criado em', auto_now_add=True)
    updated_at = models.DateTimeField('atualizado em ', auto_now_add=True)

    class Meta:
        db_table = 'order'
        verbose_name_plural = 'pedidos'
        verbose_name = 'pedido'

    def __str__(self):
        return str(self.client.email) + " " + str(self.market.name)

