#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Description:
    ============
    Script d'envoi de courriels
    
    Objectif:
    =========
    Tutoyer les méandres du SMTP (http://fr.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol)
    
    Une Application:
    ================
    Faire une farce à ses amis en usurpant leur identité à travers leur adresse e-mail. Il suffit de mettre l'adresse de celui dont on veut usurper l'identité 
    dans le champ --From-- du courriel à envoyer.

"""

#Configuration des paramètres du compte
username = '***'; #votre nom d'utilisateur
password = '***'; #votre mot de passe
server = '***'; #adresse du serveur SMTP (adresse_serveur:port[25,465,587]) 

#Les imports
from time import sleep;
import smtplib;
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText;
from email.mime.multipart import MIMEMultipart;

def create_msg(to_address, from_address='', cc_address='', bcc_address='', subject=''):
"""
    Fonction permettant la création d'un objet MIME (http://fr.wikipedia.org/wiki/Multipurpose_Internet_Mail_Extensions)
    :Entrées:
        les adresses: to, from, cc, bcc
        l'objet: subject
    :Sortie:
        Objet MIME
"""
    msg = MIMEMultipart();
    msg['Subject'] = subject;
    msg['To'] = to_address;
    msg['Cc'] = cc_address;
    msg['From'] = from_address;
    return msg;

def send_email(smtp_address, usr, password, msg, mode):
"""
    Fonction effecuant l'envoi du courriel
    :Entrées:
        adresse du serveur SMTP, le nom d'utilisateur, le mot de passe, un objet MIME et un mode
        si mode = 0: envoi aux adresses to et cc
        si mode = 1: envoi aux adresses bcc
"""
    server = smtplib.SMTP(smtp_address);
    #server.ehlo();
    #server.starttls();
    #server.ehlo();
    #server.login(username,password);
"""
    Les 4 dernières instructions sont à décommenter dans le cas où le serveur oblige une authentification avant l'envoi de courriel (port 465 ou 587 activé)
"""
    if (mode == 0 and msg['To'] != ''):
        server.sendmail(msg['From'],(msg['To']+msg['Cc']).split(","), msg.as_string());
    elif (mode == 1 and msg['Bcc'] != ''):
        server.sendmail(msg['From'],msg['Bcc'].split(","),msg.as_string());
    elif (mode != 0 and mode != 1):
        print 'error in send mail bcc'; print 'email canceled'; exit();
    server.quit();

def compose_email(addresses, subject, body, files):
"""
    Fonction d'envoi de courriel avec tous les détails
    :Entrées: 
        1. Adresses (séparées par des virgules s'il y en a plusieurs): to, from, cc, bcc 
        2. Objet: subject
        3. Contenu du courriel et son type (texte plein ou html): 
            body (list):
                [0] - text
                [1] - type
                        0 - plain
                        1 - html
        4. Fichiers attachés:
            files (list)
"""
    # Les adresses
    to_address = addresses[0];
    from_address = addresses[1];
    cc_address = addresses[2];
    bcc_address = addresses[3];

    # Création d'un message
    msg = create_msg(to_address, from_address=from_address, cc_address=cc_address , subject=subject);

    # Ajout de texte
    for text in body:
        attach_text(msg, text[0], text[1]);

    # Ajout de fichiers
    if (files != ''):
        file_list = files.split(',');
        for afile in file_list:
            attach_file(msg, afile);

    # Envoi du courriel
    send_email(server, username, password, msg, 0);

    # Vérification du champ bcc
    if (bcc_address != ''):
        msg['Bcc'] = bcc_address;
        send_email(server, username, password, msg, 1);
        
    print 'email sent'

# Attacher un texte plein ou html au message
def attach_text(msg, atext, mode):
    part = MIMEText(atext, get_mode(mode));
    msg.attach(part);

# Fonction pour avoir le type de texte
def get_mode(mode):
    if (mode == 0):
        mode = 'plain';
    elif (mode == 1):
        mode = 'html';
    else:
        print 'error in text kind'; print 'email canceled'; exit();
    return mode;

# Fonction prenant en entrée le message à envoyer et un nom de fichier et attache le fichier au message 
def attach_file(msg, afile):
    part = MIMEApplication(open(afile, "rb").read());
    part.add_header('Content-Disposition', 'attachment', filename=afile);
    msg.attach(part);


"""
    Voici un exemple de d'envoi de courriel:
    :Example 1:
    compose_email(['adresse_destinataire','adresse_expéditeur','adresse_copie_carbonne','adresse_copie_carbonne_caché'],'Objet du message',
    [['Contenu du message',0]],'fichier_attaché');
"""
