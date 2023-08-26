from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from parking_backend import settings

User = get_user_model()


@receiver(post_save, sender=User)
def post_save_admin(sender, instance, created, **kwargs):
    '''
    Отправляет письмо с информацией о создании нового администратора.

    Функция вызывается после сохранения экземпляра модели User.
    Если был создан новый администратор,
    функция отправляет на его email письмо с приветствием
    и ссылкой на панель администратора.

    '''
    if created and instance.is_staff:
        subject = 'Создана новая учетная запись администратора'
        admin_url = f'{settings.SITE_NAME}/admin/'
        message = (
            f'Добро пожаловать в команду администраторов Parkonaft. '
            f'Для входа в панель администратора переходите '
            f'по ссылке {admin_url} и авторизируйтесь!'
        )
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]
        send_mail(subject, message, from_email, recipient_list)
