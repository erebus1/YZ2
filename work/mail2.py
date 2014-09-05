__author__ = 'user'

import smtplib
import sys
def mail(msg = 'ok',toaddr = '380913023815@sms.utel.ua'):
    #Параметр, передаваемый при запуске скрипта:
    # txtparam=sys.argv[1]
    # txtparam="W"
    #От кого:
    fromaddr = 'Mr. Robot <someaccount@gmail.com>'
    #Кому:
    # toaddr = '380913023815@sms.utel.ua'
    #Тема письма:
    # subj = 'Notification from system'
    #Текст сообщения:
    # msg_txt = 'Notice:\n\n ' +  txtparam + '\n\nBye!' #
    #Создаем письмо (заголовки и текст)
    # msg = "From: %s\nTo: %s\nSubject: %s\n\n%s"  % ( fromaddr, toaddr, subj, msg_txt)
    # msg="privet"
    #Логин gmail аккаунта. Пишем только имя ящика.
    #Например, если почтовый ящик someaccount@gmail.com, пишем:
    username = 'uaticket.yz@gmail.com'
    #Соответственно, пароль от ящика:
    password = 'openTicket14'

    #Инициализируем соединение с сервером gmail по протоколу smtp.
    server = smtplib.SMTP('smtp.gmail.com:587')
    #Выводим на консоль лог работы с сервером (для отладки)
    # server.set_debuglevel(1);
    #Переводим соединение в защищенный режим (Transport Layer Security)
    server.starttls()
    #Проводим авторизацию:
    server.login(username,password)
    #Отправляем письмо:
    server.sendmail(fromaddr, toaddr, msg)
    #Закрываем соединение с сервером
    server.quit()