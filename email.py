# faça um pip install pandas openpyxl psutil antes de rodar os scripts se preferir tambem utilize um venv

import imaplib
import email
from email.message import EmailMessage
import smtplib
import os
from pathlib import Path
import time

# Configurações de e-mail (substitua pelos seus dados)
EMAIL = "seuemail@gmail.com"
SENHA = "sua_senha_ou_app_password"
IMAP_SERVER = "imap.gmail.com"   # serve para ler o email (pode manter o gmail ou trocar por outlook, etc)
SMTP_SERVER = "smtp.gmail.com"   # serve para enviar o email

def ler_emails_na_caixa():
    """Lê e-mails não lidos da caixa de entrada."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, SENHA)
    mail.select("inbox")
    
    _, search_data = mail.search(None, "UNSEEN")
    emails_processados = []
    
    for num in search_data[0].split():
        _, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        
        msg = email.message_from_bytes(raw_email)
        subject = msg["Subject"]
        from_ = msg["From"]
        
        emails_processados.append({
            "de": from_,
            "assunto": subject,
            "data": msg["Date"]
        })
        
    
    mail.logout()
    return emails_processados

def enviar_alerta(destinatario, assunto, corpo):
    """Envia e-mail de alerta ou relatório."""
    msg = EmailMessage()
    msg['Subject'] = assunto
    msg['From'] = EMAIL
    msg['To'] = destinatario
    msg.set_content(corpo)
    
    with smtplib.SMTP_SSL(SMTP_SERVER, 465) as server:
        server.login(EMAIL, SENHA)
        server.send_message(msg)
    
    print(f"✅ E-mail enviado para {destinatario}")

if __name__ == "__main__":
    print("🚀 Iniciando automação de e-mails...")
    while True:
        emails = ler_emails_na_caixa()
        if emails:
            print(f"📧 {len(emails)} novos e-mails encontrados.")
            # Exemplo: enviar relatório
            enviar_alerta("analista@empresa.com", 
                         "Relatório Automático - Telemetria",
                         "Processamento concluído com sucesso.\n\n" + str(emails))
        time.sleep(300)  # Coloquei para verificar o email a cada 5 minutos