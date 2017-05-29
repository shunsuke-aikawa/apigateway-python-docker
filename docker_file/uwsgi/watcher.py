import uwsgi
from uwsgidecorators import filemon

@filemon('index.py')
def reloaded(num):
    uwsgi.reload()

