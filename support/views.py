from django.shortcuts import render

# Create your views here.

def support(request):
    """Support page view"""
    return render(request, "support.html")