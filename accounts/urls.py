from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.AccountAllView.as_view(), name='AccountAllView'),
    path('<int:account_id>/', views.AccountDetailView.as_view(), name='AccountDetailView'),
    path('<int:account_id>/copy/', views.AccountDetailCopyView.as_view(), name='AccountDetailView'),
]