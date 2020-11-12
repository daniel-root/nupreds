from equipments.models import *
from users.models import *
from django.utils import timezone
from users.APIs.sendEmail import email_cadastro
from users.APIs.sendTelegram import autenticar, aleatorio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import telepot



def email_atraso(name, equipment, tag, description,msgFrom):
	try:
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            msgTo = 'nupreds@gmail.com'
            toPass = 'hYV83BBDA2ebx8r'
            smtpObj.login(msgTo, toPass)
            msgFrom = str(msgFrom)		
            msg = MIMEMultipart('alternative')
            text ="""
            Olá, """ + str(name) + """, tudo bem? 
            Notamos que você está muito tempo com """ + str(equipment) + """, """ + str(tag) + """ - """ + str(description) + """. Quando você puder dirija-se à recepção para fazer a devolução ou realizar novamente o empréstimo deste equipamento."""
            html = """\
            <html>
            <head></head>
            <body>
                    <p>Olá, """ + str(name) + """, tudo bem?</p>
            <p>Notamos que você está muito tempo com """ + str(equipment) + """, """ + str(tag) + """ - """ + str(description) + """. Quando você puder dirija-se à recepção para fazer a devolução ou realizar novamente o empréstimo deste equipamento.</p>
            </body>
            </html>
            """
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')
            msg.attach(part1)
            msg.attach(part2)
            smtpObj.sendmail(msgTo,msgFrom,'Subject: Atraso!\n{}'.format( msg.as_string()))
            smtpObj.quit()
            
            return True
	except:
            return False

def enviar(name, equipment, tag, description,number):
    try:
            name = str(name)
            equipment= str(equipment)
            tag = str(tag)
            description = str(description)
            number = int(number)
            bot = telepot.Bot("1244766207:AAGjFP8KytsFILHQUjXazo1yV7JUqN5w4g8")
            #print(bot)  
            bot.sendMessage(number,"Olá, "+ name + ", tudo bem? \n Notamos que você está muito tempo com " + equipment + ", " + tag + " - " + description + ". Quando você puder dirija-se à recepção para fazer a devolução ou realizar novamente o empréstimo deste equipamento.")
    except:
		    pass


def Atraso():
    #print("Aqui")
    TimeEquipment = Equipment_user.objects.filter(devolution=None)
    for time in TimeEquipment:
        if timezone.now() >= time.limit_time:
            #print(time.equipment)
            equipment = Equipment.objects.filter(id = time.equipment)
            if equipment[0].email_sent == False:
                
                user = Client.objects.filter(usuario=time.user_loan)
                cod_telegram = user[0].cod_telegram
                #print("vou enviar!")
                internet = email_atraso(user[0].usuario, equipment[0].type_equipment, equipment[0].tag, equipment[0].description,user[0].email)
                if internet:
                    continue
                else:
                    equipment.update(email_sent=False)
                equipment.update(status='Atrasado')
                if cod_telegram[0] != 'D':
                    enviar(user[0].usuario, equipment[0].type_equipment, equipment[0].tag, equipment[0].description,user[0].cod_telegram)

def TelegramCadastro():
    cod_telegram = Client.objects.filter(cod_telegram__contains='D')
    if cod_telegram:
        for cod in cod_telegram:
            atualiza_cod_telegrma = autenticar(str(cod.cod_telegram))
            if atualiza_cod_telegrma != 'Vazia' and atualiza_cod_telegrma != False:
                Client.objects.filter(id=cod.id).update(cod_telegram=atualiza_cod_telegrma)
            elif atualiza_cod_telegrma == 'Vazia':
                break
    else:
        pass

def EmailsNotSend():
    try:    
        users = Client.objects.filter(cod_telegram=None)
        #print(users)
        if users:
            #print("passei")
            for user in users:
                #print(user.usuario)
                number = aleatorio()
                internet = email_cadastro(user.usuario,number,user.email)
                if internet:
                    Client.objects.filter(id=user.id).update(cod_telegram=number)
    except:
        pass