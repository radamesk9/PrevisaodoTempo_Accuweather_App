import requests
import json
import pprint
accuweatherAPIKey = 'tJGK5OHFnAbw3l2ltA5hrxvSGDg1W5Sc'
#r = requests.get('https://www.google.com')
#r.status_code
#r.headers
#r.headers['Date']
#r.text
#

r = requests.get('http://www.geoplugin.net/json.gp')

if (r.status_code != 200):
    print('não foi possível obter a localização.')
else:
    localizacao = (json.loads(r.text))
    lat = localizacao['geoplugin_latitude']
    long = localizacao['geoplugin_longitude']
    locationAPIUrl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/" \
                     +"search?apikey=" + accuweatherAPIKey \
                      +"&q=" + lat + "%2C"+long+"%20"
    r2 = requests.get(locationAPIUrl)
    if (r2.status_code != 200):
        print('não foi possível obter o codigo do local.')
    else:
        LocationResponse = json.loads(r2.text)
        nameLocal = LocationResponse['LocalizedName'] + ", "\
                    + LocationResponse['AdministrativeArea']['LocalizedName']+ ". "\
                    + LocationResponse['Country']['LocalizedName']
        codigoLocal = LocationResponse['Key']

    print('obtendo clima do local... ', nameLocal)

    currentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/"\
                            + codigoLocal + "?apikey=" + accuweatherAPIKey + \
                             "&language=pt-br"

    r3 = requests.get(currentConditionsAPIUrl)
    if (r3.status_code != 200):
        print('não foi possível obter a localização.')
    else:
        currentConditionsResponse = (json.loads(r3.text))
        textoClima = currentConditionsResponse[0]["WeatherText"]
        temperatura = currentConditionsResponse[0]['Temperature']['Metric']['Value']
        print('clima: ' + textoClima)
        print('Temperatura: '+ str(temperatura)+ " Graus Celsius.")