from django.shortcuts import render, redirect, get_object_or_404
from equipments.models import *
from equipments.APIs import *
from datetime import datetime, timedelta
from users.models import *
from django.db.models import Q
from django.utils import timezone
from django.contrib import messages
from users.APIs.fingerPrint import *
import io
from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter, landscape, A4
from reportlab.platypus import Table
from reportlab.platypus import Image
from reportlab.platypus import TableStyle
from reportlab.lib import colors
 
def home(request):
    if request.session.has_key('username'):
        TelegramCadastro()
        EmailsNotSend()
        return render(request,'home.html')
    return render(request,'login.html')

def EquipmentTypeAll():
    equipment_type = Equipment_type.objects.all().values('name')
    return equipment_type

def EquipmentTypeAllOrderBy(value):
    equipment_type = Equipment_type.objects.all().order_by(value)
    return equipment_type

def EquipmentTypeUnique(pk):
    equipment_type = get_object_or_404(Equipment_type, pk=pk) 
    return equipment_type   

def equipment_type_list(request, templete_name='equipments/equipment_type_list.html'):
    data = {}
    data['object_list'] = Equipment_type.objects.all()
    return render(request, templete_name, data)

def equipment_type_order_by(request,value, templete_name='equipments/equipment_type_list.html'):
    data = {}
    data['object_list'] = EquipmentTypeAllOrderBy(value)
    return render(request, templete_name, data)

def equipment_type_view(request, pk, template_name='equipments/equipment_type_detail.html'):   
    return render(request, template_name, {'object':EquipmentTypeUnique(pk)})

def equipment_type_create(request, template_name='equipments/equipment_type_form.html'):
    if request.method=='POST':
        equipment_type = Equipment_type.objects.filter(name = request.POST['tag'])
        if not equipment_type:
            new_equipment_type = Equipment_type.objects.create(
                name=request.POST['tag'],
                time_maximum=request.POST['time_type'])
            return redirect('equipment_type_list')
        else:
            messages.error(request, 'Tipo de equipamento já existe!')
            data['equipment_type'] = {'name':request.POST['tag'],'time_maximum':request.POST['time_type']}
            return render(request, template_name, data)
    return render(request, template_name)

def equipment_type_update(request, pk, template_name='equipments/equipment_type_form.html'):
    equipment_type = Equipment_type.objects.filter(pk=pk)
    if request.method=='POST':
        equipment_type.update(
            name=request.POST['tag'],
            time_maximum=request.POST['time_type'])
        return redirect('equipment_type_list')
    return render(request, template_name, {'equipment_type':equipment_type})

def equipment_type_delete(request, pk, template_name='equipments/equipment_type_confirm_delete.html'):
    if request.session.has_key('username'):
        if request.method=='POST': 
            if Equipment_type.objects.filter(id = pk,inative='True'):
                Equipment_type.objects.filter(id = pk).update(inative='False')
                equipments = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id=pk)).update(inative='False')
            else:
                Equipment_type.objects.filter(id = pk).update(inative='True')
                equipments = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id=pk)).update(inative='True')
            return redirect('equipment_type_list')
            #return equipment_list(request)
        return render(request, template_name, {'object':EquipmentTypeUnique(pk)})
    return render(request, 'login.html')

def EquipmentActiveAll():
    equipment = Equipment.objects.filter(inative=False).order_by('status','tag')
    return equipment

def EquipmentAll():
    equipment = Equipment.objects.filter(inative=True,type_equipment__inative=False).order_by('status','tag')
    return equipment

