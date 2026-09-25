from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='jobs.index'),
    path('mine/', views.my_jobs, name='jobs.mine'),
    path('create/', views.create_job, name='jobs.create'),
    path('<int:job_id>/edit/', views.edit_job, name='jobs.edit'),
]