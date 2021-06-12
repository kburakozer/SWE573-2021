from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'document'

urlpatterns = [
    
    path('search/', views.Search.as_view(), name='search_result'),
    path('', views.IndexClassView.as_view(), name='index'),
    # path('tag/<slug:doc_id>/', views.Tag_view.as_view(), name='tag'),
    path('<int:pk>/', views.DocDetailView.as_view(), name='detail'),
    path('tag/<int:doc_id>/', views.Tag_view, name='tag'),
    path('register/', views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='document/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='document/logout.html'), name='logout')
]