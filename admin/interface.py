from zah.router.shortcuts import get_router
from zah.urls import render, url


class AdminInterface:
    default_router = get_router()
    
    def home(self):
        def view(request, **kwargs):
            return render(request, 'index.html')
        return view
    
    @property
    def urls(self):
        return [
            url('/admin', self.home(), name='admin')
        ]
    
    
admin_interface = AdminInterface()
