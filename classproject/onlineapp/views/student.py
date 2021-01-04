from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from onlineapp.models import *
from onlineapp.forms import *
from django.http import HttpResponseRedirect
from django.urls import resolve
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from onlineapp.serializers import *
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class StudentView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):

        user_permissions = [permission['name'] for permission in request.user.user_permissions.values('name')]

        student = get_object_or_404(Student, **kwargs)
        return render(
            request,
            template_name="onlineapp/student.html",
            context={
                'student': student,
                'user_permissions': user_permissions,
            }
        )

    def post(self, request, *args, **kwargs):

        students = Student.objects.filter(**{'college__acronym': 'vce'}).order_by('-mocktest1__total')
        template = "onlineapp/student_list.html"
        params = {}
        return render(
            request,
            template_name=template,
            context=params,
        )

class AddStudentView(View):
    login_url = 'login'

    def get(self, request, *args, **kwargs):

        student_form = AddStudent()
        mock_form = AddMock1()
        title = "Add Student"
        button = "Add"

        if resolve(request.path_info).url_name == 'edit_student':
            student = Student.objects.get(**kwargs)
            mock = MockTest1.objects.get(student=student)
            student_form = AddStudent(instance=student)
            mock_form = AddMock1(instance=mock)
            title = "Edit Student Details"
            button = "Edit"


        return render(request,
                      template_name="onlineapp/student_form.html",
                      context={
                          'title': title,
                          'student_form': student_form,
                          'mock_form': mock_form,
                          'button': button,
                      })

    def post(self, request, **kwargs):

        student_form = None
        mock = None
        title = "Add Student"
        button = "Add"
        if resolve(request.path_info).url_name == 'add_student':
            college = College(**kwargs)
            student = Student(college=college)
            student_form = AddStudent(request.POST, instance=student)

            if student_form.is_valid():
                student_form.save()
            total = sum([int(request.POST['problem' + str(i)]) for i in range(1, 5)])
            mock = MockTest1(student=student, total=total)

        if resolve(request.path_info).url_name == 'edit_student':
            student = Student.objects.get(**kwargs)
            kwargs['id'] = student.college.id
            student_form = AddStudent(request.POST, instance=student)
            if student_form.is_valid():
                student_form.save()
            total = sum([int(request.POST['problem' + str(i)]) for i in range(1, 5)])
            mock = MockTest1.objects.get(student=student)
            mock.total = total
            title = "Edit Student"
            button = "Edit"

        if resolve(request.path_info).url_name == 'del_student':
            student = Student.objects.get(**kwargs)
            kwargs['id'] = student.college.id
            # m = MockTest1.objects.get(student=student)
            student.delete()
            # m.delete()
            return redirect('college_details', **kwargs)

        mock_form = AddMock1(request.POST, instance=mock)
        if mock_form.is_valid():
            mock_form.save()
            return redirect('college_details', **kwargs)


        return render(request,
                      template_name="onlineapp/student_form.html",
                      context={
                          'title': title,
                          'student_form': student_form,
                          'mock_form': mock_form,
                          'button': button,
                      })
        # response.write("<br><b class=\"subtitle\" style=\"color:red;\">Errors:</b>")
        # response.write(form.errors)
        # return response


class StudentApiView(APIView):
    # authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        if 'id' in kwargs:
            students = Student.objects.filter(id=kwargs['id'])
        else:
            college = College.objects.get(id=kwargs["cid"])
            students = Student.objects.filter(college=college)
        serializer = StudentDetailsSerializer(students, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, **kwargs):

        college = College.objects.get(id=kwargs["cid"])
        student = Student(college=college)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(serializer.errors, status=400)

        data = serializer.data
        errors = serializer.errors

        if 'mocktest1' in request.data:
            mock1 = MockTest1(student=student)
            mockserializer = MockTest1Serializer(mock1, data=request.data['mocktest1'])
            if mockserializer.is_valid():
                mockserializer.save()
                data.update({'mocktest1': mockserializer.data})
                return JsonResponse(data, status=201)

            errors.update({'mocktest1': mockserializer.errors})

        elif serializer.is_valid():
            return JsonResponse(data, status=201)
        return JsonResponse(errors, status=400)

    def put(self, request, **kwargs):
        #college = College.objects.get(id=kwargs["cid"])
        print(kwargs)
        student = Student.objects.get(id=kwargs['id'])
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return JsonResponse(serializer.errors, status=400)
        data = serializer.data
        errors = serializer.errors
        if 'mocktest1' in request.data:
            try:
                mock1 = MockTest1.objects.get(student=student)
            except:
                mock1 = MockTest1(student=student)
            mockserializer = MockTest1Serializer(mock1, data=request.data['mocktest1'])
            if mockserializer.is_valid():
                mockserializer.save()
                data.update({'mocktest1': mockserializer.data})
                return JsonResponse(data, status=201)

            errors.update({'mocktest1': mockserializer.errors})

        elif serializer.is_valid():
            return JsonResponse(data, status=201)
        return JsonResponse(errors, status=400)

    def delete(self, request, **kwargs):
        student = Student.objects.get(id=kwargs['id'])
        student.delete()
        return HttpResponse(status=200)
