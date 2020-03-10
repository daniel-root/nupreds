from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from equipments.models import Equipment
from equipments.models import Client
from equipments.models import Equipment_type
from equipments.models import Equipment_user

class HomePageView(TemplateView):
    template_name = 'home.html'
class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['tag','description','typ','maximum_time']
class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['usuario','nome','email','telefone','cpf','data_de_nascimento','sexo','senha']

class TypeForm(ModelForm):
    class Meta:
        model = Equipment_type
        fields = ['name']

class UserEquipmentForm(ModelForm):
    class Meta:
        model = Equipment_user
        fields = ['loan','devolution','equiment','client_loan','client_devolution']

def equipment_list(request, templete_name='equipments/equipment_list.html'):
    equipment = Equipment.objects.all()
    data = {}
    data['object_list'] = equipment
    return render(request, templete_name, data)

def equipment_view(request, pk, template_name='equipments/equipment_detail.html'):
    equipment= get_object_or_404(Equipment, pk=pk)    
    return render(request, template_name, {'object':equipment})

def equipment_create(request, template_name='equipments/equipment_form.html'):
    form = EquipmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, template_name, {'form':form})

def equipment_update(request, pk, template_name='equipments/equipment_form.html'):
    equipment= get_object_or_404(Equipment, pk=pk)
    form = EquipmentForm(request.POST or None, instance=equipment)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, template_name, {'form':form})

def equipment_delete(request, pk, template_name='equipments/equipment_confirm_delete.html'):
    equipment= get_object_or_404(Equipment, pk=pk)    
    if request.method=='POST':
        equipment.delete()
        return redirect('equipment_list')
    return render(request, template_name, {'object':equipment})


def client_list(request, templete_name='clients/client_list.html'):
    client = Client.objects.all()
    data = {}
    data['object_list'] = client
    return render(request, templete_name, data)

def client_view(request, pk, template_name='clients/client_detail.html'):
    client = get_object_or_404(Client, pk=pk)    
    return render(request, template_name, {'object':client})

def client_create(request, template_name='clients/client_form.html'):
    form = ClientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('client_list')
    return render(request, template_name, {'form':form})

def client_update(request, pk, template_name='clients/client_form.html'):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    if form.is_valid():
        form.save()
        return redirect('client_list')
    return render(request, template_name, {'form':form})

def client_delete(request, pk, template_name='clients/client_confirm_delete.html'):
    client= get_object_or_404(Client, pk=pk)    
    if request.method=='POST':
        client.delete()
        return redirect('client_list')
    return render(request, template_name, {'object':client})

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

def equipment_user_create(request, template_name='equipments/equipment_user_form.html'):
    form = UserEquipmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, template_name, {'form':form})

def equipment_user_update(request, pk, template_name='equipments/equipment_user_form.html'):
    equipment_user = get_object_or_404(Equipment_user, pk=pk)
    form = UserEquipmentForm(request.POST or None, instance=equipment_user)
    if form.is_valid():
        form.save()
        return redirect('equipment_list')
    return render(request, template_name, {'form':form})

def equipment_user_view(request, pk, template_name='equipments/equipment_user_detail.html'):
    equipment_user= get_object_or_404(Equipment_user, pk=pk)    
    return render(request, template_name, {'object':equipment_user})
