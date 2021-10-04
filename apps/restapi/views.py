from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.accountuser.models import UserAccount
from apps.logchecker.models import District
from apps.restapi.pagination import CustomLimitPagination, CustomPagePagination
from apps.restapi.serializers import (
                                        ClientSerializer, 
                                        RegisterSerializer, 
                                        UserAccountGetUpdateSerializer
                                    )


class UserAccountListAPIView(generics.ListAPIView):
    serializer_class = RegisterSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]
    pagination_class = CustomPagePagination
    filter_backends = [SearchFilter,OrderingFilter,]
    search_fields = ['id', 'email', 'username', 'created']

    def get_queryset(self, *args, **kwargs):
        queryset_list = UserAccount.objects.all()
        return queryset_list


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAccount.objects.all()
    serializer_class = RegisterSerializer


@api_view(['POST',])
@permission_classes([AllowAny,])
def registerview(request):
    serializer = RegisterSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        useraccount = serializer.save()
        # token = Token.objects.get(user=useraccount).key
        data['response'] = "successfully registered a new user"
        data['email'] = useraccount.email
        data['username'] = useraccount.username
        # data['token'] = token
    else:
        data = serializer.errors
    return Response(data)


@api_view(['GET',])
def useraccountlistapiview(request):
    useraccount_list = UserAccount.objects.all()
    serializer = RegisterSerializer(useraccount_list, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT',])
def get_update_useraccountapiview(request):
    try:
        useraccount = request.user
    except UserAccount.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserAccountGetUpdateSerializer(useraccount)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserAccountGetUpdateSerializer(useraccount, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "UserAccount updated OK"
            data['id'] = useraccount.id
            data['email'] = useraccount.email
            data['username'] = useraccount.username
            data['password'] = useraccount.password
            return Response(data=data)
        data['response'] = "Verify wrong data"
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(views.APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        context = {}
        email = request.POST.get('username')
        password = request.POST.get('password')
        useraccount = authenticate(email=email, password=password)
        if useraccount:
            try:
                token = Token.objects.get(user=useraccount)
            except Token.DoesNotExist:
                token = Token.objects.create(user=useraccount)
            context['response'] = 'Successfully authenticated.'
            context['id'] = useraccount.id
            context['email'] = email
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'
        return Response(context)
