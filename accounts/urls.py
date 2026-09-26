from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('profile/', views.profile, name='accounts.profile'),
    path('profile/edit/', views.edit_profile, name='accounts.edit_profile'),
    path("profiles/search/", views.search_seekers, name="accounts.search_seekers"),
    path('profile/<int:id>/', views.profile_detail, name='accounts.profile_detail'),
]