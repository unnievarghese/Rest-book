from rest_framework.views import APIView
from api.serializers import bookserializers,loginserializer
from api.models import book
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.contrib.auth import login as book_login,logout as book_logout
from rest_framework.authtoken.models import Token

class booklist(APIView):
    def get(self,request,format=None):
        books=book.objects.all()
        serializer=bookserializers(books,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    def post(self,request,format=None):
        serializer=bookserializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class bookdetail(APIView):
    authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_object(self,pk):
        return book.objects.get(id=pk)

    def get(self,request,pk,format=None):
        book=self.get_object(pk)
        serializer=bookserializers(book)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def put(self,request,pk,format=None):
        book=self.get_object(pk)
        serializer=bookserializers(book,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        book=self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_200_OK)

class loginview(APIView):
    def post(self,request):
        serializer=loginserializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        book_login(request,user)
        token,created=Token.objects.get_or_create(user=user)
        return Response({'token':token.key},status=200)

class logoutview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        book_logout(request)
        return Response(status=status.HTTP_200_OK)