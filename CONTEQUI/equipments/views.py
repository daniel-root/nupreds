from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from equipments.models import *
from datetime import datetime, timedelta
from users.models import *
from django.db.models import Q
from django.utils import timezone
from django import forms
from django.http import HttpResponseRedirect
from django.contrib import messages


def CheckLoggedUser(request):
    if request.session.has_key('username') == False:
        return False
    return True

def home(request):
    if CheckLoggedUser(request):
        return render(request,'home.html')
    return render(request,'login.html')

class TypeForm(ModelForm):
    class Meta:
        model = Equipment_type
        fields = ['name']

class InactiveForm(forms.Form):
    #search_keyword = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Keyword Search','class':'keyword-search'}))
    inactive = forms.BooleanField(widget=forms.CheckboxInput(attrs={'onclick':'this.form.submit();'}),required=False, label="Ver inativos")

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['tag','description','type_equipment','maximum_time']

def equipment_type_list(request, templete_name='equipments/equipment_type_list.html'):
    equipment_type = Equipment_type.objects.all()
    data = {}
    data['object_list'] = equipment_type
    return render(request, templete_name, data)

def equipment_type_view(request, pk, template_name='equipments/equipment_type_detail.html'):
    equipment_type= get_object_or_404(Equipment_type, pk=pk)    
    return render(request, template_name, {'object':equipment_type})

def equipment_type_create(request, template_name='equipments/equipment_type_form.html'):
    form = TypeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, template_name, {'form':form})

def equipment_type_update(request, pk, template_name='equipments/equipment_type_form.html'):
    equipment_type= get_object_or_404(Equipment_type, pk=pk)
    form = TypeForm(request.POST or None, instance=equipment_type)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, template_name, {'form':form})

def equipment_type_delete(request, pk, template_name='equipments/equipment_type_confirm_delete.html'):
    equipment_type= get_object_or_404(Equipment_type, pk=pk)    
    if request.method=='POST':
        equipment_type.delete()
        return redirect('equipment_list')
    return render(request, template_name, {'object':equipment_type})

class tipos():
    a = 1
    b = 2
    c = 3


def equipment_list(request,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        equipment = Equipment.objects.filter(inative=False).order_by('status','tag')
        type_equipment = Equipment_type.objects.all().values_list('name',flat=True)
        #tipos={['a',1],['b',2],['c',3]}
        # {'object':equipment}
        #print(equipment)
        data = {}
        data['list_equipment'] = equipment
        data['type_equipment']= type_equipment
        data['form_inactive'] = InactiveForm()
        data['type_filter'] = tipos()
        return render(request, templete_name, data)
    return render(request, 'login.html')

def equipment_list_inactive(request,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        equipment = Equipment.objects.all().order_by('status','tag')
        type_equipment = Equipment_type.objects.all().values_list('name',flat=True)
        data = {}
        data['list_equipment'] = equipment
        data['type_equipment']= type_equipment
        data['form_inactive'] = InactiveForm()
        data['type_filter'] = tipos()
        return render(request, templete_name, data)
    return render(request, 'login.html')

def equipment_view(request, pk, template_name='equipments/equipment_detail.html'):
    if request.session.has_key('username'):
        equipment = get_object_or_404(Equipment, pk=pk)   
        #print(equipment) 
        return render(request, template_name, {'object':equipment})
    return render(request, 'login.html')

def equipment_create(request, template_name='equipments/equipment_form.html'):
    if request.session.has_key('username'):
        form = EquipmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
        return render(request, template_name, {'form':form})
    return render(request, 'login.html')

def equipment_update(request, pk, template_name='equipments/equipment_form.html'):
    if request.session.has_key('username'):
        equipment= get_object_or_404(Equipment, pk=pk)
        form = EquipmentForm(request.POST or None, instance=equipment)
        if form.is_valid():
            form.save()
            return equipment_list(request)
        return render(request, template_name, {'form':form})
    return render(request, 'login.html')

def equipment_delete(request, pk, template_name='equipments/equipment_confirm_delete.html'):
    if request.session.has_key('username'):
        equipment= get_object_or_404(Equipment, pk=pk)   
        if request.method=='POST':
            if Equipment.objects.filter(id = pk,inative='True'):
                Equipment.objects.filter(id = pk).update(inative='False')
            else:
                Equipment.objects.filter(id = pk).update(inative='True')
            return equipment_list(request)
        return render(request, template_name, {'object':equipment})
    return render(request, 'login.html')

def emprestar(request,pk):
    if request.session.has_key('username'):
        chave = pk
        return render(request, 'equipments/emprestar.html', {'chave': chave })
    return render(request, 'login.html')

def devolver(request,pk):
    if request.session.has_key('username'):
        chave = pk
        return render(request, 'equipments/devolver.html', {'chave': chave })
    return render(request, 'login.html')

def emprestar_user(request,pk):
    if request.session.has_key('username'):
        if request.method == 'POST':
            username = request.POST['username']
            password =  request.POST['password']
            post = Client.objects.filter(usuario=username,senha=password).values_list('id',flat=True)
            if post:
                StringPost = ''.join(map(str, post))
                chave = int(pk)
                BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = chave))
                amout = Equipment.objects.filter(id=chave).values_list('amount_of_loans',flat=True)
                amout_of_equipments = ''.join(map(str, amout))
                if BusyEquipment:
                    messages.error(request, 'Equipamento já emprestado!')
                    equipment= get_object_or_404(Equipment, pk=pk)
                    return render(request, 'equipments/equipment_detail.html', {'object':equipment})
                time = Equipment.objects.filter(id = chave).values_list('maximum_time',flat=True)
                time = ''.join(map(str,time))
                Equipment.objects.filter(id = chave).update(status='Ocupado',amount_of_loans=(int(amout_of_equipments)+1))
                Equipment_user.objects.create(loan=timezone.now(),devolution=None,equipment=Equipment.objects.get(id = chave),user_loan=Client.objects.get(id = int(StringPost)),amount_of_loans=int(amout_of_equipments)+1,limit_time=datetime.now()+timedelta(minutes=int(time)))
                return equipment_list(request)
        equipment= get_object_or_404(Equipment, pk=pk)
        return render(request, 'equipments/equipment_detail.html', {'object':equipment})
    return render(request, 'login.html')

