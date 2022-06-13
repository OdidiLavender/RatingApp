from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home' ),
    path('register', register, name='register' ),
    path('signIn', signIn, name='signIn' ),
    path('signOut', signOut, name='signOut' ),
    path('profile', profile, name='profile' ),
    path('post', post, name='post' ),
    path('veiwpost/<str:pk>/', viewpost, name='viewpost' ),
]