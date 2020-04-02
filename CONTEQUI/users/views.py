from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
#from django.http import HttpResponse
#from django.views.generic import ListView, DetailView
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
#rom django.urls import reverse_lazy
from users.models import Client

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['usuario','email','telefone','whatsapp','cpf','senha']

def user_list(request, templete_name='users/user_list.html'):
    if request.session.has_key('username'):
        user = Client.objects.all()
        data = {}
        data['object_list'] = user
        return render(request, templete_name, data)
    return render(request, 'login.html')

def user_view(request, pk, template_name='users/user_detail.html'):
    if request.session.has_key('username'):
        user= get_object_or_404(Client, pk=pk)    
        return render(request, template_name, {'object':user})
    return render(request, 'login.html')

def user_create(request, template_name='users/user_form.html'):
    if request.session.has_key('username'):
        form = ClientForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        return render(request, template_name, {'form':form})
    return render(request, 'login.html')

def user_update(request, pk, template_name='users/user_form.html'):
    if request.session.has_key('username'):
        user= get_object_or_404(Client, pk=pk)
        form = ClientForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
        return render(request, template_name, {'form':form})
    return render(request, 'login.html')

def user_delete(request, pk, template_name='users/user_confirm_delete.html'):
    if request.session.has_key('username'):
        user= get_object_or_404(Client, pk=pk)    
        if request.method=='POST':
            user.delete()
            return redirect('user_list')
        return render(request, template_name, {'object':user})
    return render(request, 'login.html')

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        post = Client.objects.filter(usuario=username,senha=password)
        if post:
            username = request.POST['username']
            request.session['username'] = username
            return redirect('/')
            #tag = 'tag'
            #return render(request, 'home.html',{'tag':tag})
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')
def logout_user(request):
    try:
        del request.session['username']
    except:
        pass
    return render(request,'login.html')

def type_user(request,pk):
    if request.session.has_key('username'):
        if request.method == 'POST':
            chave = int(pk)
            type_user = request.POST['type']
            post = Client.objects.filter(pk=chave)
            if post:
                teste = Client.objects.filter(pk=chave).update(user_type=type_user)
                return user_list(request)
        user= get_object_or_404(Client, pk=pk)
        return render(request, 'users/user_detail.html', {'object':user})
    return render(request, 'login.html')