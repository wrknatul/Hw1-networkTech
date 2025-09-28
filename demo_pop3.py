#!/usr/bin/env python3

from pop3_client import POP3Client

def demo_pop3_workflow():
    """Демонстрация рабочего процесса POP3 клиента"""
    print("=== ДЕМОНСТРАЦИЯ POP3 КЛИЕНТА ===\n")
    
    print("1. Создание клиента и подключение к серверу")
    print("   client = POP3Client()")
    print("   client.connect('pop.gmail.com', 995, use_ssl=True)")
    print("   # Результат: +OK Gpop ready for requests...\n")
    
    print("2. Аутентификация пользователя")
    print("   client.authenticate('user@gmail.com', 'app_password')")
    print("   # Команды: USER user@gmail.com -> +OK send PASS")
    print("   #          PASS app_password -> +OK Authentication successful\n")
    
    print("3. Получение списка писем")
    print("   messages = client.get_mail_list()")
    print("   # Команда: LIST")
    print("   # Результат:")
    print("   # +OK 3 messages (1234 bytes)")
    print("   # 1 512")
    print("   # 2 456")
    print("   # 3 266")
    print("   # .\n")
    
    print("4. Получение содержимого первого письма")
    print("   message_content = client.get_message('1')")
    print("   # Команда: RETR 1")
    print("   # Результат:")
    print("   # +OK 512 bytes")
    print("   # Return-Path: <sender@example.com>")
    print("   # Received: from mail.example.com")
    print("   # Date: Mon, 28 Sep 2025 10:00:00 +0000")
    print("   # From: sender@example.com")
    print("   # To: user@gmail.com")
    print("   # Subject: Test Message")
    print("   # ")
    print("   # This is the body of the email message.")
    print("   # .\n")
    
    print("5. Завершение сессии")
    print("   client.quit()")
    print("   # Команда: QUIT")
    print("   # Результат: +OK Bye\n")
    
    print("=== ПРИМЕР ИСПОЛЬЗОВАНИЯ ===")
    print("python3 pop3_client.py pop.gmail.com user@gmail.com app_password")
    print("\nДля Gmail необходимо:")
    print("- Включить двухфакторную аутентификацию")
    print("- Создать пароль приложения")
    print("- Использовать пароль приложения вместо обычного пароля")

def show_pop3_commands():
    """Показать основные команды POP3"""
    print("\n=== ОСНОВНЫЕ КОМАНДЫ POP3 ===")
    commands = [
        ("USER <username>", "Указать имя пользователя"),
        ("PASS <password>", "Указать пароль"),
        ("LIST", "Получить список писем с размерами"),
        ("RETR <msg_id>", "Получить письмо по ID"),
        ("DELE <msg_id>", "Пометить письмо для удаления"),
        ("QUIT", "Завершить сессию"),
        ("STAT", "Получить статистику (количество писем и общий размер)"),
        ("TOP <msg_id> <lines>", "Получить заголовки и первые N строк письма")
    ]
    
    for command, description in commands:
        print(f"{command:<20} - {description}")

def show_common_servers():
    """Показать настройки популярных почтовых серверов"""
    print("\n=== НАСТРОЙКИ ПОПУЛЯРНЫХ СЕРВЕРОВ ===")
    servers = [
        ("Gmail", "pop.gmail.com", "995", "SSL", "Требует пароль приложения"),
        ("Yandex", "pop.yandex.ru", "995", "SSL", "Требует включения POP3 в настройках"),
        ("Mail.ru", "pop.mail.ru", "995", "SSL", "Стандартная аутентификация"),
        ("Outlook/Hotmail", "outlook.office365.com", "995", "SSL", "Требует пароль приложения"),
        ("Yahoo", "pop.mail.yahoo.com", "995", "SSL", "Требует пароль приложения")
    ]
    
    print(f"{'Сервис':<15} {'Сервер':<25} {'Порт':<6} {'SSL':<4} {'Примечание'}")
    print("-" * 80)
    for service, server, port, ssl, note in servers:
        print(f"{service:<15} {server:<25} {port:<6} {ssl:<4} {note}")

if __name__ == "__main__":
    demo_pop3_workflow()
    show_pop3_commands()
    show_common_servers()
