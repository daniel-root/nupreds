from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
from equipments.models import Equipment

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