def EquipmentUnique(pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return equipment

from django.core.paginator import Paginator
def get_page(request,objects):
    objetcs = objects
    paginator = Paginator(objetcs,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def equipment_list(request,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        #print("passei por equipment_list")
        data = {}
        equipment_list = EquipmentActiveAll()
        data['list_equipment'] = get_page(request,equipment_list)
        data['equipments'] = EquipmentActiveAll()
        data['type_equipment']= EquipmentTypeAll()
        data['type'] = 'Todos'
        data['search'] = 'Null'
        Atraso()
        return render(request, templete_name, data)
    return render(request, 'login.html')

def equipment_list_inactive(request,value,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        data = {}
        data['list_equipment'] = get_page(request,EquipmentAll())
        data['type_equipment']= EquipmentTypeAll()
        data['type'] = 'Inativos'
        data['search'] = 'Null'
        #data['type'] = value

        return render(request, templete_name, data)
    return render(request, 'login.html')

def equipment_view(request, pk, template_name='equipments/equipment_detail.html'):
    if request.session.has_key('username'):
        return render(request, template_name, {'object':EquipmentUnique(pk)})
    return render(request, 'login.html')

def equipment_create(request, template_name='equipments/equipment_form.html'):
    if request.session.has_key('username'):
        data = {}
        tipo = Equipment_type.objects.all()
        data['types'] = tipo
        if request.method == 'POST':
            equipment = Equipment.objects.filter( Q(tag=request.POST['tag']) | Q(description=request.POST['description']) ,type_equipment=Equipment_type.objects.get(name = request.POST['type_equipment']))
            if not equipment:
                new_equipment = Equipment.objects.create(
                    tag=request.POST['tag'],
                    description=request.POST['description'],
                    type_equipment=Equipment_type.objects.get(name = request.POST['type_equipment']),
                    maximum_time=request.POST['maximum_time'])
                return redirect('equipment_list')
            else:
                messages.error(request, 'Equipamento já existe!')
                data['equipment'] = {'tag':request.POST['tag'],'description':request.POST['description'],'type_equipment':Equipment_type.objects.get(name = request.POST['type_equipment']),'maximum_time':request.POST['maximum_time']}
                return render(request, template_name, data)
        return render(request, template_name, data)
    return render(request, 'login.html')

def equipment_update(request, pk, template_name='equipments/equipment_form.html'):
    if request.session.has_key('username'):
        data = {}
        tipo = Equipment_type.objects.all()
        data['types'] = tipo
        equipment = get_object_or_404(Equipment, pk=pk)
        data['equipment']= equipment
        if request.method == 'POST':
            equipment = Equipment.objects.filter(pk=pk)
            equipment.update(tag=request.POST['tag'],description=request.POST['description'],type_equipment=Equipment_type.objects.get(name = request.POST['type_equipment']),maximum_time=request.POST['maximum_time'])
            return equipment_list(request)
        return render(request, template_name, data)
    return render(request, 'login.html')

def equipment_delete(request, pk, template_name='equipments/equipment_confirm_delete.html'):
    if request.session.has_key('username'):
        if request.method=='POST': 
            if Equipment.objects.filter(id = pk,inative='True'):
                Equipment.objects.filter(id = pk).update(inative='False')
            else:
                Equipment.objects.filter(id = pk).update(inative='True')
            return redirect('/Equipamentos')
        return render(request, template_name, {'object':EquipmentUnique(pk)})
    return render(request, 'login.html')
count = 0
def emprestar(request,pk):
    global count
    if request.session.has_key('username'):
        username = None
        
        if request.method=='POST':
            username = main("Verification")
            if count >= 2 and username=="N":
                    count = 0
                    data = {}
                    data['pk'] = pk
                    data['tipo'] = 'por_senha'
                    data['list_equipment'] = get_page(request,EquipmentActiveAll())
                    data['type_equipment']= EquipmentTypeAll()
                    data['equipments'] = EquipmentActiveAll()
                    data['type'] = 'Todos'
                    data['search'] = 'Null'
                    messages.error(request, 'Não foi Possível capturar digital! Tente com login e senha.')
                    return render(request, 'equipments/equipment_list.html',data)
            elif username != "Erro ao selecionar dispositivo.":
                post = Client.objects.filter(usuario=username).values_list('id',flat=True)
                if post:
                    count = 0
                    StringPost = ''.join(map(str, post))
                    BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk))
                    amout = Equipment.objects.filter(id = pk).values_list('amount_of_loans',flat=True)
                    amout_of_equipments = ''.join(map(str, amout))
                    if BusyEquipment:
                        messages.error(request, 'Equipamento já emprestado!')
                        return redirect('/Equipamentos')
                        #return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
                    time = Equipment.objects.filter(id = pk).values_list('maximum_time',flat=True)
                    time = ''.join(map(str,time))
                    Equipment.objects.filter(id = pk).update(status='Ocupado',amount_of_loans=(int(amout_of_equipments)+1))
                    Equipment_user.objects.create(loan=timezone.now(),devolution=None,equipment=Equipment.objects.get(id = pk),user_loan=Client.objects.get(id = int(StringPost)),amount_of_loans=int(amout_of_equipments)+1,limit_time=datetime.now()+timedelta(minutes=int(time)))
                    return redirect('/Equipamentos')
                else:
                    messages.error(request, 'Usuário não encontrado, tente novamente! Tentativa ' + str(count+2) + '/3')
                    count = count + 1
                    data = {}
                    data['chave'] = pk
                    data['list_equipment'] = get_page(request,EquipmentActiveAll())
                    data['equipments'] = EquipmentActiveAll()
                    data['type_equipment']= EquipmentTypeAll()
                    data['type'] = 'Todos'
                    data['search'] = 'Null'
                    #messages.error(request, 'Dispositivo não conectado!')
                    return render(request, 'equipments/equipment_list.html', data )
                    #return equipment_list(request)
                    #return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
                return redirect('/Equipamentos')
                #return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})           
            else:
                data = {}
                data['pk'] = pk
                data['tipo'] = 'por_senha'
                data['list_equipment'] = get_page(request,EquipmentActiveAll())
                data['type_equipment']= EquipmentTypeAll()
                data['equipments'] = EquipmentActiveAll()
                data['type'] = 'Todos'
                data['search'] = 'Null'
                messages.error(request, 'Dispositivo não conectado!')
                return render(
                    request,
                    'equipments/equipment_list.html',
                    data
                    )
            return redirect('/Equipamentos')
        return redirect('/Equipamentos')
            #return render(request, 'equipments/emprestar.html', data )
    else:
        return render(request, 'login.html')

def devolver(request,pk):
    global count
    if request.session.has_key('username'):
        username = None
        if request.method=='POST':
            username = main("Verification")
            if count >= 2 and username=="N":
                count = 0
                data = {}
                data['pk'] = pk
                data['tipo'] = 'por_senha'
                data['list_equipment'] = get_page(request,EquipmentActiveAll())
                data['type_equipment']= EquipmentTypeAll()
                data['equipments'] = EquipmentActiveAll()
                data['type'] = 'Todos'
                data['search'] = 'Null'
                messages.error(request, 'Muitas tentativas!')
                return render(request, 'equipments/equipment_list.html',data)

            elif username != "Erro ao selecionar dispositivo.":
                post = Client.objects.filter(usuario=username).values_list('id',flat=True)
                if post:
                    count = 0
                #StringPost = ''.join(map(str, post))
                    BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk))
                    if BusyEquipment:
                        Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).update(user_devolution=Client.objects.get(id = int(post[0])),devolution=timezone.now())
                        Equipment.objects.filter(id = pk).update(status='Livre')
                        return redirect('/Equipamentos')
                    else:
                        messages.error(request, 'Equipamento sem emprestimo!')
                        return equipment_list(request)
                        #return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
                else:
                    messages.error(request, 'Usuário não encontrado, tente novamente! Tentativa ' + str(count+2) + '/3')
                    count = count + 1
                    data = {}
                    data['chave'] = pk
                    data['list_equipment'] = get_page(request,EquipmentActiveAll())
                    data['type_equipment']= EquipmentTypeAll()
                    data['equipments'] = EquipmentActiveAll()
                    data['type'] = 'Todos'
                    data['search'] = 'Null'
                    #messages.error(request, 'Dispositivo não conectado!')
                    return render(request, 'equipments/equipment_list.html', data )
                    
                return equipment_list(request)
            else:
                data = {}
                data['pk'] = pk
                data['tipo'] = 'por_senha'
                data['list_equipment'] = get_page(request,EquipmentActiveAll())
                data['type_equipment']= EquipmentTypeAll()
                data['equipments'] = EquipmentActiveAll()
                data['type'] = 'Todos'
                data['search'] = 'Null'
                messages.error(request, 'Dispositivo não conectado!')
                return render(
                    request,
                    'equipments/equipment_list.html',
                    data
                    )
            return redirect('/Equipamentos')
        return redirect('/Equipamentos')
    else:
        return render(request, 'login.html')

