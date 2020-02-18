from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.
from equipments.models import Equipment

class EquipmentForm(ModelForm):
    class Meta:
        model = Equipment
        fields = ['tag','description','typ','maximum_time']

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
'''
class EquipmentList(ListView):
    model = Equipment

class EquipmentView(DetailView):
    model = Equipment

class EquipmentCreate(CreateView):
    model = Equipment
    fields = ['tag','description','typ','maximum_time']
    success_url = reverse_lazy('equipment_list')

class EquipmentUpdate(UpdateView):
    model = Equipment
    fields = ['tag','description','type','maximum_time']
    success_url = reverse_lazy('equipment_list')

class EquipmentDelete(DeleteView):
    model = Equipment
    success_url = reverse_lazy('equipment_list')

'''