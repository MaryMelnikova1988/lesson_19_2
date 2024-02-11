from django.urls import path
from django.views.decorators.cache import cache_page

from main.apps import MainConfig
from main.views import contact, StudentListView, StudentCreateView, StudentUpdateView, StudentDetailView, \
    StudentDeleteView

app_name = MainConfig.name

urlpatterns = [
    path('', cache_page(60)(StudentListView.as_view()), name='index'),
    path('contact/', contact, name='contact'),
    path('create/', StudentCreateView.as_view(), name='create_student'),
    path('update/<int:pk>/', StudentUpdateView.as_view(), name='update_student'),
    path('view/<int:pk>/', StudentDetailView.as_view(), name='view_student'),
    path('delete/<int:pk>/', StudentDeleteView.as_view(), name='delete_student'),

]  # path('view/<int:pk>/', view_student, name='view_student'),
