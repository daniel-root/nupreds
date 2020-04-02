from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from equipments.models import *
from datetime import datetime
from users.models import *
from django.db.models import Q
from django.utils import timezone
import signal
from django import forms
from django.http import HttpResponseRedirect

#todas as funções fazem o teste para validação de úsuario, caso não esteja validado, retorna a função login.

#redireciona para página inicial do conequi.
def home(request):
    if request.session.has_key('username'):
        return render(request, 'home.html')
    return render(request, 'login.html')

#classe para criação do formulario com base no modelo.
class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['tag','description','type_equipment','maximum_time']

#redireciona para página de equipamentos.
def equipment_list(request,templete_name='equipments/equipment_list.html'):
    if request.session.has_key('username'):
        equipment = Equipment.objects.all().order_by('status','tag') #pega todos os itens de Equipment e ordena por Status e Tag
        tipo = Equipment_type.objects.all().values_list('name',flat=True) #pega todos os tipos.
        data = {} #biblioteca para colocar os itens do banco de dados.
        data['object_list'] = equipment
        data['tipo']= tipo
        return render(request, templete_name, data)
    return render(request, 'login.html')


#mostrar item.
def equipment_view(request, pk, template_name='equipments/equipment_detail.html'):
    if request.session.has_key('username'):
        equipment= get_object_or_404(Equipment, pk=pk)    
        return render(request, template_name, {'object':equipment})
    return render(request, 'login.html')

#criar novo item
def equipment_create(request, template_name='equipments/equipment_form.html'):
    if request.session.has_key('username'):
        form = EquipmentForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('equipment_list')
        return render(request, template_name, {'form':form})
    return render(request, 'login.html')

#atualiza item
def equipment_update(request, pk, template_name='equipments/equipment_form.html'):
    if request.session.has_key('username'):
        equipment= get_object_or_404(Equipment, pk=pk)
        form = EquipmentForm(request.POST or None, instance=equipment)
        if form.is_valid():
            form.save()
            return equipment_list(request)
        return render(request, template_name, {'form':form})
    return render(request, 'login.html')

#deleta item
def equipment_delete(request, pk, template_name='equipments/equipment_confirm_delete.html'):
    if request.session.has_key('username'):
        equipment= get_object_or_404(Equipment, pk=pk)    
        if request.method=='POST':
            equipment.delete()
            return equipment_list(request)
        return render(request, template_name, {'object':equipment})
    return render(request, 'login.html')

#redirecionar para função emprestar
def emprestar(request,pk):
    if request.session.has_key('username'):
        chave = pk
        return render(request, 'equipments/emprestar.html', {'chave': chave })
    return render(request, 'login.html')

#redirecionar para função devolver
def devolver(request,pk):
    if request.session.has_key('username'):
        chave = pk
        return render(request, 'equipments/devolver.html', {'chave': chave })
    return render(request, 'login.html')

#função emprestar
def emprestar_user(request,pk):
    if request.session.has_key('username'):
        if request.method == 'POST':
            username = request.POST['username']
            password =  request.POST['password']
            post = Client.objects.filter(usuario=username,senha=password).values_list('id',flat=True) #conferir nome e senha do usuario
            if post: #continua se combinar usuario e senha.
                a = ''.join(map(str, post)) #converte QuerySet para String
                chave = int(pk) #converte string para inteiro
                teste = Equipment_user.objects.filter(devolution=None,equiment=Equipment.objects.get(id = chave)) #pega Equipment_user com a chave:
                amout = Equipment.objects.filter(id=chave).values_list('amount_of_loans',flat=True) #pega contagem de emprestimos
                amout_of_equipments = ''.join(map(str, amout)) #converte para string
                if teste: #equipamento estiver emprestado retorna.
                    equipment= get_object_or_404(Equipment, pk=pk) #pega equipamento 
                    return render(request, 'equipments/equipment_detail.html', {'object':equipment}) #retorna
                Equipment.objects.filter(id = chave).update(status='Ocupado',amount_of_loans=(int(amout_of_equipments)+1))#adicona mais 1 na contagem de emprestimos.
                Equipment_user.objects.create(loan=timezone.now(),devolution=None,equiment=Equipment.objects.get(id = chave),usuario=Client.objects.get(id = a),amount_of_loans=int(amout_of_equipments)+1)#cria novo Equipment_user.
                return equipment_list(request) #retorna
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
                a = ''.join(map(str, post))
                chave = int(pk)
                teste = Equipment_user.objects.filter(devolution=None,equiment=Equipment.objects.get(id = chave))
                #amout = Equipment.objects.filter(id=chave).values_list('amount_of_loans',flat=True)
                #samout_of_equipments = ''.join(map(str, amout))
                if teste:
                    Equipment_user.objects.filter(devolution=None,equiment=Equipment.objects.get(id = chave)).update(usuario2=Client.objects.get(id = a),devolution=timezone.now())
                    Equipment.objects.filter(id = chave).update(status='Livre')
                    return equipment_list(request)
            equipment= get_object_or_404(Equipment, pk=pk)
            return render(request, 'equipments/equipment_detail.html', {'object':equipment})
        equipment= get_object_or_404(Equipment, pk=pk)
        return render(request, 'equipments/equipment_detail.html', {'object':equipment})
    return render(request, 'login.html')

