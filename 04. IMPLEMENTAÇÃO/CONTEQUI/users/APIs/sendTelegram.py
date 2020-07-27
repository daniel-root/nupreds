import telepot
from random import randrange, uniform

def aleatorio():
    number = randrange(1000, 9999)
    return 'D' + str(number)

def autenticar(n):
    try:
            while True:
                bot = telepot.Bot("1244766207:AAGjFP8KytsFILHQUjXazo1yV7JUqN5w4g8")   
                update = bot.getUpdates()
                if len(update) == 0:
                    return 'Vazia'
                for i in range(0,len(update)):
                    if str(n) == update[i]['message']['text']:
                        number_id = int(update[i]['message']['from']['id'])
                        bot.sendMessage(number_id,"Bem vindo ao Conequi!")
                        bot.sendMessage(number_id,"Seu cadastro foi realizado com sucesso!")
                        return number_id
                return False
    except:
            pass

def enviar(name, equipment, tag, description,number):
    try:
            name = str(name)
            equipment= str(equipment)
            tag = str(tag)
            description = str(description)
            number = int(number)
            bot = telepot.Bot("1244766207:AAGjFP8KytsFILHQUjXazo1yV7JUqN5w4g8")
            print(bot)  
            bot.sendMessage(number,"Olá, "+ name + ", tudo bem? \n Notamos que você está muito tempo com " + equipment + ", " + tag + " - " + description + ". Quando você puder dirija-se à recepção para fazer a devolução ou realizar novamente o empréstimo deste equipamento.")
    except:
		    pass

    