from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from main.forms import StudentForm, SubjectForm
from main.models import Student, Subject


class StudentListView(ListView):
    model = Student
    template_name = 'main/index.html'


# Create your views here.
# def index(request):
#     student_list = Student.objects.all()
#     context = {
#         'object_list': student_list,
#         'title': "Главная"
#     }
#
#     return render(request, 'main/index.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f"{name} ({email}): {message}")
    context = {
        'title': "Контакты"
    }

    return render(request, 'main/contact.html', context)


def view_student(request, pk):
    student_item = get_object_or_404(Student, id=pk)
    context = {
        'object': student_item
    }
    return render(request, 'main/student_detail.html', context)


class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('main:index')


class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy('main:index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Student, Subject, form=SubjectForm, extra=1)
        if self.request.method == "POST":
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)

        return context_data

    def form_valid(self, form):

        formset = self.get_context_data()['formset']
        self.object.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)