def emprestar_user(request,pk):
    if request.session.has_key('username'):
        if request.method == 'POST':
            
            username = request.POST['username']
            password =  request.POST['password']
            post = Client.objects.filter(usuario=username,senha=password).values_list('id',flat=True)
            if post:
                StringPost = ''.join(map(str, post))
                BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk))
                amout = Equipment.objects.filter(id = pk).values_list('amount_of_loans',flat=True)
                amout_of_equipments = ''.join(map(str, amout))
                if BusyEquipment:
                    messages.error(request, 'Equipamento já emprestado!')
                    return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
                time = Equipment.objects.filter(id = pk).values_list('maximum_time',flat=True)
                time = ''.join(map(str,time))
                Equipment.objects.filter(id = pk).update(status='Ocupado',amount_of_loans=(int(amout_of_equipments)+1))
                Equipment_user.objects.create(loan=timezone.now(),devolution=None,equipment=Equipment.objects.get(id = pk),user_loan=Client.objects.get(id = int(StringPost)),amount_of_loans=int(amout_of_equipments)+1,limit_time=datetime.now()+timedelta(minutes=int(time)))
                return redirect('/Equipamentos')
        return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
    return render(request, 'login.html')

def devolver_user(request,pk):
    if request.session.has_key('username'):
        if request.method == 'POST':   
            username = request.POST['username']
            password =  request.POST['password']
            post = Client.objects.filter(usuario=username,senha=password).values_list('id',flat=True)
            if post:
                #StringPost = ''.join(map(str, post))
                BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk))
                if BusyEquipment:
                    Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).update(user_devolution=Client.objects.get(id = int(post[0])),devolution=timezone.now())
                    Equipment.objects.filter(id = pk).update(status='Livre')
                    return redirect('/Equipamentos')
            messages.error(request, 'Equipamento sem emprestimo!')
            return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
        
        return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
    return render(request, 'login.html')

