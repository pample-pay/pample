from .models import DRUGSTORE
from .serializer import DsSerializer
from modules import get_harversion_distance

from django.http import JsonResponse
from django.db.models import F

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class DrugstoreInfo(APIView):
    """
    현재 위치를 기반으로 주변 약국 정보를 반환해주는 API
    약국은 5km내외의, 가장 가까운 순으로 20개 sorting해서 보내줌.
    현재 위치는 https 로부터 받음.
    
    get data 형태
    {
        'mylng' : 현재 경도 값,
        'mylat' : 현재 위도 값,
    }

    get 요청을 받으면 return
    [
        {   
            'drugstore_name' : 약국 이름,
            'drugstore_zipcode' : 약국 우편번호,
            'drugstore_address' : 약국 주소,
            'drugstore_open', : 개점일
            'drugstore_lng' : 경도 값,
            'drugstore_lat' : 위도 값,
            'drugstore_associate' : 제휴 여부       # 0=False, 1=True
        }, ...
    ]
    """

    def get(self, request):
        crt = 5     # 기준, 5km
        
        mylng= request.GET.get('mylng')
        mylat= request.GET.get('mylat')

        # None일시 팜플 지도로 대체
        if mylng is None:
            mylng = 126.895845
        if mylat is None:
            mylat = 37.486505

        try:
            serializer_li = []

            result = DRUGSTORE.objects.annotate(
                distance = get_harversion_distance(F('drugstore_lat'),
                                                   F('drugstore_lng'),
                                                   mylat,
                                                   mylng)
                ).filter(distance__lt=crt).order_by('distance')[:20]
            
            for i in (result):
                serializer = DsSerializer(i).data
                serializer_li.append(serializer)
        
        except KeyError:
            return Response({'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer_li)