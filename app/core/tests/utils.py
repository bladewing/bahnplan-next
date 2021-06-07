from django.contrib.auth import get_user_model


def login_user(context, username='testuser', password='12345'):
    if not get_user_model().objects.filter(username=username).exists():
        get_user_model().objects.create_user(username=username, password=password)
    context.user = get_user_model().objects.filter(username=username).first()
    context.client.login(username=username, password=password)
