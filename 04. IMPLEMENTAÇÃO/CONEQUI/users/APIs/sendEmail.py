import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def email_atraso(name, equipment, tag, description,msgFrom):
	try:
		msgFrom = str(msgFrom)
		smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
		print(smtpObj)
		smtpObj.ehlo()
		smtpObj.starttls()
		msgTo = 'nupreds@gmail.com'
		toPass = 'hYV83BBDA2ebx8r'
		smtpObj.login(msgTo, toPass)
		msg = MIMEMultipart('alternative')
		text ="""
		Olá, """ + str(name) + """, tudo bem? 
		Notamos que você está muito tempo com """ + str(equipment) + """, """ + str(tag) + """ - """ + str(description) + """. Quando você puder dirija-se à recepção para fazer a devolução ou realizar novamente o empréstimo deste equipamento."""
		html = """\
		<html>
		<head></head>
		<body>
				<p>Olá, """ + str(name) + """, tudo bem?</p>
		<p>Notamos que você está muito tempo com """ + str(equipment) + """, """ + str(tag) + """ - """ + str(description) + """. Quando você puder dirija-se à recepção para fazer a devolução ou realizar novamente o empréstimo deste equipamento.</p>
		</body>
		</html>
		"""
		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(html, 'html')
		msg.attach(part1)
		msg.attach(part2)
		smtpObj.sendmail(msgTo,msgFrom,'Subject: Atraso!\n{}'.format( msg.as_string()))
		smtpObj.quit()
		
		return True
	except:
		return False

def email_cadastro(name,codigo,msgFrom):
	try:
			msgFrom = str(msgFrom)
			smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
			smtpObj.ehlo()
			smtpObj.starttls()
			msgTo = 'nupreds@gmail.com'
			toPass = 'hYV83BBDA2ebx8r'
			smtpObj.login(msgTo, toPass)
			msg = MIMEMultipart('alternative')
			number = str(codigo)
			name = str(name)
			text = name + """
					, seu cadastro foi realizado com sucesso no sistema Conequi, controle de equipamentos do IFCE, campus Tianguá.
					Por meio deste canal mandaremos informes, especialmente, sobre atrasos na devolução. Assim, mandaremos lembretes para você.
					Você também tem a opção de usar o aplicativo do Telegram, basta utilizar o seguinte código """ + number + """ para acordar nosso Bot. Acesse o link: https://t.me/conequi_bot."""	
			html = """\
			<html>
			<head></head>
			<body>
				<p>""" + name + """ , seu cadastro foi realizado com sucesso no sistema Conequi, controle de equipamentos do IFCE, campus Tianguá.&#128526;</p>
				<p>Por meio deste canal mandaremos informes, especialmente, sobre atrasos na devolução. Assim, mandaremos lembretes para você.&#129325;&#129325;&#129325;</p>
				<p>Você também tem a opção de usar o aplicativo do Telegram &#128241;, basta utilizar o seguinte código <strong>""" + number + """</strong> para acordar nosso Bot. Acesse o link: https://t.me/conequi_bot.</p>
			</body>
			</html>
			"""
			part1 = MIMEText(text, 'plain')
			part2 = MIMEText(html, 'html')
			msg.attach(part1)
			msg.attach(part2)
			smtpObj.sendmail(msgTo,msgFrom,'Subject: Bem-vindo!\n{}'.format( msg.as_string()))
			smtpObj.quit()
			return True
	except:
			return False