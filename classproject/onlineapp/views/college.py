from django.views import View
from onlineapp.models import *
from onlineapp.forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User,Permission
from onlineapp.serializers import CollegeSerializer
from django.forms.models import model_to_dict
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes




class CollegeView(LoginRequiredMixin, View):

    login_url = 'login'

    def get(self, request, *args, **kwargs):

        template = "onlineapp/colleges_list.html"

        # if request.user.is_superuser:
        #     user_permissions = [permission['name'] for permission in Permission.objects.values('name')]
        # else:
        user_permissions = [permission['name'] for permission in request.user.user_permissions.values('name')]

        params = {'user_permissions': user_permissions}

        if kwargs:
            college = get_object_or_404(College, **kwargs)
            students = college.student_set.order_by('-mocktest1__total')
            template = "onlineapp/student_list.html",
            params.update({
                    'student_list': students,
                    'college': college,
                })
        else:
            colleges = College.objects.values('id', 'name', 'acronym')
            params.update({'colleges_list': colleges})
        return render(
            request,
            template_name=template,
            context=params,
        )


class AddCollegeView(PermissionRequiredMixin, LoginRequiredMixin, View):
    login_url = 'login'
    permission_required = ('onlineapp.add_college','onlineapp.change_college','onlineapp.delete_college')

    def get(self, request, *args, **kwargs):
        form = AddCollege()
        title = "Add College"
        button = "Add"
        if kwargs:
            college = get_object_or_404(College, **kwargs)
            form = AddCollege(instance=college)
            title = "Edit College Details"
            button = "Edit"

        return render(request,
                      template_name="onlineapp/college_form.html",
                      context={
                          'title': title,
                          'form': form,
                          'button': button,
                      })

    def post(self, request, **kwargs):

        title = "Add College"
        button = "Add"
        if kwargs:
            college = get_object_or_404(College, **kwargs)
            if resolve(request.path_info).url_name == 'del_college':
                college.delete()
                return redirect('colleges_list')

            title = "Edit College"
            button = "Edit"
            form = AddCollege(request.POST, instance=college)
            pass
        else:
            form = AddCollege(request.POST)
        if form.is_valid():
            form.save()
            return redirect('colleges_list')


        return render(request,
                      template_name="onlineapp/college_form.html",
                      context={
                          'title': title,
                          'form': form,
                          'button': button,
                      })
        # response.write("<br><b class=\"subtitle\" style=\"color:red;\">Errors:</b>")
        # response.write(form.errors)
        # return response


@csrf_exempt
@api_view(['GET', 'POST'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def college_api(request):

    if request.method == 'GET':

        colleges = College.objects.all()
        serializer = CollegeSerializer(colleges, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CollegeSerializer(data=data)
        #print(serializer.errors)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
# @authentication_classes((SessionAuthentication, BasicAuthentication))
# @permission_classes((IsAuthenticated,))
def college_modify_api(request, *args, **kwargs):
    college = get_object_or_404(College, **kwargs)
    if request.method == 'GET':
        serializer = CollegeSerializer(college, many=False)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CollegeSerializer(college, data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)

    elif request.method == 'DELETE':
        college.delete()
        return HttpResponse(status=200)