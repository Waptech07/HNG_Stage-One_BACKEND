from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import requests
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

    def get(self, request):
        # Get the visitor's name from the query parameter
        visitor_name = request.GET.get('visitor_name', 'Guest')

        # Get client IP address
        client_ip = self.getIP()

        if not client_ip:
            # Handle case where IP address could not be retrieved
            response_data = {
                'client_ip': 'Unknown',
                'location': 'Unknown',
                'greeting': f'Hello, {visitor_name}!, we could not determine your IP address'
            }
            return JsonResponse(response_data)

        # Use ipapi to get the location based on IP
        ipapi_url = f'https://ipapi.co/{client_ip}/json/'

        try:
            # Fetch location data from ipapi
            location_response = requests.get(ipapi_url)
            if location_response.status_code == 200:
                # Extract location details
                location_data = location_response.json()
                city = location_data.get('city', 'Unknown')
                latitude = location_data.get('latitude')
                longitude = location_data.get('longitude')

                # Get weather data from OpenWeatherMap API
                weather_api_key = '268178537a976a43f5adc4694c2f80c1'
                weather_response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={weather_api_key}')

                if weather_response.status_code == 200:
                    # Extract temperature from weather data
                    weather_data = weather_response.json()
                    temperature = weather_data['main']['temp']

                    response_data = {
                        'client_ip': client_ip,
                        'location': city,
                        'greeting': f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {city}'
                    }
                else:
                    # Handle case where weather data retrieval fails
                    response_data = {
                        'client_ip': client_ip,
                        'location': city,
                        'greeting': f'Hello, {visitor_name}!, we could not retrieve the weather information for {city}'
                    }
            else:
                # Handle case where location data retrieval fails
                response_data = {
                    'client_ip': client_ip,
                    'location': 'Unknown',
                    'greeting': f'Hello, {visitor_name}!, we could not determine your location'
                }
        except requests.RequestException as e:
            # Handle request exception errors
            response_data = {
                'client_ip': client_ip,
                'location': 'Unknown',
                'greeting': f'Hello, {visitor_name}!, there was an error while fetching data: {str(e)}'
            }
            
        return JsonResponse(response_data)
