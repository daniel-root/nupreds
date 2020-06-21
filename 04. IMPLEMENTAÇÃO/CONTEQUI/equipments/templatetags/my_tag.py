from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
from equipments.models import *
from users.models import *
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.utils import timezone
from users.APIs.sendEmail import email_atraso
from users.APIs.sendTelegram import autenticar, enviar

def UserEquipmentInUse(pk):
    equipment_user = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).values_list('user_loan',flat=True)
    return equipment_user

def UserNameUnique(pk):
    user = Client.objects.filter(id=pk).values_list('usuario',flat=True)
    return user

@register.simple_tag
def NameUser(pk):
    if UserEquipmentInUse(pk):
        EquipmentUser = ''.join(map(str, UserEquipmentInUse(pk)))
        return ''.join(map(str, UserNameUnique(int(EquipmentUser))))
    return ''

@register.simple_tag
def DateTimeLoan(pk):
    DateTimeEquipmentUser = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).values_list('loan',flat=True)
    if DateTimeEquipmentUser:
        DateTime = ''.join(map(str, DateTimeEquipmentUser))
        DateTime = DateTime.split()
        Date = DateTime[0]
        Date = Date.split('-')
        Time = DateTime[1]
        Time = Time.split('.')
        Time = Time[0]
        DateTime = Date[2]+'/'+Date[1]+'/'+Date[0]+' - '+ Time
        return DateTime
    return ''

def NameEquipment(pk,value):
    name_equipment = Equipment.objects.filter(id=pk).values_list(value,flat=True)
    return name_equipment

@register.simple_tag
def TagName(pk):
    if NameEquipment(pk,'tag'):
        return ''.join(map(str, NameEquipment(pk,'tag')))
    return ''

@register.simple_tag
def DescriptionName(pk):
    if NameEquipment(pk,'description'):
        return ''.join(map(str, NameEquipment(pk,'description')))
    return ''

@register.simple_tag
def TypeName(pk):
    if NameEquipment(pk,'type_equipment'):
        type_name = Equipment_type.objects.filter(id=int(''.join(map(str, NameEquipment(pk,'type_equipment'))))).values_list('name',flat=True)
        return ''.join(map(str, type_name))  
    return ''

@register.simple_tag
def LoanOrDevolution(pk):
    chave = int(pk)
    BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = chave)).values_list('user_loan',flat=True)
    if BusyEquipment:
        return 'Devolução'
    return 'Emprestimo'

@register.simple_tag
def ActiveOrInactive(pk):
    ActiveEquipment = Equipment.objects.filter(id = pk,inative=False)
    if ActiveEquipment:
        return 'Desativar'
    return 'Ativar'

@register.simple_tag
def ActiveOrInactiveType(pk):
    ActiveEquipment = Equipment_type.objects.filter(id = pk,inative=False)
    if ActiveEquipment:
        return 'Desativar'
    return 'Ativar'

@register.simple_tag
def ActiveOrInactiveUser(pk):
    ActiveEquipment = Client.objects.filter(id = pk,inative=False)
    if ActiveEquipment:
        return 'Desativar'
    return 'Ativar'


@register.simple_tag
def Atraso(pk):
    cod_telegram = Client.objects.filter(cod_telegram__contains='D')
    if cod_telegram:
        for i in range(0,len(cod_telegram)):
            print(cod_telegram[i].cod_telegram)
            atualiza_cod_telegrma = autenticar(str(cod_telegram[i].cod_telegram))
            if atualiza_cod_telegrma != False:
                Client.objects.filter(id=cod_telegram[i].id).update(cod_telegram=atualiza_cod_telegrma)
    Equipment_time = Equipment.objects.filter(id = pk).values_list('maximum_time',flat=True)
    Maximum_Time = ''.join(map(str, Equipment_time))
    TimeEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk))
    BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).values_list('user_loan',flat=True)
    for time in TimeEquipment:
        if timezone.now() >= time.limit_time:
            equipment = Equipment.objects.filter(id = pk)
            equipment.update(status='Atrasado')
            user = Equipment_user.objects.filter(equipment = pk, user_devolution=None)
            user = Client.objects.filter(usuario=user[0].user_loan)
            cod_telegram = user[0].cod_telegram
            if cod_telegram[0] != 'D' and cod_telegram != None:
                enviar(user[0].usuario, equipment[0].type_equipment, equipment[0].tag, equipment[0].description,user[0].cod_telegram)

            #type_equipment = Equipment_type.objects.filter(id=equipment[0].type_equipment)
            print(user[0].usuario, equipment[0].type_equipment, equipment[0].tag, equipment[0].description,user[0].email)
            email_atraso(user[0].usuario, equipment[0].type_equipment, equipment[0].tag, equipment[0].description,user[0].email)
            #time = str(timezone.now() - time.limit_time)
            #time = time.split('.')
            #time = time[0]
            return ''
            #+' '+time
        return ''
    return ''
