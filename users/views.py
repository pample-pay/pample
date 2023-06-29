import jwt

from .models import User, Pharmacist
from .serializers import *

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from pample.settings import SECRET_KEY

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


def test_veiw(request):
    return render(request, 'users/test.html')


class RegisterAPIView(APIView):
    # 회원가입
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register successs",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            
            return res
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class AuthAPIView(APIView):
    # 로그인
    def post(self, request):
    	# 유저 인증 username=user_id, password=password
        user = authenticate(username=request.data.get("user_id"), password=request.data.get("password"))
        # 이미 회원가입 된 유저일 때
        if user is not None:
            serializer = UserSerializer(user)
            # jwt 토큰 접근
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "login success",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    

class IdValidation(APIView):
    # 아이디 중복검사
    def post(self, request):
        try:
            user_id = request.data['user_id']
            try: user = User.objects.get(user_id=user_id)
            except Exception as e: user = None
            context = {'data' : "not exist" if user is None else "exist"}

        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # return {'data' : "not exist"} or {'data' : "exist"}
            return JsonResponse(context)
        

class ChangePassword(APIView):
    # 비밀번호 변경
    # 변경되는 비밀번호 key 값 'password1'
    def post(self, request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token_type, access = token.split(' ')

            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)

            password = request.data['password1']
            user.set_password(password)
            user.save()

            return Response({'message': 'Password Change'})

        except:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        
    

class TokenValidAPIView(APIView):
    # 토큰 유효성 검증
    def post(self, request):
        try:
            # access token을 decode 해서 유저 id 추출 => 유저 식별
            token = request.META.get('HTTP_AUTHORIZATION')
            token_type, access = token.split(' ')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
            serializer = UserSerializer(instance=user)
            data = serializer.data

            if serializer.data['user_type'] == "3" and Pharmacist.objects.get(user=user).store is not None:
                drug_info = {'drug_id' : str(Pharmacist.objects.get(user=user).store)}
            else:
                drug_info = {'drug_id' : None}

            return Response({**data, **drug_info}, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
