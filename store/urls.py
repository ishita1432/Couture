from django.urls import path
from . import views
from . import auth_views


urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',auth_views.signup,name='signup'),
    path('login/', auth_views.signin, name='login'),
    path('logout/', auth_views.signout, name='logout'),
   path('shop/<str:category>',views.shop_with_category,name='shop_with_category'),
    # path('shop/',views.shop,name='shop'),
    path('shop/<str:sub_category>/', views.category_view, name='category_view'),
    
    path('shop/<str:category>/', views.category_view, name='category_view'),
    path('shop/<str:type>/', views.product_type, name='product_type'),
    path('cart/',views.cart,name='cart'),
    path('filter/',views.filter_products,name="filter"),
    path('<slug:cat_slug>/<slug:prod_slug>/', views.product_view, name='product_view'),
    path('category/',views.category,name='category'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('shop/<str:category>',views.shop_with_category,name='shop_with_category'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart_total/', views.update_cart_total, name='update_cart_total'),
    path('checkout/',views.checkout,name="placeorder"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('add_to_wishlist/',views.add_to_wishlist,name="add_to_wishlist"),
    path('remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('order_summary/',views.order_summary,name="order_summary"),
    path('shop/',views.shop,name='shop'),
    path('payment/<int:total_price>', views.payment,name="payment"),
]