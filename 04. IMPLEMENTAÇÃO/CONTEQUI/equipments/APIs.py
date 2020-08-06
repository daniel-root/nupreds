from equipments.models import *
from users.models import *
from django.utils import timezone
from users.APIs.sendEmail import email_atraso, email_cadastro
from users.APIs.sendTelegram import autenticar, enviar, aleatorio

def Atraso():
    TimeEquipment = Equipment_user.objects.filter(devolution=None)
    for time in TimeEquipment:
        if timezone.now() >= time.limit_time:
            print(time.equipment)
            equipment = Equipment.objects.filter(id = time.equipment)
            if equipment[0].status != 'Atrasado':
                
                user = Client.objects.filter(usuario=time.user_loan)
                cod_telegram = user[0].cod_telegram
                print("vou enviar!")
                internet = email_atraso(user[0].usuario, equipment[0].type_equipment, equipment[0].tag, equipment[0].description,user[0].email)
                if internet:
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
    users = Client.objects.filter(cod_telegram=None)
    print(users)
    if users:
        print("passei")
        for user in users:
            print(user.usuario)
            number = aleatorio()
            internet = email_cadastro(user.usuario,number,user.email)
            if internet:
                Client.objects.filter(id=user.id).update(cod_telegram=number)