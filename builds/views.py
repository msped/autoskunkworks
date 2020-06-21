from django.shortcuts import render, redirect
from .models import (
    ExteriorCategory,
    EngineCategory,
    RunningCategory,
    InteriorCategory,
    Builds
)
from .utils import new_build_content

# Create your views here.

def create_build(request):
    """Create a Build"""
    exterior_category = ExteriorCategory.objects.all()
    engine_category = EngineCategory.objects.all()
    running_category = RunningCategory.objects.all()
    interior_category = InteriorCategory.objects.all()

    if request.method == "POST":
        new_build_content(
            request,
            exterior_category,
            engine_category,
            running_category,
            interior_category
        )
        return redirect('home')

    context = {
        'exterior': exterior_category,
        'engine': engine_category,
        'running': running_category,
        'interior': interior_category
    }
    
    return render(request, "create.html", context)

def view_build(request, build_id):
    """View a Build"""
    build = Builds.objects.get(id=build_id)
    return render(request, "view.html", {'build': build})