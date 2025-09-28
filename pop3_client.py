#!/usr/bin/env python3


import socket
import ssl
import sys
import re

class POP3Client:
    def __init__(self):
        self.socket = None
        self.connected = False
        self.authenticated = False
    
    def connect(self, server, port=110, use_ssl=False):
        try:
            print(f"Подключение к {server}:{port}")

            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(30)

            self.socket.connect((server, port))

            if use_ssl:
                context = ssl.create_default_context()
                self.socket = context.wrap_socket(self.socket, server_hostname=server)

            response = self._receive_response()
            print(f"Сервер: {response}")
            
            if response.startswith('+OK'):
                self.connected = True
                return True
            else:
                print("Ошибка подключения к серверу")
                return False
                
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False
    
    def _send_command(self, command):
        """Отправка команды на сервер"""
        try:
            self.socket.send((command + '\r\n').encode('utf-8'))
            return True
        except Exception as e:
            print(f"Ошибка отправки команды: {e}")
            return False
    
    def _receive_response(self):
        """Получение ответа от сервера"""
        try:
            response = self.socket.recv(4096).decode('utf-8', errors='ignore')
            return response.strip()
        except Exception as e:
            print(f"Ошибка получения ответа: {e}")
            return None
    
    def _receive_multiline_response(self):
        """Получение многострочного ответа (например, список писем)"""
        try:
            response_lines = []
            while True:
                line = self.socket.recv(1024).decode('utf-8', errors='ignore')
                if not line:
                    break
                
                response_lines.append(line)
                
                # Проверяем, не закончился ли ответ
                if line.endswith('\r\n.\r\n'):
                    break
                elif line == '.\r\n':
                    break
            
            return ''.join(response_lines)
        except Exception as e:
            print(f"Ошибка получения многострочного ответа: {e}")
            return None
    
    def authenticate(self, username, password):
        """Аутентификация пользователя"""
        if not self.connected:
            print("Нет подключения к серверу")
            return False
        
        try:
            if not self._send_command(f"USER {username}"):
                return False
            
            response = self._receive_response()
            print(f"USER: {response}")
            
            if not response.startswith('+OK'):
                print("Ошибка аутентификации: неверное имя пользователя")
                return False
            
            # Отправляем команду PASS
            if not self._send_command(f"PASS {password}"):
                return False
            
            response = self._receive_response()
            print(f"PASS: {response}")
            
            if response.startswith('+OK'):
                self.authenticated = True
                print("Аутентификация успешна!")
                return True
            else:
                print("Ошибка аутентификации: неверный пароль")
                return False
                
        except Exception as e:
            print(f"Ошибка аутентификации: {e}")
            return False
    
    def get_mail_list(self):
        """Получение списка писем"""
        if not self.authenticated:
            print("Необходима аутентификация")
            return None

        if not self._send_command("LIST"):
            return None
        
        response = self._receive_multiline_response()
        print("\n=== СПИСОК ПИСЕМ ===")
        print(response)

        messages = []
        lines = response.split('\r\n')
        for line in lines:
            if line and not line.startswith('+OK') and line != '.':
                parts = line.split()
                if len(parts) >= 2:
                    msg_id = parts[0]
                    msg_size = parts[1]
                    messages.append({'id': msg_id, 'size': msg_size})
        
        return messages

    
    def get_message(self, message_id):
        if not self.authenticated:
            print("Необходима аутентификация")
            return None
        
        try:
            if not self._send_command(f"RETR {message_id}"):
                return None
            
            response = self._receive_multiline_response()
            return response
            
        except Exception as e:
            print(f"Ошибка получения письма: {e}")
            return None
    
    def get_message_info(self, message_id):
        if not self.authenticated:
            print("Необходима аутентификация")
            return None
        
        try:
            if not self._send_command(f"TOP {message_id} 0"):
                return None
            
            response = self._receive_multiline_response()
            return response
            
        except Exception as e:
            print(f"Ошибка получения информации о письме: {e}")
            return None
    
    def quit(self):
        if self.connected:
            try:
                self._send_command("QUIT")
                response = self._receive_response()
                print(f"QUIT: {response}")
            except:
                pass
        
        if self.socket:
            self.socket.close()
            self.connected = False
            self.authenticated = False

def main():
    if len(sys.argv) != 4:
        print("Использование: python pop3_client.py <сервер> <логин> <пароль>")
        print("Пример: python pop3_client.py pop.gmail.com user@gmail.com password")
        print("\nДля демонстрации можно использовать тестовые данные:")
        print("python pop3_client.py pop.gmail.com test@gmail.com testpass")
        sys.exit(1)
    
    server = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    port = 995
    use_ssl = True

    if server == "localhost" or "test" in server:
        port = 110
        use_ssl = False
    
    client = POP3Client()
    
    try:
        if not client.connect(server, port, use_ssl):
            print("Не удалось подключиться к серверу")
            sys.exit(1)

        if not client.authenticate(username, password):
            print("Не удалось аутентифицироваться")
            sys.exit(1)

        messages = client.get_mail_list()
        
        if messages and len(messages) > 0:
            print(f"\nНайдено писем: {len(messages)}")

            first_message_id = messages[0]['id']
            print(f"\n=== СОДЕРЖИМОЕ ПЕРВОГО ПИСЬМА (ID: {first_message_id}) ===")
            
            message_content = client.get_message(first_message_id)
            if message_content:
                print(message_content)
            else:
                print("Не удалось получить содержимое письма")
        else:
            print("Письма не найдены")
    
    except KeyboardInterrupt:
        print("\nПрерывание пользователем")
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client.quit()

if __name__ == "__main__":
    main()
