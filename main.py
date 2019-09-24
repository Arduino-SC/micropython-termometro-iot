import time
import dht
import machine
import urequests as requests

DHT_PIN = 2
API_THINGSPEAK_HOST = 'https://api.thingspeak.com/update'
THINGSPEAK_WRITE_KEY = '' # put your key here
MESUREMENT_INTERVAL = 300
DELAY = 30


def do_temp():
    try:
        d = dht.DHT11(machine.Pin(DHT_PIN))
        d.measure()

        t = d.temperature()
        h = d.humidity()
    except OSError as err:
        t = 0
        h = 0

    print('temperature = %.2f' % t)
    print('humidity    = %.2f' % h)

    global THINGSPEAK_WRITE_KEY

    if not THINGSPEAK_WRITE_KEY:
        print('not ThingSpeak key specified, skip sending data')
        return

    print('send data to ThingSpeak')

    data = '{"field1":"%.2f", "field2": "%.2f"}' % (t, h)

    headers = {'X-THINGSPEAKAPIKEY': THINGSPEAK_WRITE_KEY,
               'Content-type': 'application/json'}

    r = requests.post(API_THINGSPEAK_HOST, data=data, headers=headers)
    results = r.json()

    print(results)

last_mesurement_time = 0

while True:
    current_time = time.time()

    if current_time - last_mesurement_time > MESUREMENT_INTERVAL:
        do_temp()
        last_mesurement_time = current_time

    time.sleep(DELAY)
