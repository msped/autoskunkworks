from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.db.models import Count
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

    if request.user.id is not build.author.id:
        build.views += 1
        build.save()
    user_liked = False
    user_disliked = False
    if request.user.is_authenticated:
        if build.likes.filter(id=request.user.id):
            user_liked = True
        if build.dislikes.filter(id=request.user.id):
            user_disliked = True
    else: 
        user_liked = True
        user_disliked = True

    context = {
        'build': build,
        'user_liked': user_liked,
        'user_disliked': user_disliked
    }
    return render(request, "view.html", context)

def builds(request):

    """Show all builds that are public"""
    sort_by_price = request.GET.get('sort_by_price')
    sort_by_likes = request.GET.get('sort_by_likes')
    sort_by_views = request.GET.get('sort_by_views')

    if sort_by_price and sort_by_likes is None and sort_by_views is None:
        if sort_by_price == "high_to_low":
            builds = Builds.objects.filter(private=False).order_by('-total')
        else:
            builds = Builds.objects.filter(private=False).order_by('total')
    elif sort_by_likes and sort_by_price is None and sort_by_views is None:
        if sort_by_likes == "high_to_low":
            builds = Builds.objects.filter(private=False).order_by('-like_count')
        else:
            builds = Builds.objects.filter(private=False).order_by('-dislike_count')
    elif sort_by_views and sort_by_price is None and sort_by_likes is None:
        if sort_by_views == "high_to_low":
            builds = Builds.objects.filter(private=False).order_by('-views')
        else:
            builds = Builds.objects.filter(private=False).order_by('views')
    elif sort_by_likes and sort_by_price and sort_by_views is None:
        if sort_by_price == "high_to_low":
            if sort_by_likes == "high_to_low":
                builds = Builds.objects.filter(private=False).order_by('-total', '-like_count')
            else:
                builds = Builds.objects.filter(private=False).order_by('-total', 'like_count')
        else:
            if sort_by_likes == "high_to_low":
                builds = Builds.objects.filter(private=False).order_by('total', '-like_count')
            else:
                builds = Builds.objects.filter(private=False).order_by('total', 'like_count')
    elif sort_by_likes and sort_by_views and sort_by_price is None:
        if sort_by_views == "high_to_low":
            if sort_by_likes == "high_to_low":
                builds = Builds.objects.filter(private=False).order_by('-views', '-like_count')
            else:
                builds = Builds.objects.filter(private=False).order_by('-views', 'like_count') 
        else:
            if sort_by_likes == "high_to_low":
                builds = Builds.objects.filter(private=False).order_by('views', '-like_count')
            else:
                builds = Builds.objects.filter(private=False).order_by('views', 'like_count')
    elif sort_by_price and sort_by_views and sort_by_likes is None:
        if sort_by_price == "high_to_low":
            if sort_by_views == "high_to_low":
                builds = Builds.objects.filter(private=False).order_by('-total', '-views')
            else:
                builds = Builds.objects.filter(private=False).order_by('-total', 'views')
        else:
            if sort_by_views == "high_to_low":
                builds = Builds.objects.filter(private=False).order_by('total', '-views')
            else:
                builds = Builds.objects.filter(private=False).order_by('total', 'views')
    elif sort_by_likes and sort_by_price and sort_by_views:
        if sort_by_likes == "high_to_low":
            if sort_by_price == "high_to_low":
                if sort_by_views == "high_to_low":
                    builds = Builds.objects.filter(private=False).order_by('-total', '-views', '-like_count')
                else:
                    builds = Builds.objects.filter(private=False).order_by('-total', '-views', '-like_count')
            else:
                if sort_by_views == "high_to_low":
                    builds = Builds.objects.filter(private=False).order_by('total', '-views', '-like_count')
                else:
                    builds = Builds.objects.filter(private=False).order_by('total', '-views', '-like_count')
        else:
            if sort_by_price == "high_to_low":
                if sort_by_views == "high_to_low":
                    builds = Builds.objects.filter(private=False).order_by('-total', '-views', 'like_count')
                else:
                    builds = Builds.objects.filter(private=False).order_by('-total', '-views', 'like_count')
            else:
                if sort_by_views == "high_to_low":
                    builds = Builds.objects.filter(private=False).order_by('total', '-views', 'like_count')
                else:
                    builds = Builds.objects.filter(private=False).order_by('total', '-views', 'like_count')
    else:
        builds = Builds.objects.filter(private=False)

    paginator = Paginator(builds, 15)
    page = request.GET.get('page')
    builds_paginator = paginator.get_page(page)

    return render(request, "builds.html", {"builds": builds_paginator})

@csrf_exempt
def like_build(request, build_id):
    """Like a build, unlike if already liked"""
    if request.method == "POST" and request.user.is_authenticated:
        build = Builds.objects.get(id=build_id)
        user = User.objects.get(id=request.user.id)
        if build.likes.filter(user=user).exists():
            count = build.like_count =- 1
            build.likes.remove(user)
            build.save()
        else:
            count = build.like_count =- 1
            build.likes.add(user)
            build.save()
        return HttpResponse(count)