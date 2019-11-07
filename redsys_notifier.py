import json
import os

import requests
from datetime import date, timedelta

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is only used in dev envs

USERNAME = os.getenv("REDSYS_USERNAME")
PASSWORD = os.getenv("REDSYS_PASSWORD")

headers = {'Content-Type': 'application/json;charset=UTF-8'}
data = {"username": USERNAME, "password": PASSWORD}
response = requests.post('https://canales.redsys.es/admincanales-web/services/usuarios/login', headers=headers, data=json.dumps(data))

headers['admincanales-auth-token'] = response.json()['token']

today = date.today()
yesterday = today - timedelta(days=1)
today_date = today.strftime("%d-%m-%Y")
yesterday_date = yesterday.strftime("%d-%m-%Y")

data = {"data": {"comercio": USERNAME, "terminal": None, "fechaIni": "29-10-2019", "fechaFin": today_date,
                 "tipo": None, "resultado": None, "horaIni": "00:00:00", "horaFin": "23:59:59", "pedido": None,
                 "order": "fechaNotificacion,horaNotificacion", "direction": "ASC", "tempHoraInicio": "0",
                 "tempMinutoInicio": "0", "tempHoraFin": "23", "tempMinutoFin": "59"},
        "page": 0, "size": "100", "order": "fechaNotificacion,horaNotificacion", "direction": "ASC"}

nots = requests.post('https://canales.redsys.es/admincanales-web/services/notificaciones/consulta', headers=headers, data=json.dumps(data)).json()
if nots['numberOfElements'] != nots['totalElements']:
    raise Exception("More elements than page size")

unsuccessful_notifications = [notif['detalleResultado'] for notif in nots['content'] if notif['resultadoNotificacion'] != 'S']
if len(unsuccessful_notifications) != 0:
    print("Notifications with errors:")
    for un in unsuccessful_notifications:
        print("\t", un)
    raise Exception("fml")  # Hopefully if the actions fails Github will notify me, so I don't have to implement it.
print("No unsuccessful_notifications found")


