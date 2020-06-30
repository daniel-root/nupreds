from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from equipments.models import *
from equipments.APIs import *
from datetime import datetime, timedelta
from users.models import *
from django.db.models import Q
from django.utils import timezone
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages
from users.views import main
 
def home(request):
    if request.session.has_key('username'):
        TelegramCadastro()
        return render(request,'home.html')
    return render(request,'login.html')

class TypeForm(ModelForm):
    class Meta:
        model = Equipment_type
        fields = ['name','time_maximum']

class InactiveForm(forms.Form):
    inactive = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onclick':'this.form.submit();'}),required=False, label="Ver inativos")

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['tag','description','type_equipment','maximum_time']

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
    form = TypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, template_name, {'form':form})

def equipment_type_update(request, pk, template_name='equipments/equipment_type_form.html'):
    form = TypeForm(request.POST or None, instance=EquipmentTypeUnique(pk))
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, template_name, {'form':form})

def equipment_type_delete(request, pk, template_name='equipments/equipment_type_confirm_delete.html'):
    if request.session.has_key('username'):
        if request.method=='POST': 
            if Equipment_type.objects.filter(id = pk,inative='True'):
                Equipment_type.objects.filter(id = pk).update(inative='False')
            else:
                Equipment_type.objects.filter(id = pk).update(inative='True')
            return equipment_list(request)
        return render(request, template_name, {'object':EquipmentTypeUnique(pk)})
    return render(request, 'login.html')

def EquipmentActiveAll():
    equipment = Equipment.objects.filter(inative=False).order_by('status','tag')
    return equipment

def EquipmentAll():
    equipment = Equipment.objects.filter(inative=True).order_by('status','tag')
    return equipment

def EquipmentUnique(pk):
    equipment = get_object_or_404(Equipment, pk=pk)
    return equipment

def equipment_list(request,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        data = {}
        data['list_equipment'] = EquipmentActiveAll()
        data['type_equipment']= EquipmentTypeAll()
        data['form_inactive'] = InactiveForm()
        data['type'] = 'Todos'
        for i in range(0,len(data['list_equipment'])):
            Atraso(data['list_equipment'][i].id)
        return render(request, templete_name, data)
    return render(request, 'login.html')

def equipment_list_inactive(request,value,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        data = {}
        data['list_equipment'] = EquipmentAll()
        data['type_equipment']= EquipmentTypeAll()
        data['form_inactive'] = InactiveForm()
        data['type'] = value

        return render(request, templete_name, data)
    return render(request, 'login.html')

def equipment_view(request, pk, template_name='equipments/equipment_detail.html'):
    if request.session.has_key('username'):
        return render(request, template_name, {'object':EquipmentUnique(pk)})
    return render(request, 'login.html')

def equipment_create(request, template_name='equipments/equipment_form.html'):
    if request.session.has_key('username'):
        form = EquipmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
        return render(request, template_name, {'form':form})
    return render(request, 'login.html')

def equipment_update(request, pk, template_name='equipments/equipment_form1.html'):
    if request.session.has_key('username'):
        form = EquipmentForm(request.POST or None, instance=EquipmentUnique(pk))
        if form.is_valid():
            form.save()
            return equipment_list(request)
        return render(request, template_name, {'form':form})
    return render(request, 'login.html')

def equipment_delete(request, pk, template_name='equipments/equipment_confirm_delete.html'):
    if request.session.has_key('username'):
        if request.method=='POST': 
            if Equipment.objects.filter(id = pk,inative='True'):
                Equipment.objects.filter(id = pk).update(inative='False')
            else:
                Equipment.objects.filter(id = pk).update(inative='True')
            return equipment_list(request)
        return render(request, template_name, {'object':EquipmentUnique(pk)})
    return render(request, 'login.html')
count = 0
def emprestar(request,pk):
    global count
    #print(count)
    if request.session.has_key('username'):
        username = None
        if count >= 5:
            count = 0
            data = {}
            data['chave'] = EquipmentUnique(pk)
            data['tipo'] = 'por senha'
            return render(request, 'equipments/emprestar.html', data )
        if request.method=='POST':
            username = main("Verification")
        #print(username)
        if username != "Erro ao selecionar dispositivo.":
            post = Client.objects.filter(usuario=username).values_list('id',flat=True)
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
                return equipment_list(request)
            else:
                messages.error(request, 'Usuario não encontrado!')
                count = count + 1
                print(count)
                return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
            return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
                    
        else:
            data = {}
            data['chave'] = EquipmentUnique(pk)
            data['tipo'] = 'por senha'
            return render(request, 'equipments/emprestar.html', data )

        #return render(request, 'equipments/emprestar.html', data )
    return render(request, 'login.html')

def devolver(request,pk):
    global count
    #print(count)
    if request.session.has_key('username'):
        username = None
        if count >= 5:
            count = 0
            data = {}
            data['chave'] = pk
            #data['tipo'] = 'por senha'
            return render(request, 'equipments/devolver.html', data )
        username = None
        if request.method=='POST':
            username = main("Verification")
        #print("usuario ",username)
        if username != "Erro ao selecionar dispositivo.":
            post = Client.objects.filter(usuario=username).values_list('id',flat=True)
            #print(post)
            if post:
            #StringPost = ''.join(map(str, post))
                BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk))
                if BusyEquipment:
                    Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = pk)).update(user_devolution=Client.objects.get(id = int(post[0])),devolution=timezone.now())
                    Equipment.objects.filter(id = pk).update(status='Livre')
                    return equipment_list(request)
                else:
                    messages.error(request, 'Equipamento sem emprestimo!')
                    return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
            else:
                count = count + 1
                print(count)
                messages.error(request, 'Usuario não encontrado!')
                return render(request, 'equipments/equipment_detail.html', {'object':EquipmentUnique(pk)})
            return render(request, 'equipments/devolver.html',data)
        else:
            data = {}
            data['chave'] = pk
            #data['tipo'] = 'por senha'
            return render(request, 'equipments/devolver.html', data )

        #print(username)
        post = Client.objects.filter(usuario=username).values_list('id',flat=True)
        
    return render(request, 'login.html')

