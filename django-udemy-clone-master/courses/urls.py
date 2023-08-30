from django.urls import path
from .views import *


app_name = 'courses'

urlpatterns = [
    path('courses/<slug:slug>', CourseDetailView.as_view(), name='course-details'),
    path('courses/<slug:slug>/category', CoursesByCategoryListView.as_view(), name='course-by-category'),
    path('add/', add_course, name='add_course'),
    path('my-courses/', MyCoursesListView.as_view(), name='my-courses'),
    path('delete/<slug:slug>/', CourseDeleteView.as_view(), name='delete-course')

]
