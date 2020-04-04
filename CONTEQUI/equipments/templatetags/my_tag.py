from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()
from equipments.models import *
from users.models import *
from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.utils import timezone

@register.simple_tag
def my_tag(pk):
    chave = int(pk)
    teste = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = chave)).values_list('user_loan',flat=True)
    #teste = Equipment_user.objects.get(devolution=None,equiment=Equipment.objects.get(id = chave))
    #data = {}
    #data['object_list'] = teste
    if teste:
        a = ''.join(map(str, teste))
        p = Client.objects.filter(id=a).values_list('usuario',flat=True)
        client = ''.join(map(str, p))
        return client
    return ''

@register.simple_tag
def my_tag2(pk):
    chave = int(pk)
    teste = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = chave)).values_list('loan',flat=True)
    #teste = Equipment_user.objects.get(devolution=None,equiment=Equipment.objects.get(id = chave))
    #data = {}
    #data['object_list'] = teste
    if teste:
        a = ''.join(map(str, teste))
        DataHora = a.split()
        Data = DataHora[0]
        Data = Data.split('-')
        Hora = DataHora[1]
        Hora = Hora.split('.')
        Hora = Hora[0]
        #Hora = Hora.split(':')
        print(timezone.now())
        #print(timezone.now()+3)
        a = Data[2]+'/'+Data[1]+'/'+Data[0]+' - '+Hora
        #a2 =  a.strftime("%d/%m/%Y %H:%M:%S")
        #p = Client.objects.filter(id=a).values_list('usuario',flat=True)
        #client = ''.join(map(str, p))
        return a
    return ''

@register.simple_tag
def my_tag3(pk):
    chave = int(pk)
    teste = Equipment.objects.filter(id=chave).values_list('tag',flat=True)
    #teste = Equipment_user.objects.get(devolution=None,equiment=Equipment.objects.get(id = chave))
    #data = {}
    #data['object_list'] = teste
    if teste:
        a = ''.join(map(str, teste))
        #DataHora = a.split()
        #Data = DataHora[0]
        #Data = Data.split('-')
        #Hora = DataHora[1]
        #Hora = Hora.split('.')
        #Hora = Hora[0]
        #Hora = Hora.split(':')
        #print(timezone.now())
        #print(timezone.now()+3)
        #a = Data[2]+'/'+Data[1]+'/'+Data[0]+' - '+Hora
        #a2 =  a.strftime("%d/%m/%Y %H:%M:%S")
        #p = Client.objects.filter(id=a).values_list('usuario',flat=True)
        #client = ''.join(map(str, p))
        return a
        
    return ''

@register.simple_tag
def my_tag4(pk):
    chave = int(pk)
    teste = Equipment.objects.filter(id=chave).values_list('description',flat=True)
    #teste = Equipment_user.objects.get(devolution=None,equiment=Equipment.objects.get(id = chave))
    #data = {}
    #data['object_list'] = teste
    if teste:
        a = ''.join(map(str, teste))
        #DataHora = a.split()
        #Data = DataHora[0]
        #Data = Data.split('-')
        #Hora = DataHora[1]
        #Hora = Hora.split('.')
        #Hora = Hora[0]
        #Hora = Hora.split(':')
        #print(timezone.now())
        #print(timezone.now()+3)
        #a = Data[2]+'/'+Data[1]+'/'+Data[0]+' - '+Hora
        #a2 =  a.strftime("%d/%m/%Y %H:%M:%S")
        #p = Client.objects.filter(id=a).values_list('usuario',flat=True)
        #client = ''.join(map(str, p))
        return a
        
    return ''

@register.simple_tag
def my_tag5(pk):
    chave = int(pk)
    teste = Equipment.objects.filter(id=chave).values_list('type_equipment',flat=True)
    #teste = Equipment_user.objects.get(devolution=None,equiment=Equipment.objects.get(id = chave))
    #data = {}
    #data['object_list'] = teste
    if teste:
        a = ''.join(map(str, teste))
        teste = Equipment_type.objects.filter(id=int(a)).values_list('name',flat=True)
        a = ''.join(map(str, teste))
        #DataHora = a.split()
        #Data = DataHora[0]
        #Data = Data.split('-')
        #Hora = DataHora[1]
        #Hora = Hora.split('.')
        #Hora = Hora[0]
        #Hora = Hora.split(':')
        #print(timezone.now())
        #print(timezone.now()+3)
        #a = Data[2]+'/'+Data[1]+'/'+Data[0]+' - '+Hora
        #a2 =  a.strftime("%d/%m/%Y %H:%M:%S")
        #p = Client.objects.filter(id=a).values_list('usuario',flat=True)
        #client = ''.join(map(str, p))
        return a
        
    return ''

@register.simple_tag
def my_tag6(pk):
    chave = int(pk)
    teste = Equipment.objects.filter(id=chave).values_list('amount_of_loans',flat=True)
    #teste = Equipment_user.objects.get(devolution=None,equiment=Equipment.objects.get(id = chave))
    #data = {}
    #data['object_list'] = teste
    if teste:
        a = ''.join(map(str, teste))
        #DataHora = a.split()
        #Data = DataHora[0]
        #Data = Data.split('-')
        #Hora = DataHora[1]
        #Hora = Hora.split('.')
        #Hora = Hora[0]
        #Hora = Hora.split(':')
        #print(timezone.now())
        #print(timezone.now()+3)
        #a = Data[2]+'/'+Data[1]+'/'+Data[0]+' - '+Hora
        #a2 =  a.strftime("%d/%m/%Y %H:%M:%S")
        #p = Client.objects.filter(id=a).values_list('usuario',flat=True)
        #client = ''.join(map(str, p))
        return a
        
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
def Atraso(pk):
    Equipment_time = Equipment.objects.filter(id = pk).values_list('maximum_time',flat=True)
    Maximum_Time = ''.join(map(str, Equipment_time))
    TimeEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).values_list('loan',flat=True)
    BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).values_list('user_loan',flat=True)
    #data = {}
    #data['Time']=TimeEquipment
    #print('Time' in data)
    #timedelta(minutes=60)
    #Time = ''.join(map(str, TimeEquipment))
    if str(timezone.now()) >= '2020-04-04 17:55':
        return 'Atrasado'