def emprestar_user(request,pk):
    if request.session.has_key('username'):
        if request.method == 'POST':
            
            username = request.POST['username']
            #print(username)
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
                return equipment_list(request)
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
                    return equipment_list(request)
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
            data['list_equipment'] = equipment
            data['type_equipment']= EquipmentTypeAll()
            data['form_inactive'] = InactiveForm()
            data['type'] = value
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
            data['list_equipment'] = equipment
            data['type_equipment']= EquipmentTypeAll()
            data['form_inactive'] = InactiveForm()
            data['type'] = value
            return render(request, templete_name, data)
    return render(request, 'login.html')

def filter_type(request,value,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        equipment = Equipment.objects.filter(type_equipment = Equipment_type.objects.get(name = value),inative=False).order_by('status','tag')
        data = {}
        data['list_equipment'] = equipment
        data['type_equipment']= EquipmentTypeAll()
        data['form_inactive'] = InactiveForm()
        data['type'] = value
        return render(request, templete_name, data)
    return render(request, 'login.html')

def search(request,value):
    if request.session.has_key('username'):
        if request.method == 'POST':
            name = request.POST['search']
            equipment = Equipment.objects.filter(Q(tag__contains=name) | Q(description__contains=name))
            data = {}
            data['list_equipment'] = equipment
            data['type_equipment']= EquipmentTypeAll()
            data['form_inactive'] = InactiveForm()
            data['type'] = value
            return render(request, 'equipments/equipment_list.html', data)
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
    if request.method == 'POST':
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

        if value == 'Listagem':
            type_equipment = request.POST['type_equipment']
            data['type_equipment_'] = type_equipment
            data['tag_'] = 'Todos'
            data['start_'] = 'Todos'
            data['end_'] = 'Todos'
            if type_equipment == 'Todos':
                equipment_user = Equipment.objects.all().order_by('type_equipment','tag')
                data['list_equipment_user']= equipment_user
                data['type'] = value
            else:
                EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
                EquipmentType = ''.join(map(str, EquipmentType))
                EquipmentType = int(EquipmentType)
                equipment_user = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType))
                data['list_equipment_user']= equipment_user
                data['type'] = value
        elif value == 'Rastreio':
            type_equipment = request.POST['type_equipment']
            tag = request.POST['tag']
            inicio = request.POST['start']
            fim = request.POST['end']
            tag_ = tag.split('-')
            tag_ = tag_[0] 
            data = {}
            data['type_equipment_'] = type_equipment
            data['tag_'] = tag_
            data['start_'] = inicio
            data['end_'] = fim
            if type_equipment == 'Todos' and tag=='Todos':
                equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim)
                data['list_equipment_user']= equipment_user
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
                data['list_equipment_user']= equipment_user
                data['type'] = value
            elif tag != 'Todos':
                EquipmentFilter = Equipment.objects.filter(tag = tag_).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim,equipment =  int(EquipmentFilter))
                data['list_equipment_user']= equipment_user
                data['type'] = value
        elif value == 'NaoDevolvidos':
            type_equipment = request.POST['type_equipment']
            tag = request.POST['tag']
            inicio = request.POST['start']
            tag_ = tag.split('-')
            tag_ = tag_[0] 
            data = {}
            data['type_equipment_'] = type_equipment
            data['tag_'] = tag_
            data['start_'] = inicio
            if type_equipment == 'Todos' and tag=='Todos':
                equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None)
                data['list_equipment_user']= equipment_user
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
                equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None,equipment__in =  number)
                data['list_equipment_user']= equipment_user
                data['type'] = value
            elif tag != 'Todos':
                EquipmentFilter = Equipment.objects.filter(tag = tag_).values_list('id',flat=True)
                EquipmentFilter = ' '.join(map(str, EquipmentFilter))
                equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None,equipment =  int(EquipmentFilter))
                data['list_equipment_user']= equipment_user
                data['type'] = value
        return render(request, 'equipments/reports.html', data)
    else:
        equipment = Equipment.objects.all()
        equipment_user = Equipment_user.objects.all()
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
        data['type'] = value
        data['type_equipment_'] = 'Todos'
        data['tag_'] = 'Todos'
        data['start_'] = 'Todos'
        data['end_'] = 'Todos'
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
    if type_equipment_ == 'Todos':
        equipment_user = Equipment.objects.all().order_by(order_by)
        data['list_equipment_user']= equipment_user
        data['type'] = 'Listagem'
    else:
        EquipmentType = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
        EquipmentType = ''.join(map(str, EquipmentType))
        EquipmentType = int(EquipmentType)
        equipment_user = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = EquipmentType)).order_by(order_by)
        data['list_equipment_user']= equipment_user
        data['type'] = 'Listagem'

    return render(request, 'equipments/reports.html', data)

