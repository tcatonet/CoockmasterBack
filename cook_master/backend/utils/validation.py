from flask_mail import Message
from flask import current_app
valid_email_regex = r"[^@]+@[^@]+\.[^@]+"
valid_phone_regex = '^(33|0)(6|7|9)\d{8}$'


def send_confirmation_mail(new_user_email, code):
    confirmation_email = Message('Thanks you for joining in !', sender=current_app.config['MAIL_USERNAME'], recipients=[new_user_email])
    body = 'Welcome to GD Analysis !\n'
    body += f'In order to complete your subscription, we just need you use this code: {code} \n'
    body += 'Bests regards\nThe CM Team'
    confirmation_email.body = body
    return confirmation_email


def send_confirmation_creation_account(new_user_email):
    confirmation_email = Message('Acount sucessfully validate !', sender=current_app.config['MAIL_USERNAME'], recipients=[new_user_email])
    body = 'Welcome to GD Analysis !\n'
    body += f'In order to complete your subscription, we just need you use this code:\n'
    body += 'Bests regards\nThe CM Team'
    confirmation_email.body = body
    return confirmation_email


def send_update_password_mail(new_user_email, flask_root_url, token):
    link = flask_root_url + f'verification/{token}'
    confirmation_email = Message('Password update', sender=current_app.config['MAIL_USERNAME'], recipients=[new_user_email])
    body = 'Password update !\n'
    body += f': {link} \n'
    body += 'Bests regards\nThe CM Team'
    confirmation_email.body = body
    return confirmation_email


def send_update_email_mail(new_user_email, flask_root_url, token):
    link = flask_root_url + f'verification/{token}'
    confirmation_email = Message('Email update', sender=current_app.config['MAIL_USERNAME'], recipients=[new_user_email])
    body = 'Email update !\n'
    body += f'In order to complete your subscription, we just need you to visit once the following link: {link} \n'
    body += 'Bests regards\nThe CM Team'
    confirmation_email.body = body
    return confirmation_email


def send_delete_account_mail(new_user_email, flask_root_url, token):
    link = flask_root_url + f'verification/{token}'
    confirmation_email = Message('Account delete', sender=current_app.config['MAIL_USERNAME'], recipients=[new_user_email])
    body = 'Account delete !\n'
    body += f'In order to complete your subscription, we just need you to visit once the following link: {link} \n'
    body += 'Bests regards\nThe CM Team'
    confirmation_email.body = body
    return confirmation_email


def send_retrieve_password_mail(new_user_email, flask_root_url, token):
    link = flask_root_url + f'verification/{token}'
    confirmation_email = Message('Retrieve password !', sender=current_app.config['MAIL_USERNAME'], recipients=[new_user_email])
    body = 'Retrieve password !\n'
    body += f'In order to complete your subscription, we just need you to visit once the following link: {link} \n'
    body += 'Bests regards\nThe CM Team'
    confirmation_email.body = body
    return confirmation_email