def filter_list(request,pk,value,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        if value == 'Todos':
            if pk == 'Etiqueta':
                filtro = 'tag'
            elif pk == 'Descricao':
                filtro = 'description'
            elif pk == 'EmPosse':
                filtro = 'tag'
            equipment = Equipment.objects.filter(inative=False).order_by('status',filtro)
            data = {}
            data['list_equipment'] = get_page(request,equipment)
            data['type_equipment']= EquipmentTypeAll()
            data['type'] = value
            data['search'] = 'Null'
            return render(request, templete_name, data)

        elif value == 'Inativos':
            if pk == 'Etiqueta':
                filtro = 'tag'
            elif pk == 'Descricao':
                filtro = 'description'
            elif pk == 'EmPosse':
                filtro = 'tag'
            equipment = Equipment.objects.filter(inative=True).order_by('status',filtro)
            data = {}
            data['list_equipment'] = get_page(request,equipment)
            data['type_equipment']= EquipmentTypeAll()
            data['type'] = value
            data['search'] = 'Null'
            return render(request, templete_name, data)
        else:
            if pk == 'Etiqueta':
                filtro = 'tag'
            elif pk == 'Descricao':
                filtro = 'description'
            elif pk == 'EmPosse':
                filtro = 'tag'
            equipment = Equipment.objects.filter(type_equipment = Equipment_type.objects.get(name = value),inative=False).order_by('status',filtro)
            data = {}
            data['list_equipment'] = get_page(request,equipment)
            data['type_equipment']= EquipmentTypeAll()
            data['type'] = value
            data['search'] = 'Null'
            return render(request, templete_name, data)
    return render(request, 'login.html')

def filter_type(request,value,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        equipment = Equipment.objects.filter(type_equipment = Equipment_type.objects.get(name = value),inative=False).order_by('status','tag')
        data = {}
        data['list_equipment'] = get_page(request,equipment)
        data['type_equipment']= EquipmentTypeAll()
        data['type'] = value
        data['search'] = 'Null'
        return render(request, templete_name, data)
    return render(request, 'login.html')

def search(request,value,search_):
    data = {}
    if request.session.has_key('username'):
        if request.method == 'POST':
            name = request.POST['search']
            data['search'] = name
            return redirect('/Pesquisar/'+value+'/'+name)
        else:
            name = search_
            data['search'] = name
        equipment = Equipment.objects.filter(Q(tag__contains=name) | Q(description__contains=name))
        data['list_equipment'] = get_page(request,equipment)
        data['type_equipment']= EquipmentTypeAll()
        data['type'] = 'Todos'
        return render(request, 'equipments/equipment_list.html', data)
            
    return render(request, 'login.html')
def search_page(request,name):
    equipment = Equipment.objects.filter(Q(tag__contains=name) | Q(description__contains=name))
    data = {}
    data['list_equipment'] = get_page(request,equipment)
    data['type_equipment']= EquipmentTypeAll()
    data['type'] = 'Todos'
    return render(request, 'equipments/equipment_list.html', data)
def search_type(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            name = request.POST['cemquipamento']
            data = {}
            data['object_list'] = Equipment_type.objects.filter(name__contains=name)
            return render(request, 'equipments/equipment_type_list.html', data)
    return render(request, 'login.html')

'''
class RastreioForm(forms.Form):
    data = {}
    tipo = Equipment_type.objects.all().values_list('name',flat=True)
    data['tipo']= tipo
    CHOICE = [('Todos','Todos')]
    
    for QuerySet in tipo:
        CHOICE.append((QuerySet,QuerySet))
    
    equipment = Equipment.objects.all().values_list('tag','description')
    CHOICE_EQUIPMENT = [('Todos','Todos')]
    for QuerySet in equipment:
        CHOICE_EQUIPMENT.append((QuerySet[0]+"-"+QuerySet[1],QuerySet[0]+"-"+QuerySet[1]))

    type_equipment = forms.ChoiceField(label='Tipo',choices=CHOICE)
    tag = forms.ChoiceField(label='Etiqueta-Descrição',choices=CHOICE_EQUIPMENT)
    #description = forms.CharField(label='Descrição', max_length=100)
    start = forms.DateTimeField(
        label='Start',
        widget=forms.widgets.DateTimeInput(attrs={'type':'date'}),
    )
    end = forms.DateTimeField(
        label='End',
        widget=forms.widgets.DateTimeInput(attrs={'type':'date'}),
    )
    '''
'''
def reports_list(request,templete_name='equipments/reports.html'):
    if request.session.has_key('username'):
        data = {}
        tipo = Equipment_type.objects.all().values_list('name',flat=True)
        CHOICE = [('Todos','Todos')]
        for QuerySet in tipo:
            CHOICE.append((QuerySet,QuerySet))
        equipment = Equipment.objects.all().values_list('tag','description')
        CHOICE_EQUIPMENT = [('Todos','Todos')]
        for QuerySet in equipment:
            CHOICE_EQUIPMENT.append((QuerySet[0]+"-"+QuerySet[1],QuerySet[0]+"-"+QuerySet[1]))

        data['types'] = CHOICE
        data['equipments'] = CHOICE_EQUIPMENT
        data['list_equipment_user_form']= form
        data['type'] = 'Todos'
        data['type_equipment_'] = 'Todos'
        data['tag_'] = 'Todos'
        data['start_'] = 'Todos'
        data['end_'] = 'Todos'
        
        return render(request, templete_name, data)
    return render(request, 'login.html')
'''


def get_rastreio(request,value):
    data = {}
    equipment = Equipment.objects.all()
    equipment_user = Equipment_user.objects.all()
    tipo = Equipment_type.objects.all().values_list('name',flat=True)
    CHOICE = []
    for QuerySet in tipo:
        CHOICE.append((QuerySet))
    equipment = Equipment.objects.all().values_list('tag','description')
    CHOICE_EQUIPMENT = []
    for QuerySet in equipment:
        CHOICE_EQUIPMENT.append((QuerySet[0]+"-"+QuerySet[1]))
    data['types'] = CHOICE
    data['equipments'] = CHOICE_EQUIPMENT
    data['type'] = value
    if value == 'Listagem' and request.method == 'POST':
        #return redirect('/Pesquisar/'+value+'/'+name)
        type_equipment = request.POST['type_equipment']
        return redirect('/Listagem/type_equipment/'+type_equipment)
        '''
        data['type_equipment_'] = type_equipment
        data['tag_'] = 'Todos'
        data['start_'] = 'Todos'
        data['end_'] = 'Todos'
        data['order_by'] = 'Nenhum'
        if type_equipment == 'Todos':
            equipment_user = Equipment.objects.all().order_by('type_equipment','tag')
            data['list_equipment_user']= get_page(request,equipment_user)
            data['type'] = value
        else:
            EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
            EquipmentType = ''.join(map(str, EquipmentType))
            EquipmentType = int(EquipmentType)
            equipment_user = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType))
            data['list_equipment_user']= get_page(request,equipment_user)
            data['type'] = value
        '''
    elif value == 'Rastreio' and request.method == 'POST':
        type_equipment = request.POST['type_equipment']
        tag = request.POST['tag']
        inicio = request.POST['start']
        fim = request.POST['end']
        tag_ = tag.split('-')
        tag_ = Equipment.objects.get(description__exact=tag_[1], tag__exact=tag_[0])
        #print(test.id)
        #tag_ = tag_[0]
        url= '/Rastreio/{}/{}/{}/{}/{}'.format('loan',type_equipment,tag_.id,inicio,fim)
        return redirect(url) 
        '''
        data = {}
        data['list_equipment_user']= get_page(request,Equipment_user.objects.all())
        data['type_equipment_'] = type_equipment
        data['tag_'] = tag_
        data['start_'] = inicio
        data['end_'] = fim
        data['order_by'] = 'Nenhum'
        if type_equipment == 'Todos' and tag=='Todos':
            equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim)
            data['list_equipment_user']= get_page(request,equipment_user)
            data['type'] = value
        elif type_equipment != 'Todos' and tag == 'Todos':
            EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
            EquipmentType = ''.join(map(str, EquipmentType))
            EquipmentType = int(EquipmentType)
            EquipmentFilter = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).values_list('id',flat=True)
            EquipmentFilter = ' '.join(map(str, EquipmentFilter))
            EquipmentFilter = EquipmentFilter.split()
            number = []
            for i in EquipmentFilter:
                number.append(int(i))
            equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim,equipment__in =  number)
            data['list_equipment_user']= get_page(request,equipment_user)
            data['type'] = value
        elif tag != 'Todos':
            EquipmentFilter = Equipment.objects.filter(tag = tag_).values_list('id',flat=True)
            EquipmentFilter = ' '.join(map(str, EquipmentFilter))
            equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim,equipment =  int(EquipmentFilter))
            data['list_equipment_user']= get_page(request,equipment_user)
            data['type'] = value
        '''
    elif value == 'Não Devolvidos'  and request.method == 'POST':
        type_equipment = request.POST['type_equipment']
        tag = request.POST['tag']
        inicio = request.POST['start']
        tag_ = tag.split('-')
        tag_ = tag_[0] 
        url= '/NaoDevolvidos/{}/{}/{}/{}'.format('loan',type_equipment,tag_,inicio)
        return redirect(url)
        '''
        data = {}
        data['type_equipment_'] = type_equipment
        data['tag_'] = tag_
        data['start_'] = inicio
        data['end_'] = 'Vazio'
        data['order_by'] = 'Nenhum'
        if type_equipment == 'Todos' and tag=='Todos':
            equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None)
            data['list_equipment_user']= get_page(request,equipment_user)
            data['type'] = value
        if type_equipment != 'Todos' and tag == 'Todos':
            EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
            EquipmentType = ''.join(map(str, EquipmentType))
            EquipmentType = int(EquipmentType)
            EquipmentFilter = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).values_list('id',flat=True)
            EquipmentFilter = ' '.join(map(str, EquipmentFilter))
            EquipmentFilter = EquipmentFilter.split()
            number = []
            for i in EquipmentFilter:
                number.append(int(i))
            equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None,equipment__in =  number)
            data['list_equipment_user']= get_page(request,equipment_user)
            data['type'] = value
        if tag != 'Todos':
            EquipmentFilter = Equipment.objects.filter(tag = tag_).values_list('id',flat=True)
            EquipmentFilter = ' '.join(map(str, EquipmentFilter))
            equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None,equipment =  int(EquipmentFilter))
            data['list_equipment_user']= get_page(request,equipment_user)
            data['type'] = value
        '''
    else:
        data['type_equipment_'] = 'Todos'
        data['list_equipment_user']= get_page(request,[])
        data['tag_'] = 'Todos'
        data['start_'] = 'Todos'
        data['end_'] = 'Todos'
        data['order_by'] = 'Vazio'  
    return render(request, 'equipments/reports.html', data)

def listagem(request,order_by,type_equipment_):
    data = {}
    tipo = Equipment_type.objects.all().values_list('name',flat=True)
    CHOICE = []
    for QuerySet in tipo:
        CHOICE.append((QuerySet))
    equipment = Equipment.objects.all().values_list('tag','description')
    CHOICE_EQUIPMENT = []
    for QuerySet in equipment:
        CHOICE_EQUIPMENT.append((QuerySet[0]+"-"+QuerySet[1]))
    data['types'] = CHOICE
    data['equipments'] = CHOICE_EQUIPMENT
    type_equipment = type_equipment_
    data['type_equipment_'] = type_equipment
    data['type'] = 'Listagem'
    data['type_equipment_'] = type_equipment
    data['tag_'] = 'Todos'
    data['start_'] = 'Todos'
    data['end_'] = 'Todos'
    data['order_by'] = order_by
    if type_equipment_ == 'Todos':
        equipment_user = Equipment.objects.all().order_by(order_by)
        data['list_equipment_user']= get_page(request,equipment_user)
        data['type'] = 'Listagem'
    else:
        EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
        EquipmentType = ''.join(map(str, EquipmentType))
        EquipmentType = int(EquipmentType)
        equipment_user = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).order_by(order_by)
        data['list_equipment_user']= get_page(request,equipment_user)
        data['type'] = 'Listagem'

    return render(request, 'equipments/reports.html', data)

def rastreio(request,order_by,type_equipment_,tag,start,end):
    data = {}
    print("aqui")
    tipo = Equipment_type.objects.all().values_list('name',flat=True)
    CHOICE = []
    for QuerySet in tipo:
        CHOICE.append((QuerySet))
    equipment = Equipment.objects.all().values_list('tag','description')
    CHOICE_EQUIPMENT = []
    for QuerySet in equipment:
        CHOICE_EQUIPMENT.append((QuerySet[0]+"-"+QuerySet[1]))
    data['types'] = CHOICE
    data['equipments'] = CHOICE_EQUIPMENT
    data['type'] = 'Rastreio'
    data['list_equipment_user']= get_page(request,Equipment_user.objects.all())
    data['type_equipment_'] = type_equipment_
    data['tag_'] = tag
    data['start_'] = start
    data['end_'] = end
    data['order_by'] = order_by
    type_equipment = type_equipment_
    inicio = start
    fim = end
    tag_ = tag
    if type_equipment == 'Todos' and tag=='Todos':
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim).order_by(order_by)
        data['list_equipment_user']= get_page(request,equipment_user)
        data['type'] = 'Rastreio'
    elif type_equipment != 'Todos' and tag == 'Todos':
        EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
        EquipmentType = ''.join(map(str, EquipmentType))
        EquipmentType = int(EquipmentType)
        EquipmentFilter = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).values_list('id',flat=True)
        EquipmentFilter = ' '.join(map(str, EquipmentFilter))
        EquipmentFilter = EquipmentFilter.split()
        number = []
        for i in EquipmentFilter:
            number.append(int(i))
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim,equipment__in =  number).order_by(order_by)
        data['list_equipment_user']= get_page(request,equipment_user)
        data['type'] = 'Rastreio'
    elif tag != 'Todos':
        EquipmentFilter = Equipment.objects.filter(id = tag_).values_list('id',flat=True)
        EquipmentFilter = ' '.join(map(str, EquipmentFilter))
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim,equipment =  int(EquipmentFilter)).order_by(order_by)
        data['list_equipment_user']= get_page(request,equipment_user)
        data['type'] = 'Rastreio'
    return render(request, 'equipments/reports.html', data)

