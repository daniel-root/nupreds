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

def user_list(request, templete_name='users/user_list.html'):
    if request.session.has_key('username'):
        name = request.session['username']
        type_privilegio = Client.objects.filter(usuario=name)
        data = {}
        data['object_list'] = UserAll()
        data['type_user'] = type_privilegio
        return render(request, templete_name, data)
    return render(request, 'login.html')

def user_list_inactive(request,templete_name='users/user_list.html'):
    if request.session.has_key('username'):
        name = request.session['username']
        type_privilegio = Client.objects.filter(usuario=name)
        data = {}
        data['object_list'] = UserInactive()
        data['type_user'] = type_privilegio
        return render(request, templete_name, data)
    return render(request, 'login.html')

def user_view(request, pk, template_name='users/user_detail.html'):
    if request.session.has_key('username'):
        user= get_object_or_404(Client, pk=pk)    
        return render(request, template_name, {'object':user})
    return render(request, 'login.html')

def user_create(request, template_name='users/user_form.html'):
    if request.session.has_key('username'):
        data = {}
        user = {'id': 'None'}
        form = ClientForm(request.POST or None)
        data['form']= form
        data['user']= user
        if request.method == 'POST':
            data['form'].usuario = request.POST['usuario']
            data['form'].email = request.POST['email']
            data['form'].telefone = request.POST['telefone']
            data['form'].cpf = request.POST['cpf']
            data['form'].senha = request.POST['senha']
            new = request.POST['usuario']
            data['form'].save()
            new = Client.objects.filter(usuario=new)
            number = aleatorio()
            new.update(cod_telegram=number)
            email_cadastro(new[0].usuario,number,new[0].email)
            #print(new[0].id)
            return user_update(request, new[0].id)
        return render(request, template_name, data)
    return render(request, 'login.html')

def user_update(request, pk, template_name='users/user_form.html'):
    if request.session.has_key('username'):
        #print('chequi')
        data = {}
        user= get_object_or_404(Client, pk=pk)
        form = ClientForm(request.POST or None, instance=user)
        data['form']= form
        data['user']= user
        if request.method == 'POST':
            data['form'].usuario = request.POST['usuario']
            data['form'].email = request.POST['email']
            data['form'].telefone = request.POST['telefone']
            data['form'].cpf = request.POST['cpf']
            data['form'].senha = request.POST['senha']
            data['form'].save()
            return render(request, template_name, data)
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

def user_fingerprint(request, pk, template_name='users/user_fingerprint.html'):
    if request.session.has_key('username'):
        data = {}
        data['object'] = get_object_or_404(Client, pk=pk)
        data['frase'] = 'Click em inicar!'
        if request.method=='POST':
            #result, pFeatures1, nFeatures1Size = CaptureFinger("any finger", hReader, DPFJ_FMD_ISO_19794_2_2005, byref(pFeatures1), byref(nFeatures1Size))
            #string = ''.join(chr(i) for i in nFeatures1Size)
            #print(string)
            #return string
            #data['frase'] = 'Coloque o dedo no leitor!'
            #print("Aqui")
            result = main("Registro")
            if result[0] != 'F':
                data['frase'] = result
            #print(result,len(result))
            else:
                Client.objects.filter(id = data['object'].id).update(fingerprint=result)
                data['frase'] = 'Registro Completo!'
            return render(request, template_name, data)
            #return user_fingerprint_registration(request,data['frase'],pk )
        
        return render(request, template_name, data)
    return render(request, 'login.html')


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


def user_teste(request, template_name='users/user_teste.html'):
    if request.session.has_key('username'):
        #user= Client.objects.all()
        data = {}
        data['nome']= None
        if request.method=='POST':
            result = main("Verification")
            if result:
                data['nome']= ('Bem Vindx, ' + result)
            else: data['nome'] = 'Digital não reconhecida no banco de dados! Tente novamente'
            return render(request, template_name,data )
            return redirect('user_list')
        return render(request, template_name)
    return render(request, 'login.html')
    '''
    if request.session.has_key('username'):
        user= get_object_or_404(Client, pk=pk)    
        if request.method=='POST':
            user.delete()
            return redirect('user_list')
        return render(request, template_name, {'object':user})
    return render(request, 'login.html')
    '''

def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password =  request.POST['password']
        post = Client.objects.filter(Q(user_type='Administrador') | Q(user_type='Super'),usuario=username,senha=password, )
        if post:
            username = request.POST['username']
            request.session['username'] = username
            return render(request, 'home.html')
        elif Client.objects.filter(usuario=username,senha=password):
            messages.error(request, 'Usuario não autorizado.')
            return render(request, 'login.html')
        else :
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