# import datetime
#
#
# from django.conf import settings
# from django.template.loader import render_to_string
#
# from django.core.mail import EmailMultiAlternatives
#
#
# from .models import Post
#
#
# # функция отправки уведомлений подписчикам на почту о новом объявлении в любимой категории
# def subscribers_send_mails(pk, headline, subscribers_emails):
#     # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
#     html_context = render_to_string(
#         'mail/adv_add_email.html',
#         {
#             'link': f'{settings.SITE_URL}/posts/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         # тема письма
#         subject=headline,
#         # тело пустое, потому что мы используем шаблон
#         body='',
#         # адрес отправителя
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         # список адресатов
#         to=subscribers_emails,
#     )
#
#     msg.attach_alternative(html_context, 'text/html')
#     msg.send(fail_silently=False)
#
#
# # функция отправки на почту автору объявления уведомления о том, что у него есть новый отклик
# def ad_author_send_mail(pk, email):
#     # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
#     html_context = render_to_string(
#         'mail/comment_add_email.html',
#         {
#             'link': f'{settings.SITE_URL}/posts/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         # тема письма
#         subject='Новый отклик',
#         # тело пустое, потому что мы используем шаблон
#         body='',
#         # адрес отправителя
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         # список адресатов
#         to=email,
#     )
#
#     msg.attach_alternative(html_context, 'text/html')
#     msg.send(fail_silently=False)
#
#
# # функция отправки на почту автору оклика уведомления о том, что его отклик принят
# def comment_author_send_mail(pk, email):
#     # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
#     html_context = render_to_string(
#         'mail/reply_approve_email.html',
#         {
#             'link': f'{settings.SITE_URL}/posts/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         # тема письма
#         subject='Отклик принят',
#         # тело пустое, потому что мы используем шаблон
#         body='',
#         # адрес отправителя
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         # список адресатов
#         to=email,
#     )
#
#     msg.attach_alternative(html_context, 'text/html')
#     msg.send(fail_silently=False)
#
#
# # задача, которая уведомляет о новом объявлении в любимом разделе
# @receiver
# def adv_add_notification(pk):
#     adv = PostCategory.objects.get(id=pk)
#     category = adv.category
#     subscribers = []
#     subscribers_emails = []
#     subscribers += category.subscribers.all()
#
#     for s in subscribers:
#         subscribers_emails.append(s.email)
#
#     subscribers_send_mails(adv.pk, adv.headline, subscribers_emails)
#
#
# # задача, которая уведомляет о новом отклике на объявление
# @shared_task
# def reply_add_notification(pk):
#     reply = Reply.objects.get(id=pk)
#     adv = reply.adv
#     adv_author_email = [adv.author.email]
#     ad_author_send_mail(adv.pk, adv_author_email)
#
#
# # задача, которая уведомляет о принятом отклике
# @shared_task
# def reply_approve_notification(pk):
#     reply = Reply.objects.get(id=pk)
#     adv = reply.adv
#     reply_author_email = [reply.user.email]
#     reply_author_send_mail(adv.pk, reply_author_email)
#
