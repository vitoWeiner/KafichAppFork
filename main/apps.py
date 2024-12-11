from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from django.contrib.auth.models import Group 
        from django.db.models.signals import post_migrate

        def create_groups(sender, **kwargs):
            Group.objects.get_or_create(name='Administrator')
            Group.objects.get_or_create(name='Korisnik')

       
        post_migrate.connect(create_groups, sender=self)

    