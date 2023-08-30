from django import forms
from django.shortcuts import redirect, render
from .models import Course, Module

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

            return redirect('courses:course_detail', slug=course.slug)

    else:
        course_form = CourseForm()
        module_form = ModuleForm()

    context = {
        'course_form': course_form,
        'module_form': module_form,
        'title': 'Add Course',
    }

    return render(request, 'add_course.html', context)