def devolver_user(request,pk):
    if request.session.has_key('username'):
        if request.method == 'POST':
            username = request.POST['username']
            password =  request.POST['password']
            post = Client.objects.filter(usuario=username,senha=password).values_list('id',flat=True)
            if post:
                StringPost = ''.join(map(str, post))
                chave = int(pk)
                BusyEquipment = Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = chave))
                if BusyEquipment:
                    Equipment_user.objects.filter(devolution=None,equipment=Equipment.objects.get(id = chave)).update(user_devolution=Client.objects.get(id = int(StringPost)),devolution=timezone.now())
                    Equipment.objects.filter(id = chave).update(status='Livre')
                    return equipment_list(request)
            messages.error(request, 'Equipamento sem emprestimo!')
            equipment= get_object_or_404(Equipment, pk=pk)
            return render(request, 'equipments/equipment_detail.html', {'object':equipment})
        equipment= get_object_or_404(Equipment, pk=pk)
        return render(request, 'equipments/equipment_detail.html', {'object':equipment})
    return render(request, 'login.html')

def filter_list(request,pk,templete_name='equipments/equipment_list.html'):
    pk = pk
    if request.session.has_key('username'):
        if pk == 1:
            filtro = 'tag'
        elif pk == 2:
            filtro = 'description'
        elif pk == 3:
            filtro = 'tag'
        equipment = Equipment.objects.all().order_by('status',filtro)
        tipo = Equipment_type.objects.all().values_list('name',flat=True)
        data = {}
        data['list_equipment'] = equipment
        data['type_equipment']= tipo
        data['type_filter'] = tipos()
        return render(request, templete_name, data)
    return render(request, 'login.html')

def filter_type(request,value,templete_name='equipments/equipment_list.html'):
    pk = value
    if request.session.has_key('username'):
        filtro = pk
        equipment = Equipment.objects.filter(type_equipment = Equipment_type.objects.get(name = filtro)).order_by('status','tag')
        tipo = Equipment_type.objects.all().values_list('name',flat=True)
        data = {}
        data['list_equipment'] = equipment
        data['type_equipment']= tipo
        data['type_filter'] = tipos()
        return render(request, templete_name, data)
    return render(request, 'login.html')

