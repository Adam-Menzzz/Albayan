from django import forms
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, View
from courses.models import Course, Category, Module
from udemy.models import Enroll
from .forms import CourseForm, ModuleForm


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/details.html'
    context_object_name = 'course'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        slug = self.kwargs.get(self.slug_url_kwarg)
        slug_field = self.get_slug_field()
        queryset = queryset.filter(**{slug_field: slug})
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404("No %(verbose_name)s found matching the query" %
                          {'verbose_name': self.model._meta.verbose_name})
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        if self.request.user.is_authenticated:
            if Enroll.objects.filter(course=course, user_id=self.request.user.id).exists():
                context['is_enrolled'] = True

        return context

class CoursesByCategoryListView(ListView):
    model = Course
    template_name = 'courses/courses_by_category.html'
    context_object_name = 'courses'

    def get_queryset(self):
        category = Category.objects.get(slug=self.kwargs['slug'])
        return self.model.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = category
        context['categories'] = Category.objects.all()
        return context

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'category', 'short_description', 'description', 'outcome', 'requirements', 'language', 'price', 'level', 'thumbnail', 'video_url']

class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['title', 'video', 'text']

def add_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)
        module_form = ModuleForm(request.POST, request.FILES)
        if course_form.is_valid() and module_form.is_valid():
            course = course_form.save(commit=False)
            course.user = request.user
            course.save()

            module = module_form.save(commit=False)
            module.course = course
            module.save()

            return redirect('/')

    else:
        course_form = CourseForm()
        module_form = ModuleForm()

    context = {
        'course_form': course_form,
        'module_form': module_form,
        'title': 'Add Course',
    }

    return render(request, 'courses/add_course.html', context)

class CourseDeleteView(View):
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        course.delete()
        return redirect('courses:my-courses')

class MyCoursesListView(View):
    def get(self, request):
        courses = Course.objects.filter(user=request.user)
        return render(request, 'courses/my_courses.html', {'courses': courses})
