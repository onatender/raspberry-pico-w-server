import http.server
import socketserver
import json

# Sunmak istediğiniz JSON dosyasının yolu
JSON_FILE_PATH = 'data.json'
PORT = 8080  # İstediğiniz port numarası

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    # Gelen GET isteğine yanıt veriyoruz
    def do_GET(self):
        if self.path == '/data.json':  # JSON dosyasına gelen istek
            try:
                with open(JSON_FILE_PATH, 'r') as file:
                    json_data = json.load(file)  # JSON dosyasını oku
                    self.send_response(200)  # HTTP 200 OK yanıtı
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(json_data).encode())  # JSON verisini gönder
            except Exception as e:
                self.send_response(500)  # Eğer dosya açılmazsa HTTP 500 hata kodu
                self.end_headers()
                self.wfile.write(str(e).encode())  # Hata mesajı gönder
        else:
            self.send_response(404)  # Yanlış path isteğinde 404 döndür
            self.end_headers()

# HTTP Sunucusu oluştur
with socketserver.TCPServer(("", PORT), MyRequestHandler) as httpd:
    print(f"Sunucu {PORT} portunda çalışıyor. JSON dosyası için http://localhost:{PORT}/data.json")
    httpd.serve_forever()
