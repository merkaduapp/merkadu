import json
import logging
from django.conf import settings
from django.http import HttpResponse
import requests
import pandas as pd
from django.contrib import messages
from django.core.exceptions import BadRequest
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Product, Order, Market, BaseConfiguration, CustomUser
from .forms import MarketForm, ProductForm, OrderForm
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
import math
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Product


logger = logging.getLogger(__name__)

CATEGORY_CHOICES = (
    ('drinks', 'Bebidas'),
    ('grocery_store', 'Mercearia'),
    ('cleaning_products', 'Produtos de Limpeza'),
    ('personal_hygiene', 'Higiene Pessoal'),
    ('medicines', 'Medicamentos'),
)

def search_products_market(request, market_id):
    query = request.GET.get('search', '')
    search_term = request.GET.get('search', '').lower()

    # Filtra os produtos que contêm o termo de pesquisa no nome
    search_results = Product.objects.filter(name__icontains=search_term)
    products = Product.objects.filter(market_id=market_id)

    context = {
        'products': products,
        'market_id': market_id,
        'query': query,

    }

    if search_term:
        # Se houver um termo de pesquisa, filtre os produtos
        products = Product.objects.filter(market_id=market_id, name__icontains=search_term)
    else:
        # Se não houver termo de pesquisa, obtenha todos os produtos
        products = Product.objects.filter(market_id=market_id)

    return render(request, 'search_results.html', context)



def empty_cart(request):
    # Lógica para esvaziar o carrinho

    # Exemplo: Se você estiver usando sessões para armazenar o carrinho
    request.session.pop('cart', None)

    # Redireciona de volta à página de onde a solicitação foi feita
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            # Lógica para lidar com credenciais inválidas
            return render(request, 'custom_login.html', {'error_message': 'Credenciais inválidas'})

    return render(request, 'seu_template_de_login.html')


