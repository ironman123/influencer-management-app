from celery import Celery
from celery.schedules import crontab

app = Celery(broker_url='redis://localhost:6379/0',
             result_backend='redis://localhost:6379/1')


@app.on_after_configure.connect
def setup_perodic_tasks(sender,**kwargs):
    sender.add_periodic_task(10.0,hello_world.s(),name='add every 10')

@app.task
def hello_world():
    print("Hello!!!")