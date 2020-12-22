import requests
import json
from datetime import date
import urllib.parse
import pprint as p
accuweatherAPIKey = 'tJGK5OHFnAbw3l2ltA5hrxvSGDg1W5Sc'
mapBoxAPIToken = 'pk.eyJ1IjoiZHJpZnRlcms5IiwiYSI6ImNraXpiaXZ6bTAwdTkzMGx1dG9rbW1remkifQ.VmTzqmXbIHfF-QtWs5gagg'
dia_semana = ['Domingo', 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado']

def pegarPrevisao5Dias(codigoLocal):

    DailyAPIUrl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"\
                            + codigoLocal + "?apikey=" + accuweatherAPIKey + \
                             "&language=pt-br&metric=true"
    r = requests.get(DailyAPIUrl)
    if (r.status_code != 200):
        print('não foi possível obter o clima do local.')
        return None
    else:
        try:
            DailyResponse = (json.loads(r.text))
            infoClima5Dias = []
            for dia in DailyResponse['DailyForecasts']:
                climaDia = {}
                climaDia['max'] = dia['Temperature']['Maximum']['Value']
                climaDia['min'] = dia['Temperature']['Minimum']['Value']
                climaDia['clima'] = dia['Day']['IconPhrase']
                diaSemana = int(date.fromtimestamp(dia['EpochDate']).strftime("%w"))
                climaDia['dia'] = dia_semana[diaSemana]
                infoClima5Dias.append(climaDia)
            return infoClima5Dias
        except:
            return None

def pegarCoordenadas():
    r = requests.get('http://www.geoplugin.net/json.gp')

    if (r.status_code != 200):
        print('não foi possível obter a localização.')
        return None
    else:
        try:
            localizacao = (json.loads(r.text))
            coordenadas = {}
            coordenadas['lat'] = localizacao['geoplugin_latitude']
            coordenadas['long'] = localizacao['geoplugin_longitude']
            return coordenadas
        except:
            return None

def pegarCodigoLocal(lat, long):
    locationAPIUrl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/" \
                     +"search?apikey=" + accuweatherAPIKey \
                      +"&q=" + lat + "%2C"+long+"%20"
    r = requests.get(locationAPIUrl)
    if (r.status_code != 200):
        print('não foi possível obter o codigo do local.')
        return None
    else:
        try:
            LocationResponse = json.loads(r.text)
            infoLocal = {}
            infoLocal['nomeLocal'] = LocationResponse['LocalizedName'] + ", "\
                        + LocationResponse['AdministrativeArea']['LocalizedName']+ ". "\
                        + LocationResponse['Country']['LocalizedName']
            infoLocal['codigoLocal'] = LocationResponse['Key']
            return infoLocal
        except:
            return None

def pegarTempoAgora(codigoLocal, nomeLocal):

    currentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/"\
                            + codigoLocal + "?apikey=" + accuweatherAPIKey + \
                             "&language=pt-br"
    r = requests.get(currentConditionsAPIUrl)
    if (r.status_code != 200):
        print('não foi possível obter o clima do local.')
        return None
    else:
        try:
            currentConditionsResponse = (json.loads(r.text))
            infoClima = {}
            infoClima['textoClima'] = currentConditionsResponse[0]["WeatherText"]
            infoClima['temperatura'] = currentConditionsResponse[0]['Temperature']['Metric']['Value']
            infoClima['nomeLocal'] = nomeLocal
            return infoClima
        except:
            return None
## inicio
def mostrarPrevisao(lat, long):
    try:
        local = pegarCodigoLocal(lat, long)
        climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
        print('Clima atual em: ' + climaAtual['nomeLocal'])
        print(climaAtual['textoClima'])
        print('Temperatura: ' + str(climaAtual['temperatura']) + "\xb0" + "C")
    except:
        print('\nErro ao obter clima atual.')

    opcao = input('\nDeseja ver a previsão para os próximos dias?(s ou n) ').lower()
    if opcao == 's':
        try:
            print('\nClima para hoje e para os próximos 5 dias:\n')
            previsao5Dias = pegarPrevisao5Dias(local['codigoLocal'])
            for dia in previsao5Dias:
                print(dia['dia'])
                print('Mínima: ' + str(dia['min']) + "\xb0" + "C")
                print('Máxima: ' + str(dia['max']) + "\xb0" + "C")
                print('Clima: ' + dia['clima'])
                print('-------------------------')
        except:
            print('Erro ao obter a previsão para os próximos dias.')

def pesquisarLocal(local):
    _local = urllib.parse.quote(local)
    mapboxGeocodeUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/" \
                       + _local + ".json?access_token=" + mapBoxAPIToken
    r = requests.get(mapboxGeocodeUrl)
    if (r.status_code != 200):
        print('não foi possível obter o clima do local.')
        return None
    else:
        try:
            mapboxResponse = json.loads(r.text)
            coodenadas = {}
            coodenadas['long'] = str(mapboxResponse['features'][0]['geometry']['coordinates'][0])
            coodenadas['lat'] = str(mapboxResponse['features'][0]['geometry']['coordinates'][1])
            return coodenadas
        except:
            print('Erro na pesquisa do local, contate o suporte técnico.')
try:
    coordenadas = pegarCoordenadas()
    mostrarPrevisao(coordenadas['lat'], coordenadas['long'])

    continuar = "s"

    while continuar == 's':
        continuar = input('Deseja consultar a previsão de outro local?(s ou n): ').lower()
        if continuar != "s":
            break
        local = input("Digite a cidade e o estado: ")
        try:
            coordenadas = pesquisarLocal(local)
            mostrarPrevisao(coordenadas['lat'], coordenadas['long'])
        except:
            print('\nnão foi possível obter a previsão pra esse local.')
except:
    print('Erro ao processar a solicitação. entre em contato com o suporte técnico.')