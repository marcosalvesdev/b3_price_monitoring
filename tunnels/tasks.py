from core import celery_app


@celery_app.task
def sum_x_y(x, y):
    return x + y
