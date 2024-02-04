from django.urls import path
import app.views as app_views
from django.conf import settings
from django.conf.urls.static import static
from .views import user_login, register
from django.contrib.auth.views import LogoutView





app_name = 'merkadu'

urlpatterns = [
    path('', app_views.home, name='home'),
    # path('multi-login/', MultiLoginView.as_view(), name='multi-login'),
    path('pricing', app_views.pricing, name='pricing'),
    path('privacity-term', app_views.privacity_term, name='privacity_term'),
    path('termos', app_views.termos, name='termos'),
    # Market URLs
    path('dashboard', app_views.dashboard, name='dashboard'),
    path('orders', app_views.orders, name='orders'),
    path('products', app_views.products, name='products'),
    path('products/add', app_views.add_product, name='add'),
    path('products/edit/<uuid:pk>', app_views.edit_product, name='edit'),
    path('orders/edit/<uuid:pk>', app_views.edit_order, name='edit'),
    path('products/import_table_products', app_views.import_table_products, name='import_table_products'),
    path('search_products', app_views.search_products, name='search_products'),
    path('configurations', app_views.configurations, name='configurations'),
    path('empty_cart/', app_views.empty_cart, name='empty_cart'),
    path('market/<uuid:market_id>/search/', app_views.search_products_market, name='search_products_market'),




    # Client URLs
    path('markets', app_views.markets, name='markets'),
    path('market/<uuid:pk>', app_views.market, name='market'),
    path('market_orders/<uuid:pk>', app_views.market_orders, name='market_orders'),
    path('market_checkout/<uuid:pk>', app_views.market_checkout, name='market_checkout'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # Admin URLs
    path('pay_markets', app_views.pay_markets, name='pay_markets')
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


