from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('register', views.RegisterView.as_view(), name='register'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('users/', include([
        path('my-courses', views.EnrolledCoursesListView.as_view(), name='enrolled-courses'),
        path('my-courses/<slug:slug>/modules/', views.CourseModulesListView.as_view(), name='course-modules-list'),
        path('my-courses/<slug:course_slug>/modules/<slug:module_title>/', views.ModuleContentView.as_view(), name='course-modules-single'),
        path('profile', views.ProfileUpdateView.as_view(), name='my-profile'),
    ])),
]
