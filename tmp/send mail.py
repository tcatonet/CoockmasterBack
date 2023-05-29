#
# @app.route("/contact/mail", methods=['POST'])
# def contactSendMail():
#     dto = request.get_json()
#
#     # building mail content
#     sent_mail = f'Subject: Sender: {dto["user_email"]} {dto["subject"]}\n\n{dto["message"]}'
#     data = {'mail_content': sent_mail}
#
#     # sending it accordingly to our mail config
#     try:
#         s = smtplib.SMTP(MailConfig['server'], MailConfig['smtp_port'])
#         s.starttls()
#         s.login(MailConfig['user'], MailConfig['password'])
#         s.sendmail(MailConfig['email'], MailConfig['email'], sent_mail)
#         s.quit()
#
#     except Exception:
#         return response_failure(message=ErrorMessages.SENDMAIL_ERROR, data=data)
#     return response_success(True, InfoMessages.SENDMAIL_SUCCESS, data=data)