def filter_list(request,pk,templete_name='equipments/equipment_list.html'):
    pk = pk
    #teste = Equipment_user.objects.filter(devolution=None)
    #print(teste)
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
        data['object_list'] = equipment
        data['object_list'] = equipment
        data['tipo']= tipo
        return render(request, templete_name, data)
    return render(request, 'login.html')

def filter_type(request,value,templete_name='equipments/equipment_list.html'):
    pk = value
    print(pk)
    #teste = Equipment_user.objects.filter(devolution=None)
    #print(teste)
    if request.session.has_key('username'):
        filtro = pk
        equipment = Equipment.objects.filter(type_equipment = Equipment_type.objects.get(name = filtro)).order_by('status','tag')
        tipo = Equipment_type.objects.all().values_list('name',flat=True)
        data = {}
        data['object_list'] = equipment
        data['object_list'] = equipment
        data['tipo']= tipo
        return render(request, templete_name, data)
    return render(request, 'login.html')

def search(request):
    if request.session.has_key('username'):
        if request.method == 'POST':
            name = request.POST['search']
            equipment = Equipment.objects.filter(Q(tag__contains=name) | Q(description__contains=name))
            tipo = Equipment_type.objects.all().values_list('name',flat=True)
            data = {}
            data['object_list'] = equipment
            data['object_list'] = equipment
            data['tipo']= tipo
            return render(request, 'equipments/equipment_list.html', data)
    return render(request, 'login.html')
'''
def timeout(seconds):
    def decorator(function):
        def wrapper(*args, **kwargs):
            def handler(signum, frame):
                raise Exception(f'Timeout of {function.__name__} function')
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(seconds)
            result = function(*args, **kwargs)
            signal.alarm(0)
            return result
        return wrapper
    return decorator

@timeout(seconds=5)
def read_user_name():
    print('Seja bem-vindo')

try:
    read_user_name()
except Exception as e:
    print(e)
'''
def reports_list(request,templete_name='equipments/reports.html'):
    if request.session.has_key('username'):
        equipment = Equipment.objects.all()
        equipment_user = Equipment_user.objects.all()
        data = {}
        data['list0'] = equipment
        data['list1']= equipment_user
        return render(request, templete_name, data)
    return render(request, 'login.html')


class RastreioForm(forms.Form):
    data = {}
    tipo = Equipment_type.objects.all().values_list('name',flat=True)
    data['tipo']= tipo
    #print(data)
    CHOICE = [('Todos','Todos')]
    for QuerySet in tipo:
        CHOICE.append((QuerySet,QuerySet))
    
    #print(CHOICE)
    #type_equipment = forms.CharField(label='ED', max_length=100)
    type_equipment = forms.ChoiceField(label='Tipo',choices=CHOICE)
    tag = forms.CharField(label='Etiqueta', max_length=100)
    description = forms.CharField(label='Descrição', max_length=100)
    #inicio = forms.DateTimeField(label='Intervalo Inicial',input_formats=['%d/%m/%Y %H:%M'])
    inicio = forms.DateTimeField(
        label='Start',
        widget=forms.widgets.DateTimeInput(attrs={'type':'date'}),
    )
    fim = forms.DateTimeField(
        label='End',
        widget=forms.widgets.DateTimeInput(attrs={'type':'date'}),
    )

def get_rastreio(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RastreioForm(request.POST)
        type_equipment = request.POST['type_equipment']
        #print(type_equipment)
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
        data['list0'] = equipment
        data['list1']= equipment_user
        data['list2']= form
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