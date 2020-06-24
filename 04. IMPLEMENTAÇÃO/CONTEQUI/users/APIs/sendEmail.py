import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def email_atraso(name, equipment, tag, description,msgFrom):
    try:
        msgFrom = str(msgFrom)
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        msgTo = 'nupreds@gmail.com'
        toPass = 'hYV83BBDA2ebx8r'
        smtpObj.login(msgTo, toPass)
        #msg = '''
        #Daniel, seu cadastro foi realizado com sucesso!
        #'''
        msg = MIMEMultipart('alternative')

        #msg['Subject'] = "Link"
        #msg['From'] = "my@email.com"
        #msg['To'] = "your@email.com"
        
        #name = 'Daniel'
        #equipment = 'Chave'
        #tag = '069'
        #description = 'Incubadora'

        text ="""
        Olá, """ + str(name) + """, tudo bem? 
        Notamos que você está muito tempo com """ + str(equipment) + """, """ + str(tag) + """ - """ + str(description) + """. Quando você puder dirija-se a recepção para fazer a devolução ou realizar novamente o empréstimo deste equipamento."""
        html = """\
        <html>
        <head></head>
        <body>
                <p>Olá, """ + str(name) + """, tudo bem?</p>
        <p>Notamos que você está muito tempo com """ + str(equipment) + """, """ + str(tag) + """ - """ + str(description) + """. Quando você puder dirija-se a recepção para fazer a devolução ou realizar novamente o empréstimo deste equipamento.</p>
        </body>
        </html>
        """

        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        msg.attach(part1) # text must be the first one
        msg.attach(part2) # html must be the last one

        smtpObj.sendmail(msgTo,msgFrom,'Subject: Atraso!\n{}'.format( msg.as_string()))
        #smtpObj.sendmail(msgTo,msgFrom,message)
        smtpObj.quit()
        print("Email enviado com sucesso!")
    except:
            print("Erro ao enviar e-mail")

def email_cadastro(name,codigo,msgFrom):
	try:
			msgFrom = str(msgFrom)
			smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
			smtpObj.ehlo()
			smtpObj.starttls()
			msgTo = 'nupreds@gmail.com'
			toPass = 'hYV83BBDA2ebx8r'
			smtpObj.login(msgTo, toPass)
			#msg = '''
			#Daniel, seu cadastro foi realizado com sucesso!
			#'''
			msg = MIMEMultipart('alternative')

			#msg['Subject'] = "Link"
			#msg['From'] = "my@email.com"
			#msg['To'] = "your@email.com"
			
			number = str(codigo)
			name = str(name)

			text = name + """
					, seu cadastro foi realizado com sucesso no sistema Conequi, controle de equipamentos do IFCE, campus Tianguá.
					Através deste e-mail estaremos mandando informes, se houver atraso na devolução mandaremos o e-mail de lembrete para você.
					Também damos a opção de lembrete por meio do Telegram, basta utilizar o seguinte código:""" + number + """. Acesse o link: https://t.me/conequi_bot. 
					Após acessar o link, irá abrir um chat com nosso robozinho, clique em start, e em seguida coloque o código que você recebeu. Nosso robozinho irá reconhecer você e mandará uma mensagem de cadastro realizado!"""	
			html = """\
			<html>
			<head></head>
			<body>
				<p>""" + name + """ , seu cadastro foi realizado com sucesso no sistema Conequi, controle de equipamentos do IFCE, campus Tianguá.&#128526;</p>
				<p>Através deste e-mail estaremos mandando informes, se houver atraso na devolução mandaremos o e-mail de lembrete para você.&#129325;&#129325;&#129325;</p>
				<p>Também damos a opção de lembrete por meio do Telegram &#128241;, basta utilizar o seguinte código:<strong>""" + number + """</strong>. Acesse o link: https://t.me/conequi_bot.</p>
				<p>Após acessar o link, irá abrir um chat com nosso robozinho &#129302;, clique em start, e em seguida coloque o código que você recebeu. Nosso robozinho irá reconhecer você e mandará uma mensagem de cadastro realizado!</p>
			</body>
			</html>
			"""

			part1 = MIMEText(text, 'plain')
			part2 = MIMEText(html, 'html')

			msg.attach(part1) # text must be the first one
			msg.attach(part2) # html must be the last one

			smtpObj.sendmail(msgTo,msgFrom,'Subject: Bem-vindo!\n{}'.format( msg.as_string()))
			#smtpObj.sendmail(msgTo,msgFrom,message)
			smtpObj.quit()
			print("Email enviado com sucesso!")
	except:
			print("Erro ao enviar e-mail")