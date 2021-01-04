"""classproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from onlineapp.views import *

urlpatterns = [

    path('', lambda req: redirect('colleges_list', permanent=True)),

    path('first_view', my_first_view),

    path('colleges/', CollegeView.as_view(), name="colleges_list"),
    path('college/<int:id>', CollegeView.as_view(), name="college_details"),
    path('college/<str:acronym>', CollegeView.as_view(), name="college_acronym"),

    path('api/colleges/', college_api, name="api_colleges_list"),
    path('api/colleges/<int:id>', college_modify_api, name="api_college_details"),
    path('api/colleges/<str:acronym>', college_modify_api, name="api_college_acronym"),

    path('api/college/<int:cid>/students', StudentApiView.as_view(), name="api_student_list"),
    path('api/college/<int:cid>/student/<int:id>', StudentApiView.as_view(), name="api_student_details"),

    path('colleges/add', AddCollegeView.as_view(), name="add_college"),
    path('colleges/<int:id>/edit', AddCollegeView.as_view(), name="edit_college"),
    path('colleges/<int:id>/delete', AddCollegeView.as_view(), name="del_college"),

    path('student/<int:id>', StudentView.as_view(), name="student_details"),

    path('student/add/<int:id>', AddStudentView.as_view(), name="add_student"),
    path('student/edit/<int:id>', AddStudentView.as_view(), name="edit_student"),
    path('student/del/<int:id>', AddStudentView.as_view(), name="del_student"),

    path('login', LoginView.as_view(), name='login'),
    path('signup', SignupView.as_view(), name='signup'),
    path('logout', LogoutView, name='logout'),

    path('api/login', login_api, name="api_login"),
]

# if settings.DEBUG:
#     from django.contrib.staticfiles.urls import staticfiles_urlpatterns
#     urlpatterns += staticfiles_urlpatterns()
