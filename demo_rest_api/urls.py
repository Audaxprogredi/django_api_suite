from django.urls import path
from . import views

urlpatterns = [
   # Ruta general para GET (listar) y POST (crear)
   path("index/", views.DemoRestApi.as_view(), name="demo_rest_api_resources"),
   
   # Ruta específica para PUT, PATCH y DELETE que requiere un ID
   path("<str:item_id>/", views.DemoRestApiItem.as_view(), name="demo_rest_api_item"),
]