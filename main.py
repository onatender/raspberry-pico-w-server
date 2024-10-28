import network
import urequests
import time
from machine import Pin

# Yerleşik LED için Pin ayarı (Raspberry Pi Pico W'de GPIO 25)
led = Pin(15, Pin.OUT)
led2 = Pin("LED", Pin.OUT)

# Wi-Fi ağına bağlanma fonksiyonu
def connect_wifi(ssid, password):
    led2.off()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Wi-Fi\'a bağlanılıyor...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Wi-Fi bağlı:', wlan.ifconfig())
    led2.on()
    print("yakildi")
    

# JSON veri kontrol fonksiyonu
def check_json_data():
    try:
        # URL'ye istek gönder
        print("aliniyor")
        response = urequests.get('http://192.168.1.35:8080/data.json')
        print("alindi")
        if response.status_code == 200:  # Eğer istek başarılıysa
            json_data = response.json()  # Yanıtı JSON olarak al
            print("veri",json_data)
            # JSON verisindeki 'data' anahtarını kontrol et
            if 'data' in json_data and json_data['data'] > 500:
                led.on()  # data > 500 ise LED'i yak
                print("Veri 500'den büyük, LED yakıldı.")
            else:
                led.off()  # data <= 500 ise LED'i söndür
                print("Veri 500'den küçük veya eşit, LED söndürüldü.")
        
        response.close()  # Yanıtı kapat
        
    except Exception as e:
        print("Bir hata oluştu:", e)

# Wi-Fi bilgilerinizi girin
SSID = 'SSID_HERE'
PASSWORD = 'PW_HERE'

# Wi-Fi'ya bağlan ve durumu sürekli kontrol et
try:
    connect_wifi(SSID, PASSWORD)
    
    while True:
        check_json_data()  # JSON verisini kontrol et
        time.sleep(1)  # Her 10 saniyede bir isteği tekrar et
        
except KeyboardInterrupt:
    print("Program durduruldu.")