def nao_devolvidos(request,order_by,type_equipment_,tag,start):
    data = {}
    tipo = Equipment_type.objects.all().values_list('name',flat=True)
    CHOICE = []
    for QuerySet in tipo:
        CHOICE.append((QuerySet))
    equipment = Equipment.objects.all().values_list('tag','description')
    CHOICE_EQUIPMENT = []
    for QuerySet in equipment:
        CHOICE_EQUIPMENT.append((QuerySet[0]+"-"+QuerySet[1]))
    data['types'] = CHOICE
    data['equipments'] = CHOICE_EQUIPMENT
    data['type'] = 'NaoDevolvidos'
    data['type_equipment_'] = type_equipment_
    data['tag_'] = tag
    data['start_'] = start
    data['end_'] = 'Todos'
    data['order_by'] = order_by
    type_equipment = type_equipment_
    inicio = start
    tag_ = tag
    if type_equipment_ == 'Todos' and tag=='Todos':
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None).order_by(order_by)
        data['list_equipment_user']= get_page(request,equipment_user)
    elif type_equipment_ != 'Todos' and tag == 'Todos':
        EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
        EquipmentType = ''.join(map(str, EquipmentType))
        EquipmentType = int(EquipmentType)
        EquipmentFilter = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).values_list('id',flat=True)
        EquipmentFilter = ' '.join(map(str, EquipmentFilter))
        EquipmentFilter = EquipmentFilter.split()
        number = []
        for i in EquipmentFilter:
            number.append(int(i))
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None,equipment__in =  number).order_by(order_by)
        data['list_equipment_user']= get_page(request,equipment_user)
    elif tag != 'Todos':
        EquipmentFilter = Equipment.objects.filter(tag = tag_).values_list('id',flat=True)
        EquipmentFilter = ' '.join(map(str, EquipmentFilter))
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None,equipment =  int(EquipmentFilter)).order_by(order_by)
        data['list_equipment_user']= get_page(request,equipment_user)
    return render(request, 'equipments/reports.html', data)


