import gc
import webrepl

def do_connect():
    import network

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('SSID_DA_SUA_REDE', 'SENHA_DA_SUA_REDE')

        while not wlan.isconnected():
            pass

    print('network config:', wlan.ifconfig())


def do_ntp():
    from ntptime import settime

    settime()

webrepl.start()
gc.collect()

do_connect()
do_ntp()

