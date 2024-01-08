from celery import shared_task

from tg.main import RunBot


@shared_task()
def run_tg_bot():
    bot = RunBot
    bot()
