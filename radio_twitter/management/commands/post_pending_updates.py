from django.core.management.base import BaseCommand, CommandError
from radio_twitter.models import Credential, PendingUpdate

class Command(BaseCommand):
    def handle(self, *args, **options):
        pending_updates = PendingUpdate.objects.filter(has_posted=False)
        credentials = Credential.objects.filter(is_active=True)
        for pending_update in pending_updates:
            for credential in credentials:
                api = credential.get_api()
                api.PostUpdate(status=pending_update.status)
        pending_updates.update(has_posted=True)
        PendingUpdate.objects.filter(has_posted=True).delete()  # cull all of the old updates