def home(request):
    return render(request, 'startbootstrap-new-age-gh-pages/index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Autenticar o usuário recém-registrado
            authenticated_user = authenticate(request, username=user.username, password=request.POST['password1'], backend='django.contrib.auth.backends.ModelBackend')
            
            if authenticated_user:
                auth_login(request, authenticated_user)
            
            return redirect('merkadu:home')  # Redirecione para a página inicial após o registro
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('merkadu:home')  # Redirecione para a página inicial após o login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})



def search_products(request):
    search_query = request.GET.get('search', '')
    if search_query:
        # Lógica para filtrar produtos baseada na pesquisa
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.all()

    return render(request, 'market/products.html', {"products":products})


def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor



@csrf_protect
def home(request):
    print("DEBUG - User:", request.user)

    user_greeting = request.user
    current_market_id = None

    if request.user.is_authenticated:
        current_market = Market.objects.filter(user=request.user).first()
        current_market_id = current_market.id if current_market else None

    print("DEBUG - Current Market ID:", current_market_id)

    return render(request, 'index.html', {'user_greeting': user_greeting, 'user': request.user, 'current_market_id': current_market_id})

def pricing(request):
    return render(request, 'pricing.html', {})

def privacity_term(request):
    return render(request, 'politica_privacidade.html', {})

def recovery_password(request):
    return render(request, 'client/password_recovery.html', {})


@login_required
@csrf_protect
def termos(request):
    return render(request, 'termos.html', {})


# MARKET'S VIEWS
@login_required
@csrf_protect
def dashboard(request):
    market = Market.objects.filter(user=request.user)
    if market:
        market = market[0]
        orders = Order.objects.filter(market=market, status='Finalizado', market_payed=False)
        orders_count = len(list(orders))
        balance_count = sum([truncate(order.market_receivable, 2) for order in orders])
    else:
        return redirect('/configurations')
    return render(request, 'market/dashboard.html', { 'orders': orders_count, 'balance': balance_count})


@login_required
@csrf_protect
def products(request):
    category = request.GET.get('category', '')  # Pega o parâmetro da URL
    if category:
        products = Product.objects.filter(category=category)  # Filtra por categoria
    else:
        products = Product.objects.all()  # Todos os produtos se nenhuma categoria for selecionada

    market = Market.objects.filter(user=request.user)
    if market:
        market = market[0]
        products = Product.objects.filter(market=market)
        search = request.GET.get('search')
        if search:
            products = products.annotate(
                search=SearchVector('category', 'name', 'descript', 'value'),
            ).filter(search=search)
    else:
        return redirect('/configurations')
    
    

    return render(request, 'market/products.html', {"products":products})


@login_required
@csrf_protect
def edit_product(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form = form.save()
            return redirect('/products')
    else:
        product = Product.objects.get(id=pk)
        form = ProductForm(instance=product)
    return render(request, 'market/edit_product.html', {"form": form, "product":product})


@login_required
@csrf_protect
def add_product(request):
    try:
        if request.method == 'POST':
            market = Market.objects.get(user=request.user)
            form = ProductForm(request.POST, request.FILES)
            
            if form.is_valid():
                produto = form.save(commit=False)
                produto.market = market
                produto.save()

                # Adicione lógica adicional, se necessário
                if produto.produto_catalogo:
                    produto_do_catalogo = produto.produto_catalogo
                    # Faça o que for necessário para associar produtos do catálogo ao produto do mercado
                    # Associe a imagem do catálogo ao novo produto
                    if produto_do_catalogo.image:
                        produto.image = produto_do_catalogo.image
                        produto.save()

                return redirect('/products')
            else:
                logger.error(f"Erro no formulário: {form.errors}")
        else:
            market = Market.objects.filter(user=request.user)
            if market:
                market = market[0]
                # Obtenha todos os produtos ordenados por nome para exibição
                products = Product.objects.filter(market=market).order_by('produto_catalogo__name')
                form = ProductForm()
                return render(request, 'market/add_product.html', {"form": form, "products": products})
            else:
                return redirect('/configurations')

    except Exception as e:
        logger.exception(f"Erro na view add_product: {str(e)}")
        return render(request, 'error.html', status=500)

@login_required
@csrf_protect
def import_table_products(request):
    if request.method == "POST":
        market = Market.objects.filter(user=request.user)
        if market:
            market = market[0]
        else:
            market = Market.objects.create(user=request.user)
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Este arquivo não é um arquivo CSV!')
            return render(request, "import_table_products.html")
        data_frame = pd.read_csv(csv_file ,sep=';')

        for index, row in data_frame.iterrows():
            Product.objects.create(
                name = row['nome'],
                market = market,
                descript = row['descrição'],
                value = row['valor'],
                offer_value = row['valor em oferta'],
                quantity_in_stock = row['quantidade em estoque'],
            )
        return redirect("/products")
    else:
        return render(request, "market/import_table_products.html")


@login_required
@csrf_protect
def orders(request):
    market = Market.objects.filter(user=request.user)
    if market:
        market = market[0]
        orders = Order.objects.filter(market=market)
        search = request.GET.get('search')
        if search:
            orders = orders.annotate(
                search=SearchVector('id', 'data', 'status'),
            ).filter(search=search)
    else:
        return redirect('/configurations')
    return render(request, 'market/orders.html', {"orders": reversed(orders)})


@login_required
@csrf_protect
def edit_order(request, pk):
    if request.method == 'POST':
        order = Order.objects.get(id=pk)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form = form.save()
            return redirect('/orders')
    else:
        order = Order.objects.get(id=pk)
        form = OrderForm(instance=order)
    return render(request, 'market/edit_order.html', {"form": form, "order":order})


@login_required
@csrf_protect
def configurations(request):
    if request.method == 'POST':
        market = Market.objects.get(user=request.user)
        form = MarketForm(request.POST, instance=market)
        if form.is_valid():
            user = form.save()
            return render(request, 'market/configurations.html', {"form": form})
    else:
        market = Market.objects.filter(user=request.user)
        if market:
            market = market[0]
        else:
            market = Market.objects.create(user=request.user)
        form = MarketForm(instance=market)
    return render(request, 'market/configurations.html', {"form": form})


# CLIENT'S VIEWS

@csrf_protect
def markets(request):
    markets = Market.objects.filter(is_active=True)
    return render(request, 'client/markets.html', {'markets': markets})


# @csrf_protect
def market(request, pk):

    CATEGORY_CHOICES_TRANSLATION = {
        'drinks': 'Bebidas',
        'grocery_store': 'Mercearia',
        'cleaning_products': 'Produtos de Limpeza',
        'personal_hygiene': 'Higiene Pessoal',
        'medicines': 'Medicamentos',
    }
    user_greeting = request.user
    if request.session.get(f'cart_{pk}') is None:
        request.session[f'cart_{pk}'] = {}

    add_product = request.GET.get('add_product')
    if add_product:
        product = Product.objects.get(id=add_product)
        if add_product not in request.session.get(f'cart_{pk}'):
            request.session.get(f'cart_{pk}')[add_product] = {
                "id": str(product.id),
                "name": str(product.name),
                "image": str(product.image.url),
                "quantity": 1,
                "sub_total": float(product.value),
            }
        else:
            quantity = request.session.get(f'cart_{pk}')[add_product]["quantity"] + 1
            sub_total = request.session.get(f'cart_{pk}')[add_product]["sub_total"] + float(product.value)
            request.session.get(f'cart_{pk}')[add_product] = {
                "id": str(product.id),
                "name": str(product.name),
                "image": str(product.image.url),
                "quantity": quantity,
                "sub_total": sub_total,
            }
        request.session.modified = True

    remove_product = request.GET.get('remove_product')
    if remove_product:
        if remove_product in request.session.get(f'cart_{pk}'):
            product = Product.objects.get(id=remove_product)
            quantity = request.session.get(f'cart_{pk}')[remove_product]["quantity"] - 1
            sub_total = request.session.get(f'cart_{pk}')[remove_product]["sub_total"] - float(product.value)
            request.session.get(f'cart_{pk}')[remove_product] = {
                "id": str(product.id),
                "name": str(product.name),
                "image": str(product.image.url),
                "quantity": quantity,
                "sub_total": sub_total,
            }
            if request.session.get(f'cart_{pk}')[remove_product]["quantity"] == 0:
                del request.session.get(f'cart_{pk}')[remove_product]
            request.session.modified = True
    
    cart = request.session[f'cart_{pk}']
    total_value = 0
    for product in list(cart):
        total_value += cart[product]["sub_total"]
        
    market = Market.objects.get(id=pk)
    products = Product.objects.filter(is_active=True, market=market)
    search = request.GET.get('search')
    products_count = products.count()

    search = request.GET.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(descript__icontains=search) | 
            Q(value__icontains=search) |
            Q(category__label__icontains=search)  # Adicione esta linha para pesquisa na categoria pelo nome
        )
    # Mapeia os valores originais para suas versões em português
    translated_categories = dict(CATEGORY_CHOICES)
    # Substitui os valores originais pelos traduzidos na lista de produtos
    # Substitui os valores originais pelos traduzidos na lista de produtos
    for product in products:
        product.category = translated_categories.get(product.category, product.category)
    
    def empty_cart():
        # Lógica para esvaziar o carrinho
        request.session[f'cart_{pk}'] = {}
        request.session.modified = True

    if 'empty_cart' in request.GET:
        empty_cart()
        return redirect('merkadu:market', pk=pk)
    
    sort_param = request.GET.get('sort', 'relevance')

    # Adicionar lógica para ordenação
    if sort_param == 'price_asc':
        products = products.order_by('value')
    elif sort_param == 'price_desc':
        products = products.order_by('-value')
    elif sort_param == 'name_asc':
        products = products.order_by('name')
    elif sort_param == 'name_desc':
        products = products.order_by('-name')
    elif sort_param == 'relevance':
        # Lógica de ordenação de relevância (ajuste conforme necessário)
        pass
   
    product_categories = products.values_list('category', flat=True).distinct()
    selected_category = request.GET.get('category', None)

    if selected_category:
        products = products.filter(category=selected_category)

    for product in products:
        product.category = translated_categories.get(product.category, product.category)

    return render(request, 'client/market.html', 
        {
        "market": market, 
        "products": products, 
        "cart": cart, 
        "total": total_value,
        "search": search,
        "id": market,
        "user_greeting": user_greeting,
        "empty_cart": empty_cart,
        "products_count": products_count,
        "product_categories": product_categories,
        "selected_categories": selected_category,
        "translated_categories": translated_categories,
        }
    )


@login_required
@csrf_protect
def market_orders(request, pk):
    user = User.objects.get(email=request.user)
    market = Market.objects.get(id=pk)
    orders = Order.objects.filter(client=user, market=market)
    search = request.GET.get('search')
    if search:
        products = products.annotate(
            search=SearchVector('name', 'descript', 'value'),
        ).filter(search=search)
    return render(request, 'client/orders.html', {"market": market, "orders": reversed(orders)})


# @login_required
# @csrf_protect
def market_checkout(request, pk):
    merkadu_config = BaseConfiguration.objects.first()
    market = Market.objects.get(id=pk)
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    try:
        market = Market.objects.get(id=pk)
    except Market.DoesNotExist:
        return render(request, 'client/error.html', {'error_message': 'Mercado não encontrado.'})

    add_product = request.GET.get('add_product')
    if add_product:
        product = Product.objects.get(id=add_product)
        if add_product not in request.session.get(f'cart_{pk}'):
            request.session.get(f'cart_{pk}')[add_product] = {
                "id": str(product.id),
                "name": str(product.name),
                "image": str(product.image.url),
                "quantity": 1,
                "sub_total": float(product.value),
            }
        else:
            quantity = request.session.get(f'cart_{pk}')[add_product]["quantity"] + 1
            sub_total = request.session.get(f'cart_{pk}')[add_product]["sub_total"] + float(product.value)
            request.session.get(f'cart_{pk}')[add_product] = {
                "id": str(product.id),
                "name": str(product.name),
                "image": str(product.image.url),
                "quantity": quantity,
                "sub_total": sub_total,
            }
        request.session.modified = True

    # REMOVING A PRODUCT TO CART
    remove_product = request.GET.get('remove_product')
    if remove_product:
        if remove_product in request.session.get(f'cart_{pk}'):
            product = Product.objects.get(id=remove_product)
            quantity = request.session.get(f'cart_{pk}')[remove_product]["quantity"] - 1
            sub_total = request.session.get(f'cart_{pk}')[remove_product]["sub_total"] - float(product.value)
            request.session.get(f'cart_{pk}')[remove_product] = {
                "id": str(product.id),
                "name": str(product.name),
                "image": str(product.image.url.url),
                "quantity": quantity,
                "sub_total": sub_total,
            }
            if request.session.get(f'cart_{pk}')[remove_product]["quantity"] == 0:
                del request.session.get(f'cart_{pk}')[remove_product]
            request.session.modified = True
    
    # CALCULATING CART VALUES
    cart = request.session[f'cart_{pk}']
    # total_value = 0
    total_value = sum(product["sub_total"] for product in cart.values())

    for product in list(cart):
        total_value += cart[product]["sub_total"]   
    
    delivery_fee = market.delivery_fee
    merkadu_delivery_fee_percent = merkadu_config.delivery_fee_percent
    merkadu_tax = merkadu_config.merkadu_tax
    pix_cost_percent = merkadu_config.pix_cost_percent

    total_value = total_value + merkadu_tax + delivery_fee
    pix_cost = (total_value / 100) * pix_cost_percent
    merkadu_receivable = (merkadu_tax + ((delivery_fee / 100) * merkadu_delivery_fee_percent))
    market_receivable = total_value - pix_cost - merkadu_receivable

    market = Market.objects.get(id=pk)
    print(">>>>>>>>>>>mercado", market)
    name = request.GET.get('name')
    cpf = request.GET.get('cpf')
    phone = request.GET.get('phone')
    address_street = request.GET.get('address_street')
    address_district = request.GET.get('address_district')
    address_number = request.GET.get('address_number')
    checkout = request.GET.get('checkout')

    if checkout and total_value > market.min_order_value:
        if user is None:
            # Usuário não autenticado, você pode tratar de maneira diferente aqui
            return HttpResponse("Pedido realizado por usuário não autenticado.")
        if merkadu_config:
            delivery_fee_percent = merkadu_config.delivery_fee_percent
        headers = {
            'Authorization': f'Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}',
        }
        # CRIAR PIX DINÂMICO DO PEDIDO
        api ="https://api.mercadopago.com/v1/"
        payload_to_create_charge = {
            "transaction_amount": total_value,
            "payment_method_id": "pix",
            "payer": {
                "first_name": name.split(" ")[0],
                "last_name": name.split(" ")[1],
                "email": user.email
            },
            "description": f"Compra no supermercado {market.name} no merkadu.SHOP"
        }
        charge = requests.post(api + "payments", json=payload_to_create_charge, headers=headers)
        charge = dict(json.loads(charge.content))
        pix_info = {
            "qr_code": charge["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": charge["point_of_interaction"]["transaction_data"]["qr_code_base64"]
        }
        request.session[f"charge_{pk}"] = charge
        
        request.session[f"name_{pk}"] = name 
        request.session[f"cpf_{pk}"] = cpf
        request.session[f"phone_{pk}"] = phone
        request.session[f"address_street_{pk}"] = address_street
        request.session[f"address_district_{pk}"] = address_district
        request.session[f"address_number_{pk}"] = address_number
        
        request.session.modified = True
        return render(request, 'client/pay_pix.html', {
                "pix_info": pix_info,
                "market": market, 
                "total": total_value,
            }
        )

    payed_pix = request.GET.get('payed_pix')
    if payed_pix:
        charge = request.session.get(f'charge_{pk}')
        id = charge["id"]
        api ="https://api.mercadopago.com/v1/"
        headers = {
            'Authorization': f'Bearer {settings.MERCADO_PAGO_ACCESS_TOKEN}',
        }
        charge = requests.get(api + f"payments/{id}", headers=headers)
        charge = dict(json.loads(charge.content))
        pix_info = {
            "qr_code": charge["point_of_interaction"]["transaction_data"]["qr_code"],
            "qr_code_base64": charge["point_of_interaction"]["transaction_data"]["qr_code_base64"]
        }
        if charge["status"] == "approved":  
            name = request.session[f"name_{pk}"]
            cpf = request.session[f"cpf_{pk}"]
            phone = request.session[f"phone_{pk}"]
            address_street = request.session[f"address_street_{pk}"]
            address_district = request.session[f"address_district_{pk}"]
            address_number = request.session[f"address_number_{pk}"]
            
            products = list(request.session[f'cart_{pk}'].values())
            order = Order(
                market=market,
                client=user,
                client_name=name,
                client_cpf=cpf,
                client_phone=phone,
                products=products,
                status='Pendente',
                total=total_value,
                pix_cost=pix_cost,
                pix_cost_percent=pix_cost_percent,
                merkadu_receivable=merkadu_receivable,
                market_receivable=market_receivable,
                delivery_fee=delivery_fee,
                delivery_fee_percent=merkadu_delivery_fee_percent,
                merkadu_tax=merkadu_tax,
                address_street=address_street,
                address_number=address_number,
                address_district=address_district,
            )
            order.save()
            del request.session[f'cart_{pk}']
            return render(request, 'client/sucess_payment.html', {
                "market": market, 
                "total": total_value,
                "orders": f'market_orders/{pk}',
            })
        else:
            return render(request, 'client/pay_pix.html', {
                    "pix_info": pix_info,
                    "market": market, 
                    "total": total_value,
                    "not_payed_pix": True
                }
            )

    error = ""
    if total_value < market.min_order_value:
        error = f"O pedido tem o valor menor que o mínimo de R${market.min_order_value}"
    
    return render(request, 'client/checkout.html', {
            "market": market, 
            "cart": cart, 
            "total":total_value,
            "config": merkadu_config,
            "error": error
        }
    )


# ADMIN'S VIEWS
@login_required
@csrf_protect
def pay_markets(request):
    if request.user.is_superuser:
        
        # RECEBÍVEL DO MERCADO JÀ FOI PAGO
        market = request.GET.get('market')
        if market:
            market = Market.objects.get(id=market)
            orders = Order.objects.filter(market=market, status='Finalizado', market_payed=False)
            for order in orders:
                order.market_payed = True
                order.save()            

        # MERCADOS A RECEBEREM PAGAMENTO
        markets_objs = []
        markets = Market.objects.filter(is_active=True)
        for market in markets:
            orders = Order.objects.filter(market=market, status='Finalizado', market_payed=False)
            orders_numbers = len(list(orders))
            market_receivable = sum([truncate(order.market_receivable, 2) for order in orders])

            market_obj = {
                "id": market.id,
                "market_name": market.name,
                "orders_numbers": orders_numbers,
                "market_receivable": market_receivable
            }
            if market_receivable:
                markets_objs.append(market_obj)
        return render(request, 'merkadu/pay_markets.html', { "markets": markets_objs })
    else:
        raise BadRequest('Invalid request.')