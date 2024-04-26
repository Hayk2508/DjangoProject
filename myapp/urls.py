from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create-post/', views.create_post, name='create-post'),
    path('post/<str:pk>/', views.post, name='post'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('delete-post/<str:pk>/', views.delete_post, name='delete-post'),
    path('UserPosts/', views.UserPosts, name='UserPosts'),
    path('register/', views.registerUser, name='register'),
]

