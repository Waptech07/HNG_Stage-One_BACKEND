from rest_framework.views import APIView
from urllib.request import urlopen
import re as r

# Create your views here.

class HelloView(APIView):
    def getIP(self):
        try:
            d = str(urlopen('http://checkip.dyndns.com/').read())
            ip_address = r.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(d).group(1)
        except Exception as e:
            ip_address = None
        return ip_address    