def rastreio(request,order_by,type_equipment_,tag,start,end):
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
    data['type'] = 'Rastreio'
    data['type_equipment_'] = type_equipment_
    data['tag_'] = tag
    data['start_'] = start
    data['end_'] = end
    type_equipment = type_equipment_
    inicio = start
    fim = end
    tag_ = tag
    if type_equipment == 'Todos' and tag=='Todos':
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim).order_by(order_by)
        data['list_equipment_user']= equipment_user
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
        data['list_equipment_user']= equipment_user
        data['type'] = 'Rastreio'
    elif tag != 'Todos':
        EquipmentFilter = Equipment.objects.filter(tag = tag_).values_list('id',flat=True)
        EquipmentFilter = ' '.join(map(str, EquipmentFilter))
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim,equipment =  int(EquipmentFilter)).order_by(order_by)
        data['list_equipment_user']= equipment_user
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
    type_equipment = type_equipment_
    inicio = start
    tag_ = tag
    if type_equipment_ == 'Todos' and tag=='Todos':
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None).order_by(order_by)
        data['list_equipment_user']= equipment_user
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
        data['list_equipment_user']= equipment_user
    elif tag != 'Todos':
        EquipmentFilter = Equipment.objects.filter(tag = tag_).values_list('id',flat=True)
        EquipmentFilter = ' '.join(map(str, EquipmentFilter))
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution=None,equipment =  int(EquipmentFilter)).order_by(order_by)
        data['list_equipment_user']= equipment_user
    return render(request, 'equipments/reports.html', data)

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def some_view(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 750, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='reports.pdf')