def search(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            name = request.POST['search']
            equipment = Equipment.objects.filter(Q(tag__contains=name) | Q(description__contains=name))
            tipo = Equipment_type.objects.all().values_list('name',flat=True)
            data = {}
            data['list_equipment'] = equipment
            data['type_equipment']= tipo
            data['type_filter'] = tipos()
            return render(request, 'equipments/equipment_list.html', data)
    return render(request, 'login.html')

def reports_list(request,templete_name='equipments/reports.html'):
    if request.session.has_key('username'):
        equipment = Equipment.objects.all()
        equipment_user = Equipment_user.objects.all()
        data = {}
        data['list_equipment_user']= equipment_user
        return render(request, templete_name, data)
    return render(request, 'login.html')


class RastreioForm(forms.Form):
    data = {}
    tipo = Equipment_type.objects.all().values_list('name',flat=True)
    data['tipo']= tipo
    CHOICE = [('Todos','Todos')]
    
    for QuerySet in tipo:
        CHOICE.append((QuerySet,QuerySet))
    
    type_equipment = forms.ChoiceField(label='Tipo',choices=CHOICE)
    tag = forms.CharField(label='Etiqueta', max_length=100)
    description = forms.CharField(label='Descrição', max_length=100)
    start = forms.DateTimeField(
        label='Start',
        widget=forms.widgets.DateTimeInput(attrs={'type':'date'}),
    )
    end = forms.DateTimeField(
        label='End',
        widget=forms.widgets.DateTimeInput(attrs={'type':'date'}),
    )

def get_rastreio(request):
    if request.method == 'POST':
        form = RastreioForm(request.POST)
        type_equipment = request.POST['type_equipment']
        tag = request.POST['tag']
        description = request.POST['description']
        inicio = request.POST['inicio']
        fim = request.POST['fim']
        equipment = Equipment.objects.all()
        
        #teste = Equipment_type.objects.filter(name=type_equipment).values_list('id',flat=True)
        #a = ''.join(map(str, teste))
        #print(a)
        #a = int(a)
        #teste1 = Equipment.objects.filter(type_equipment=Equipment_type.objects.get(id = a)).values_list('id',flat=True)
        #b = ' '.join(map(str, teste1))
        #b = b.split()
        #get_object_or_404(Equipment, pk=pk)
        #print(b)    
        #chave = int(b)
        equipment_user = Equipment_user.objects.filter(loan__gte=inicio,devolution__lte=fim)
        #number = []
        #for i in b:
        #    number.append(int(i))
        #print(number)
        #equipment_user = Equipment_user.objects.filter(equiment=Equipment.objects.get(type_equipment = a))
        #equipment_user = Equipment_user.objects.filter(equiment__in =  number)
        #print(equipment_user)
    #print(tipo)
        data = {}
        data['list_equipment_user']= equipment_user
        data['list_equipment_user_form']= form
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
            return render(request, 'equipments/reports.html', data)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RastreioForm()
        equipment = Equipment.objects.all()
        equipment_user = Equipment_user.objects.all()
    #print(tipo)
        data = {}
        data['list0'] = equipment
        data['list1']= equipment_user
        data['list2']= form

    return render(request, 'equipments/reports.html', data)

class RastreioListForm(forms.Form):
    type_equipment = forms.CharField(label='Tipo', max_length=100)
    tag = forms.CharField(label='Etiqueta', max_length=100)
    description = forms.CharField(label='Descrição', max_length=100)
    #inicio = forms.DateTimeField(label='Intervalo Inicial')
    #fim = forms.DateTimeField(label='Intervalo Final')

def get_rastreio_list(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RastreioListForm(request.POST)
        equipment = Equipment.objects.all()
        equipment_user = Equipment_user.objects.all().order_by(loan)
    #print(tipo)
        data = {}
        data['list0'] = equipment
        data['list1']= equipment_user
        data['list2']= form
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
            return render(request, 'equipments/reports_user.html', data)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RastreioListForm()
        equipment = Equipment.objects.all()
        equipment_user = Equipment_user.objects.all()
    #print(tipo)
        data = {}
        data['list0'] = equipment
        data['list1']= equipment_user
        data['list2']= form

    return render(request, 'equipments/reports_user.html', data)

class RastreioList2Form(forms.Form):
    type_equipment = forms.CharField(label='Tipo', max_length=100)
    tag = forms.CharField(label='Etiqueta', max_length=100)
    description = forms.CharField(label='Descrição', max_length=100)
    inicio = forms.DateTimeField(label='Intervalo Inicial')
    fim = forms.DateTimeField(label='Intervalo Final')

def get_rastreio_list2(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RastreioList2Form(request.POST)
        equipment = Equipment.objects.all()
        equipment_user = Equipment_user.objects.filter(devolution=None).order_by(loan)
    #print(tipo)
        data = {}
        data['list0'] = equipment
        data['list1']= equipment_user
        data['list2']= form
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')
            return render(request, 'equipments/reports_devolvidos.html', data)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RastreioList2Form()
        equipment = Equipment.objects.all()
        equipment_user = Equipment_user.objects.filter(devolution=None)
    #print(tipo)
        data = {}
        data['list0'] = equipment
        data['list1']= equipment_user
        data['list2']= form

    return render(request, 'equipments/reports_devolvidos.html', data)