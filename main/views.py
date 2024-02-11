from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from main.forms import StudentForm, SubjectForm
from main.models import Student, Subject
from main.services import get_cached_subjects_for_student


class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    # permission_required = 'main.view_student'
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
@login_required
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


class StudentDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Student
    permission_required = 'main.view_student'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # if settings.CACHE_ENABLED:
        #     key = f'subject_list_{self.object.pk}'
        #     subject_list = cache.get(key)
        #     if subject_list is None:
        #         subject_list = self.object.subject_set.all()
        #         cache.set(key, subject_list)
        # else:
        #     subject_list = self.object.subject_set.all()
        context_data['subjects'] = get_cached_subjects_for_student(self.object.pk)
        return context_data


# def view_student(request, pk):
#     student_item = get_object_or_404(Student, id=pk)
#     context = {
#         'object': student_item
#     }
#     return render(request, 'main/student_detail.html', context)


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    permission_required = 'main.add_student'
    success_url = reverse_lazy('main:index')


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    permission_required = 'main.change_student'
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


class StudentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Student
    # permission_required = 'main.delete_student'
    success_url = reverse_lazy('main:index')

    def test_func(self):
        return self.request.user.is_superuser
