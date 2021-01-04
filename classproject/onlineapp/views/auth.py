from debug_toolbar.panels import logging
from django.views import View
from onlineapp.models import *
from onlineapp.forms import *
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import resolve
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import logging


def my_first_view(request):
    logger = logging.getLogger("onlineapp")
    logger.info("this is a debug")
    logger.error("whys is this coming as error")
    return HttpResponse("<body>firstview</body>")



class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        title = "Login"

        if request.user.is_authenticated:
            return redirect('colleges_list')

        return render(request,
                      template_name="onlineapp/login_form.html",
                      context={
                          'title': title,
                          'form': form,
                      })

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            next = request.GET.get('next')
            if next:
                return HttpResponseRedirect(next)

            return redirect('colleges_list')
        else:
            messages.error(request, "Invalid Credentials")
            form = LoginForm(request.POST)

            title = "Login"
            return render(request,
                          template_name="onlineapp/login_form.html",
                          context={
                              'title': title,
                              'form': form,
                          })


class SignupView(View):

    def get(self, request, *args, **kwargs):
        form = SignupForm()
        title = "SignUp"

        return render(request,
                      template_name="onlineapp/signup_form.html",
                      context={
                          'title': title,
                          'form': form,
                      })

    def post(self, request, *args, **kwargs):

        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(**form.cleaned_data)
            user.save()

            if user:
                login(request, user)
            else:
                messages.error(request, "Invalid Credentials")
                form = LoginForm(request.POST)

        title = "Signup"
        return render(request,
                      template_name="onlineapp/signup_form.html",
                      context={
                        'title': title,
                        'form': form,
                      })


def LogoutView(request):
    logout(request)
    return redirect('login')


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login_api(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)
