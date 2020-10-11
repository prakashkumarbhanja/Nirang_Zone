from django.http.response import Http404
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import login

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView

from django.core.mail import send_mail, BadHeaderError

from .models import Userprofile
from .serializers import UserSerializer, UserSerUpdateSerializer


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serialized = UserSerializer(data=request.data)
        if serialized.is_valid():
            email = request.POST.get('email')
            print('*********', email)
            username = request.POST.get('username')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            phone_no = request.POST.get('phone_no')
            message = "Thanks for Registering with Us!!! I am welcoming you."

            try:
                send_mail("Welcome Message", message, 'pkbhanja07@gmail.com', [email, ], fail_silently=True)
            except BadHeaderError:
                return Response("Invalid Header Found")
            # return Response("Your email has send")

            user = User.objects.create_user(username=username, email=email)
            # user.set_password
            Userprofile.objects.create(user=user, phone_no=phone_no)
            user.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class Login(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(Login, self).post(request, format=None)

class Update_Delete_User(APIView):

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerUpdateSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = UserSerUpdateSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

