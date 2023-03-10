# get secret key
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def get_secret(setting, secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)
    

# calcuate harversion distance
import math
from django.db.models import Func

class Sin(Func):
    function = 'SIN'
class Cos(Func):
    function = 'COS'
class ATan2(Func):
    function = 'ATan2'
class Sqrt(Func):
    function = 'SQRT'
class Round(Func):
  function = 'ROUND'


def degree2radius(degree):
    return degree * (math.pi/180)

def get_harversion_distance(x1, y1, x2, y2, precision=5):
    """
    경위도 (x1,y1)과 (x2,y2) 점의 거리를 반환
    Harversion Formula 이용하여 2개의 경위도간 거래를 구함(단위:Km)
    """

    R = 6371 # 지구의 반경(단위: km)
    dLon = degree2radius(x2-x1)   
    dLat = degree2radius(y2-y1)
    a = Sin(dLat/2) * Sin(dLat/2) \
        + (Cos(degree2radius(y1)) \
          *Cos(degree2radius(y2)) \
          *Sin(dLon/2) * Sin(dLon/2))
    b = 2 * ATan2(Sqrt(a), Sqrt(1-a))
    
    return Round(R * b, precision=5)
