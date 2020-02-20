from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.
from users.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['user','cpf','phone','whatsapp']

def user_list(request, templete_name='users/user_list.html'):
    user = User.objects.all()
    data = {}
    data['object_list'] = user
    return render(request, templete_name, data)

def user_view(request, pk, template_name='users/user_detail.html'):
    user= get_object_or_404(User, pk=pk)    
    return render(request, template_name, {'object':user})

def user_create(request, template_name='users/user_form.html'):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('user_list')
    return render(request, template_name, {'form':form})

def user_update(request, pk, template_name='users/user_form.html'):
    user= get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('use_list')
    return render(request, template_name, {'form':form})

def user_delete(request, pk, template_name='users/user_confirm_delete.html'):
    user= get_object_or_404(User, pk=pk)    
    if request.method=='POST':
        user.delete()
        return redirect('use_list')
    return render(request, template_name, {'object':user})

