from django.urls import path

from main.apps import MainConfig
from main.views import contact, view_student, StudentListView, StudentCreateView, StudentUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', StudentListView.as_view(), name='index'),
    path('contact/', contact, name='contact'),
    path('/create/', StudentCreateView.as_view(), name='create_student'),
    path('/update/<int:pk>/', StudentUpdateView.as_view(), name='update_student'),

]    # path('view/<int:pk>/', view_student, name='view_student'),