from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    template_data = {}
    template_data['title'] = 'MoneyParce'
    return render(request, 'home/index.html', {
        'template_data': template_data})


def about(request):
    return render(request, 'home/about.html')

@login_required
def settings_view(request):
    return render(request, "home/settings.html")

# Create your views here.