def page(list_complete,inicio,fim,report,type_equipment,tag,start,end):
    #tipo = 'listagem'
    #title = 'SISTEMA DE CONTROLE DE EQUIPAMENTO'
    #subtitle = 'Relatório de ' + tipo + ' de equipamento'
    #date_now = date.today()
    #time_now = datetime.now()
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')
    date = datetime.now()
    print(date.strftime("%H:%M"))
    #date = str(time_now.day)+'/'+str(time_now.month)+'/'+str(time_now.year)
    #time = str(time_now.hour)+':'+str(time_now.minute)


    picPath = 'equipments/static/images/download.png'
    
    picture = Image(picPath)
    picture.drawWidth = 150
    picture.drawHeight = 50
    picTable = Table([[picture]], 150, 50)
    description = 'Todos'
    if tag != 'Todos':
        #print('Aqui')
        description = Equipment.objects.filter(tag=tag)
        type_equipment = str(description[0].type_equipment)
        description = str(description[0].description)
        

    list01 = ["SISTEMA DE CONTROLE DE EQUIPAMENTOS"],["Relatório de "+ report +" de equipamento"],[""]
    list02 = ["Data: "+str(date.strftime("%d/%m/%Y"))],["Hora: "+str(date.strftime("%H:%M"))],["Página: " + str(inicio+1)  +" de " + str(fim)]
    list03 = ["Tipo: "+type_equipment,"Etiqueta: "+tag],["Descrição: "+description,""],["Inicial: "+start.strftime("%d/%m/%Y"),"Final: "+end.strftime("%d/%m/%Y")]

    Tablelist01 = Table(list01)
    Tablelist02 = Table(list02)
    Tablelist03 = Table(list03)

    style = TableStyle([
        ('ALIGN',(0,0),(-1,-1),'CENTER'),
    ])

    Tablelist01.setStyle(style)

    style2 = TableStyle([
        ('RIGHTPADDING',(0,0),(-1,-1),150),
    ])

    Tablelist03.setStyle(style2)

    refNoTable = Table([
            [picTable,Tablelist01, Tablelist02]
        ], [250, 350, 100])

    tableAll = Table(list_complete)

    style3 = TableStyle([
        ('RIGHTPADDING',(0,0),(-1,-1),25),
        #('BACKGROUND',(0,0),(8,0),colors.green),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('BOTTOMPADDING',(0,0),(-1,0),5),
        ('LINEABOVE',(0,1),(-1,1),0.5,colors.black),
    ])

    tableAll.setStyle(style3)

    rowNumb = len(list_complete)
    for i in range(1,rowNumb):
        if i % 2 == 0:
            bc = colors.palegreen
        else:
            bc = colors.white
        ts = TableStyle(
            [('BACKGROUND',(0,i),(-1,i),bc)]
        )
        tableAll.setStyle(ts)


    table = Table([
            [refNoTable],
            [Tablelist03],
            [tableAll]
        ])
    
    return table



