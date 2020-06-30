from equipments.models import *
from users.models import *
from django.utils import timezone
from users.APIs.sendEmail import email_atraso
from users.APIs.sendTelegram import autenticar, enviar

def Atraso(pk):
    Equipment_time = Equipment.objects.filter(id = pk).values_list('maximum_time',flat=True)
    Maximum_Time = ''.join(map(str, Equipment_time))
    TimeEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk))
    BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).values_list('user_loan',flat=True)
    for time in TimeEquipment:
        if timezone.now() >= time.limit_time:
            equipment = Equipment.objects.filter(id = pk)
            equipment.update(status='Atrasado')

def TelegramCadastro():
    cod_telegram = Client.objects.filter(cod_telegram__contains='D')
    if cod_telegram:
        for i in range(0,len(cod_telegram)):
            atualiza_cod_telegrma = autenticar(str(cod_telegram[i].cod_telegram))
            if atualiza_cod_telegrma != 'Vazia' and atualiza_cod_telegrma != False:
                Client.objects.filter(id=cod_telegram[i].id).update(cod_telegram=atualiza_cod_telegrma)
            elif atualiza_cod_telegrma == 'Vazia':
                break