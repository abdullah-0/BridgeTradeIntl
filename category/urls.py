from django.urls import path
from .views import CategoryView, CategoryDetailView,HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/', CategoryView.as_view(), name='category'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
]
