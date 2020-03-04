from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
# Create your views here.
from equipments.models import Equipment
from equipments.models import Client

class HomePageView(TemplateView):
    template_name = 'home.html'
class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['tag','description','typ','maximum_time']
class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['usuario','nome','email','telefone','cpf','data_de_nascimento','sexo']

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
    form = CLientForm(request.POST or None)
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
