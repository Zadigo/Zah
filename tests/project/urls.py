from zah.urls import url
from zah.tests.project.views import home

patterns = [
    url('/', home, name='home')
]
