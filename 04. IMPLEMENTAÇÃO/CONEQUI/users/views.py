from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from users.models import Client
from django.db.models import Q
from django.contrib import messages 
#import users.DigitalPersona.enrollment as finger
from users.APIs.sendEmail import email_cadastro
from users.APIs.sendTelegram import aleatorio
from users.APIs.fingerPrint import *

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['usuario','email','telefone','cpf','senha']
        

def UserAll():
    user = Client.objects.filter(inative=False)
    return user

def UserInactive():
    user = Client.objects.filter(inative=True)
    return user

from django.core.paginator import Paginator
def get_page(request,objects):
    objetcs = objects
    paginator = Paginator(objetcs,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def user_list(request, templete_name='users/user_list.html'):
    if request.session.has_key('username'):
        name = request.session['username']
        type_privilegio = Client.objects.filter(usuario=name)
        data = {}
        data['object_list'] = get_page(request,UserAll())
        data['type_user'] = type_privilegio
        data['type'] = 'Todos'
        data['search'] = 'Null'
        return render(request, templete_name, data)
    return render(request, 'login.html')

def user_list_inactive(request,templete_name='users/user_list.html'):
    if request.session.has_key('username'):
        name = request.session['username']
        type_privilegio = Client.objects.filter(usuario=name)
        data = {}
        data['object_list'] = get_page(request,UserInactive())
        data['type_user'] = type_privilegio
        data['type'] = 'Inativos'
        data['search'] = 'Null'
        return render(request, templete_name, data)
    return render(request, 'login.html')

def user_view(request, pk, template_name='users/user_detail.html'):
    if request.session.has_key('username'):
        user= get_object_or_404(Client, pk=pk)    
        return render(request, template_name, {'object':user})
    return render(request, 'login.html')
count = 0
def user_create(request, template_name='users/user_form.html'):
    global count
    if request.session.has_key('username'):
        data = {}
        user = {'id': 'None'}
        form = ClientForm(request.POST or None)
        data['form']= form
        data['user']= user
        if request.method == 'POST':
            result = main("Registro")
            
            if result[0] != 'F':
                #print("aqui")
                user = Client.objects.filter(cpf=request.POST['cpf'])
                if not user:    
                    new_user = Client.objects.create(
                        usuario = request.POST['usuario'],
                        email = request.POST['email'],
                        telefone = request.POST['telefone'],
                        cpf = request.POST['cpf'],
                        senha = request.POST['pwd1'],
                        #fingerprint=result
                    )
                    new = Client.objects.filter(usuario=request.POST['usuario'])
                    number = aleatorio()
                    internet = email_cadastro(new[0].usuario,number,new[0].email)
                    if internet:
                        new.update(cod_telegram=number)
                    #print(new[0].id)
                    #Client.objects.filter(id = data['object'].id).update(fingerprint=result)
                    messages.success(request, "Cadastro Realizado!")
                    messages.error(request, "Digital não cadastrada! Tente novamente em Recadastrar Digital.")
                    return redirect('/Usuario/Editar/'+str(new[0].id))
                else:
                    messages.error(request, 'Usuário já existe!')
                    messages.error(request, result)
                    #data['mensagem'] = 'Te acorda menino!'
                    data['user'] = {'usuario':request.POST['usuario'],
                        'email':request.POST['email'],
                        'telefone':request.POST['telefone'],
                        'cpf':request.POST['cpf'],
                        'senha':request.POST['pwd1'],
                        'id':'None'
                    }
                '''
                count = count + 1
                #print(count)
                if count <= 2:
                    messages.error(request, result)
                    data['user'] = {'usuario':request.POST['usuario'],
                        'email':request.POST['email'],
                        'telefone':request.POST['telefone'],
                        'cpf':request.POST['cpf'],
                        'senha':request.POST['pwd1'],
                        'id':'None'
                    }
                    return render(request, template_name, data)
                else:
                    messages.error(request, "Não foi possivel fazer a leitura da digital")
                    count=0 
                    data['user'] = {'usuario':request.POST['usuario'],
                        'email':request.POST['email'],
                        'telefone':request.POST['telefone'],
                        'cpf':request.POST['cpf'],
                        'senha':request.POST['pwd1'],
                        'id':'None'
                    }
                    return render(request, template_name, data)
                '''
            else:
                #Client.objects.filter(id = data['object'].id).update(fingerprint=result)
                #data['frase'] = 'Registro Completo!'
                user = Client.objects.filter(cpf=request.POST['cpf'])
                if not user:    
                    new_user = Client.objects.create(
                        usuario = request.POST['usuario'],
                        email = request.POST['email'],
                        telefone = request.POST['telefone'],
                        cpf = request.POST['cpf'],
                        senha = request.POST['pwd1'],
                        fingerprint=result
                    )
                    new = Client.objects.filter(usuario=request.POST['usuario'])
                    number = aleatorio()
                    internet = email_cadastro(new[0].usuario,number,new[0].email)
                    if internet:
                        new.update(cod_telegram=number)
                    #print(new[0].id)
                    return redirect('/Usuario')
                else:
                    messages.error(request, 'Usuário já existe!')
                    #data['mensagem'] = 'Te acorda menino!'
                    data['user'] = {'usuario':request.POST['usuario'],
                        'email':request.POST['email'],
                        'telefone':request.POST['telefone'],
                        'cpf':request.POST['cpf'],
                        'senha':request.POST['pwd1'],
                        'id':'None'
                    }
        return render(request, template_name, data)
    return render(request, 'login.html')

def user_update(request, pk, template_name='users/user_form.html'):
    if request.session.has_key('username'):
        #print('chequi')
        data = {}
        user= get_object_or_404(Client, pk=pk)
        #form = ClientForm(request.POST or None, instance=user)
        #data['form']= form
        data['user']= user
        if request.method == 'POST':
            update_user = Client.objects.filter(pk=pk)
            #print(request.POST)
            update_user.update(
            usuario = request.POST['usuario'],
            email = request.POST['email'],
            telefone = request.POST['telefone'],
            cpf = request.POST['cpf'],
            senha = request.POST['pwd1']
            )
            return redirect('/Usuario')
        return render(request, template_name, data)
    return render(request, 'login.html')
    
def user_delete(request, pk, template_name='users/user_confirm_delete.html'):
    if request.session.has_key('username'):
        user= get_object_or_404(Client, pk=pk)
        if request.method=='POST': 
            if Client.objects.filter(id = pk,inative='True'):
                Client.objects.filter(id = pk).update(inative='False')
            else:
                Client.objects.filter(id = pk).update(inative='True')
            return user_list(request)
        return render(request, template_name, {'object':user})
    return render(request, 'login.html')

def user_fingerprint(request, pk, template_name='users/user_form.html'):
    if request.session.has_key('username'):
        data = {}
        data['object'] = get_object_or_404(Client, pk=pk)
        if request.method=='POST':           
            result = main("Registro")
            if result[0] != 'F':
                print("aquiestou")
                messages.error(request, result)
                return redirect('/Usuario/Editar/'+pk)
                
                #return render(request, template_name, data)
                #data['frase'] = result
            else:
                Client.objects.filter(id = data['object'].id).update(fingerprint=result)
                messages.success(request, "Registro Completo!")
                return redirect('/Usuario/Editar/'+pk)
            #return redirect('/Usuario')
            #return user_fingerprint_registration(request,data['frase'],pk )
        return render(request, template_name, data)
    return render(request, 'login.html')

'''
def user_fingerprint_registration(request, frase,pk, template_name='users/user_fingerprint.html'):
    if request.session.has_key('username'):
        data = {}
        data['object'] = get_object_or_404(Client, pk=pk)
        if frase == 'Click em inicar!':
            #print(data['object'].id)
            #Client.objects.filter(id = data['object'].id).update(fingerprint=finger.main())
            data['frase'] = 'Coloque o dedo no leitor'
            return render(request, template_name, data)
        if frase == 'Coloque o dedo no leitor':
            
            data['frase'] = 'Coloque o mesmo dedo no leitor'
            return render(request, template_name, data)
        if data['frase'] == 'Coloque o dedo indicado no leitor':
            data['frase'] = 'Coloque o dedo novamente no leitor'
            return render(request, template_name, data)
        
        data['frase'] = 'Cadastro completo!'
        return render(request, template_name, data)
    return render(request, 'login.html')
'''
'''
from django.core.paginator import Paginator
def user_teste(request, template_name='users/user_teste.html'):
    if request.session.has_key('username'):
        #user= Client.objects.all()
        data = {}
        data['nome']= None
        contact_list = Client.objects.all()
        paginator = Paginator(contact_list, 3) # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data['page_obj'] = page_obj
        if request.method=='POST':
            result = main("Verification")
            if result:
                data['nome']= ('Bem Vindx, ' + result)
            else: data['nome'] = 'Digital não reconhecida no banco de dados! Tente novamente'
            return render(request, template_name,data)
            return redirect('user_list')
        return render(request, template_name,data)
    return render(request, 'login.html')
    '''
def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        post = Client.objects.filter(Q(user_type='Administrador') | Q(user_type='Super'),usuario=username,senha=password)
        if post:
            username = request.POST['username']
            request.session['username'] = username
            return render(request, 'home.html')
        elif Client.objects.filter(usuario=username,senha=password):
            messages.error(request, 'Usuario não autorizado.')
            return render(request, 'login.html')
        else:
            messages.error(request, 'Usuario e Senha inválidos. Favor Tentar novamente.')
            return render(request, 'login.html')
    return render(request, 'login.html')
    
def logout_user(request,template_name='confirm_logout.html'):
    if request.session.has_key('username'):
        if request.method=='POST': 
            try:
                del request.session['username']
            except:
                pass
            return render(request,'login.html')
        return render(request, template_name)
    return render(request, 'login.html')

    

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

def filter_type(request,value,templete_name='users/user_list.html'):
    if request.session.has_key('username'):
        user = Client.objects.filter(user_type = value, inative=False)
        data = {}
        name = request.session['username']
        type_privilegio = Client.objects.filter(usuario=name)
        data = {}
        data['object_list'] = get_page(request,user)
        data['type_user'] = type_privilegio
        data['type'] = value
        data['search'] = 'Null'
        return render(request, templete_name, data)
    return render(request, 'login.html')

def filter_list(request,pk,value,templete_name='users/user_list.html'):
    if request.session.has_key('username'):
        if value == 'Todos':
            if pk == 'Id':
                filtro = 'id'
            elif pk == 'Nome':
                filtro = 'usuario'
            elif pk == 'CPF':
                filtro = 'cpf'
            user = Client.objects.filter(inative=False).order_by(filtro)
            data = {}
            name = request.session['username']
            type_privilegio = Client.objects.filter(usuario=name)
            data['object_list'] = get_page(request,user)
            data['type_user'] = type_privilegio
            data['type'] = value
            data['search'] = 'Null'
            return render(request, templete_name, data)
        elif value == 'Inativos':
            if pk == 'Id':
                filtro = 'id'
            elif pk == 'Nome':
                filtro = 'usuario'
            elif pk == 'CPF':
                filtro = 'cpf'
            user = Client.objects.filter(inative=True).order_by(filtro)
            data = {}
            name = request.session['username']
            type_privilegio = Client.objects.filter(usuario=name)
            data['object_list'] = get_page(request,user)
            data['type_user'] = type_privilegio
            data['type'] = value
            data['search'] = 'Null'
            return render(request, templete_name, data)
        else:
            filtro = 'id'
            if pk == 'Id':
                filtro = 'id'
            elif pk == 'Nome':
                filtro = 'usuario'
            elif pk == 'CPF':
                filtro = 'cpf'
            user = Client.objects.filter(user_type = value, inative=False).order_by(filtro)
            data = {}
            name = request.session['username']
            type_privilegio = Client.objects.filter(usuario=name)
            data = {}
            data['object_list'] = user
            data['type_user'] = type_privilegio
            data['type'] = value
            data['search'] = 'Null'
            return render(request, templete_name, data)
    return render(request, 'login.html')

def search_user(request,value,search_):
    if request.session.has_key('username'):
        data = {}
        if request.method == 'POST':
            name = request.POST['search']
            data['search'] = name
            return redirect('/Usuario/Pesquisar/'+value+'/'+name)
        else:
            name = search_
            data['search'] = name
        users = Client.objects.filter(Q(usuario__contains=name) | Q(cpf__contains=name))
        name = request.session['username']
        type_privilegio = Client.objects.filter(usuario=name)
        
        data['object_list'] = get_page(request,users)
        data['type_user'] = type_privilegio
        data['type'] = 'type'
        return render(request, 'users/user_list.html', data)
    return render(request, 'login.html')