def some_view(request,report,type_equipment,tag,start,end,order_by):
    def call_type_equipment(id):
        equipment = Equipment.objects.filter(id=id).values_list('type_equipment',flat=True)
        name_equipment = Equipment_type.objects.filter(id=equipment[0]).values_list('name',flat=True)
        return name_equipment[0]
            
    def call_tag_equipment(id):
        name_equipment = Equipment.objects.filter(id=id).values_list('tag',flat=True)
        return name_equipment[0]

    #from textwrap import wrap

    def call_description_equipment(id):
        name_equipment = Equipment.objects.filter(id=id).values_list('description',flat=True)
        #wraped_text = "-\n".join(wrap(name_equipment[0], 10))
        #print(wraped_text)
        return name_equipment[0]

    if report == 'Listagem':
        if order_by == 'Nenhum':
            if type_equipment == 'Todos':
                list_report = Equipment.objects.all().order_by('type_equipment','tag')
            else:
                list_report = Equipment.objects.filter(type_equipment = Equipment_type.objects.get(name=type_equipment))
        else:
            if type_equipment == 'Todos':
                list_report = Equipment.objects.all().order_by(order_by)
            else:
                list_report = Equipment.objects.filter(type_equipment = Equipment_type.objects.get(name=type_equipment)).order_by(order_by)

        list_complete = []
        for equipment in list_report:
            list_temp = [equipment.type_equipment.name,equipment.tag,equipment.description,'','','','',equipment.amount_of_loans]
            list_complete.append(list_temp)

    elif report == 'Rastreio':
        if order_by == 'Nenhum':
            if type_equipment == 'Todos' and tag =='Todos':
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution__lte=end)
            elif type_equipment != 'Todos' and tag == 'Todos':
                EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
                EquipmentType = ''.join(map(str, EquipmentType))
                EquipmentType = int(EquipmentType)
                EquipmentFilter = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                EquipmentFilter = EquipmentFilter.split()
                number = []
                for i in EquipmentFilter:
                    number.append(int(i))
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution__lte=end,equipment__in =  number)
            elif tag != 'Todos':
                EquipmentFilter = Equipment.objects.filter(tag = tag).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution__lte=end,equipment =  int(EquipmentFilter))
        else:
            report = 'Não Devolvidos'
            if type_equipment == 'Todos' and tag=='Todos':
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution__lte=end).order_by(order_by)
            elif type_equipment != 'Todos' and tag == 'Todos':
                #print('cheguei')
                EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
                EquipmentType = ''.join(map(str, EquipmentType))
                EquipmentType = int(EquipmentType)
                EquipmentFilter = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                EquipmentFilter = EquipmentFilter.split()
                number = []
                for i in EquipmentFilter:
                    number.append(int(i))
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution__lte=end,equipment__in =  number).order_by(order_by)
            elif tag != 'Todos':
                EquipmentFilter = Equipment.objects.filter(tag = tag).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution__lte=end,equipment =  int(EquipmentFilter)).order_by(order_by)

        list_complete = []
        for equipment in list_report:
            list_temp = [call_type_equipment(equipment.equipment),call_tag_equipment(equipment.equipment),call_description_equipment(equipment.equipment),equipment.loan.strftime("%d/%m/%Y às %H:%M"),str(equipment.user_loan),equipment.devolution.strftime("%d/%m/%Y às %H:%M"),str(equipment.user_devolution),equipment.amount_of_loans]
            list_complete.append(list_temp)
    else:
        if order_by == 'Nenhum':
            if type_equipment == 'Todos' and tag=='Todos':
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution=None)
            elif type_equipment != 'Todos' and tag == 'Todos':
                EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
                EquipmentType = ''.join(map(str, EquipmentType))
                EquipmentType = int(EquipmentType)
                EquipmentFilter = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                EquipmentFilter = EquipmentFilter.split()
                number = []
                for i in EquipmentFilter:
                    number.append(int(i))
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution=None,equipment__in =  number)
            elif tag != 'Todos':
                EquipmentFilter = Equipment.objects.filter(tag = tag).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution=None,equipment =  int(EquipmentFilter))
        else:
            if type_equipment == 'Todos' and tag=='Todos':
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution=None).order_by(order_by)
            elif type_equipment != 'Todos' and tag == 'Todos':
                EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
                EquipmentType = ''.join(map(str, EquipmentType))
                EquipmentType = int(EquipmentType)
                EquipmentFilter = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                EquipmentFilter = EquipmentFilter.split()
                number = []
                for i in EquipmentFilter:
                    number.append(int(i))
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution=None,equipment__in =  number).order_by(order_by)
            elif tag != 'Todos':
                EquipmentFilter = Equipment.objects.filter(tag = tag).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                list_report = Equipment_user.objects.filter(loan__gte=start,devolution=None,equipment =  int(EquipmentFilter)).order_by(order_by)

        list_complete = []
        for equipment in list_report:
            list_temp = [call_type_equipment(equipment.equipment),call_tag_equipment(equipment.equipment),call_description_equipment(equipment.equipment),equipment.loan.strftime("%d/%m/%Y às %H:%M"),str(equipment.user_loan),equipment.devolution.strftime("%d/%m/%Y às %H:%M"),str(equipment.user_devolution),equipment.amount_of_loans]
            list_complete.append(list_temp)



    #list_report = Equipment_user.objects.all()
    list_title = ["Tipo","Etiqueta","Descrição","Solicitação","Responsável","Devolução","Responsável","Qtd. Empr."]
    
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer,pagesize=landscape(A4),rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
    elems = []

    numberPage = int(len(list_complete)/20)
    numberPage = numberPage  + 1
    if numberPage >= 1:    
        for i in range(0,numberPage):
            list_ = []
            list_.append(list_title)
            list_ = list_ + list_complete[i*20:(i+1)*20]
            table = page(list_,i,numberPage,report,type_equipment,tag,start,end)
            elems.append(table)
    else:
        table = page(list_complete)
        elems.append(table)
   
    pdf.build(elems)
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reports.pdf')