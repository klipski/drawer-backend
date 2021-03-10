from datetime import datetime, timedelta

from app.celery import app
from drawer.models import Drawer


@app.task(name='delete_expired_bookmarks')
def delete_expired_bookmarks():
    for drawer in Drawer.objects.all():
        if drawer.remove_after_days:
            drawer.bookmarks.filter(
                deleted_at__lt=datetime.now() - timedelta(days=drawer.remove_after_days)
            ).delete()
