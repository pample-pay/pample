import os
import jwt
import uuid
import json
import boto3
import secretkey

from pathlib import Path
from collections import OrderedDict
from itertools import islice

from users.models import User, Pharmacist
from pample.settings import SECRET_KEY
from .serializers import *

from db.models import DRUGSTORE_TB, DRUGSTORE_VIEW_TB

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


# AWS 업로드용 class 정의
class S3ImgUploader:
    def __init__(self, file):
        self.file = file

    def upload(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        AWS_secrets = os.path.join(BASE_DIR, 'AWS_secrets.json')

        with open(AWS_secrets) as f:
            AWS_secrets_key = json.loads(f.read())

        s3_client = boto3.client(
            's3',
            aws_access_key_id     = secretkey.get_secret("aws_access_key_id", AWS_secrets_key),
            aws_secret_access_key = secretkey.get_secret("aws_secret_access_key", AWS_secrets_key)
        )

        url = 'img'+'/'+uuid.uuid1().hex
        
        s3_client.upload_fileobj(
            self.file, 
            "pample-api-bucket", 
            url, 
            ExtraArgs={
                "ContentType": self.file.content_type
            }
        )
        return url


# 글 작성 및 수정 
# 글 작성 관련 권한은 Header에 포함된 JWT 토큰으로 받음 / 만약 불일치시 401 에러
# 작성은 201, 수정은 200 response 각각 리턴
class BlogList(APIView):
    serializer_class = DlSerializer
    # 새로운 List 작성
    def post(self, request):
        # request.data는 사용자의 입력 데이터
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token_type, access = token.split(' ')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            if user.user_type == "3" and Pharmacist.objects.get(user=user).store is not None:
                serializer = DlSerializer(data=request.data)
                if serializer.is_valid(): #유효성 검사
                    pharmacist = Pharmacist.objects.get(user=user)
                    serializer.validated_data['drugstore'] = pharmacist.store
                    url = S3ImgUploader(serializer.validated_data['drugstore_thumbnail']).upload()
                    serializer.validated_data['drugstore_thumbnail'] = 'https://pample-api-bucket.s3.ap-northeast-2.amazonaws.com/' + url
                    # 상세페이지가 존재하는지 검사
                    dl_instance = DRUGSTORE_VIEW_TB.objects.filter(Q(drugstore=pharmacist.store)).first()
                
                    if dl_instance:
                        # 상세페이지 존재시 업데이트
                        serializer.update(dl_instance, serializer.validated_data)
                        return Response(
                            json.dumps(OrderedDict(islice(serializer.validated_data.items(), 3)),
                                       ensure_ascii=False , indent='\t'),
                            status=status.HTTP_200_OK)
                    else:
                        # 상세페이지 미존재시 글 업로드
                        dl_instance = serializer.create(serializer.validated_data)
                        return Response(
                            json.dumps(OrderedDict(islice(serializer.validated_data.items(), 3)),
                                       ensure_ascii=False , indent='\t'),
                            status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)


class ListDetail(APIView):
    # List 객체 가져오기
    def get_object(self, pk):
        try:
            return DRUGSTORE_VIEW_TB.objects.get(pk=pk)
        # Default 값 정의
        except DRUGSTORE_VIEW_TB.DoesNotExist:
            arb_instance = DRUGSTORE_VIEW_TB(
                drugstore = DRUGSTORE_TB.objects.get(pk=pk),
                drugstore_thumbnail = "https://pample-api-bucket.s3.ap-northeast-2.amazonaws.com/noimg/noimg.png",
                drugstore_abstract = "등록된 게시물이 없습니다.",
                drugstore_content = "등록된 게시물이 없습니다."
            )
            return arb_instance
    # List detail 보기
    def get(self, request, pk, format=None):
        list = self.get_object(pk)

        serializer1 = DlViewSerializer(list)
        serializer2 = DrugStoreSerializer(list.drugstore)

        return Response({**serializer1.data, **serializer2.data},)
    # List 삭제하기
    def delete(self, request, pk, format=None):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            token_type, access = token.split(' ')
            payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_object_or_404(User, pk=pk)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            if Pharmacist.objects.get(user=user).store == DRUGSTORE_VIEW_TB.objects.get(pk=pk).drugstore:
                list = self.get_object(pk)
                list.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
    