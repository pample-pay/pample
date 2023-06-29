from db.models import DRUGSTORE_TB
from .serializer import DsSerializer
from .modules import get_harversion_distance

from django.db.models import F
from django.http import HttpResponseForbidden

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class DrugstoreInfo(APIView):
    """
    현재 위치를 기반으로 주변 약국 정보를 반환해주는 API
    가장 가까운 순으로 10km이내, 최대 20개로 sorting해서 return한다.
    
    post data 형식
    {
        "mylng" : "현재 경도 값",
        "mylat" : "현재 위도 값"
    }
    """

    # def get(self, request):
    #     return HttpResponseForbidden()

    def post(self, request):
        crt = 10     # 기준, 단위 km
        try: 
            mylng= float(request.data['mylng'])
            mylat= float(request.data['mylat'])
        except KeyError:
            return Response(
                {'message': 'Key error'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            result = DRUGSTORE_TB.objects.annotate(
                distance = get_harversion_distance(
                    F('drugstore_lat'),
                    F('drugstore_lng'),
                    mylat,
                    mylng
                )
            ).filter(distance__lt=crt).order_by('distance')[:20]

            serializer_li = []
            for i in (result):
                serializer = DsSerializer(i).data
                serializer_li.append(serializer)
                
            return Response(serializer_li)