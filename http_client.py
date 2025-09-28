#!/usr/bin/env python3

import socket
import ssl
from urllib.parse import urlparse
import sys

class HTTPClient:
    def __init__(self):
        self.socket = None
    
    def parse_url(self, url):
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        
        parsed = urlparse(url)
        return {
            'scheme': parsed.scheme,
            'hostname': parsed.hostname,
            'port': parsed.port or (443 if parsed.scheme == 'https' else 80),
            'path': parsed.path or '/',
            'query': parsed.query
        }
    
    def create_socket(self, hostname, port, is_https):
        """Создание сокета и подключение к серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(30)

            self.socket.connect((hostname, port))

            if is_https:
                context = ssl.create_default_context()
                self.socket = context.wrap_socket(self.socket, server_hostname=hostname)
            
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def send_request(self, hostname, path, query):
        full_path = path
        if query:
            full_path += '?' + query

        request = (
            f"GET {full_path} HTTP/1.1\r\n"
            f"Host: {hostname}\r\n"
            f"User-Agent: Custom-HTTP-Client/1.0\r\n"
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            f"Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3\r\n"
            f"Accept-Encoding: identity\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )
        
        try:
            self.socket.send(request.encode('utf-8'))
            return True
        except Exception as e:
            print(f"Ошибка отправки запроса: {e}")
            return False
    
    def receive_response(self):
        try:
            response = b""
            while True:
                chunk = self.socket.recv(4096)
                if not chunk:
                    break
                response += chunk
            
            return response.decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"Ошибка получения ответа: {e}")
            return None
    
    def parse_response(self, response):
        if not response:
            return None, None
        
        parts = response.split('\r\n\r\n', 1)
        if len(parts) == 2:
            headers = parts[0]
            body = parts[1]
        else:
            headers = response
            body = ""
        
        return headers, body
    
    def fetch_url(self, url):
        print(f"Запрос к URL: {url}")
        print("=" * 60)
        
        url_info = self.parse_url(url)
        print(f"Подключение к: {url_info['hostname']}:{url_info['port']}")
        
        is_https = url_info['scheme'] == 'https'
        if not self.create_socket(url_info['hostname'], url_info['port'], is_https):
            return False
        
        if not self.send_request(url_info['hostname'], url_info['path'], url_info['query']):
            return False
        
        response = self.receive_response()
        if not response:
            return False
        
        headers, body = self.parse_response(response)
        
        print("\n=== HTTP ЗАГОЛОВКИ ===")
        print(headers)
        print("\n" + "=" * 60)
        print("=== СОДЕРЖИМОЕ СТРАНИЦЫ ===")
        print(body)
        print("=" * 60)
        
        return True
    
    def close(self):
        if self.socket:
            self.socket.close()

def main():
    if len(sys.argv) != 2:
        print("Использование: python http_client.py <URL>")
        print("Пример: python http_client.py http://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    client = HTTPClient()
    
    try:
        success = client.fetch_url(url)
        if not success:
            print("Не удалось получить страницу")
            sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    main()
