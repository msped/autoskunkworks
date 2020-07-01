from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import (
    ExteriorCategory,
    EngineCategory,
    RunningCategory,
    InteriorCategory,
    Builds,
    Exterior,
    Engine,
    Running,
    Interior
)
from .utils import (
    new_build_content,
    sort_builds_standard,
    sort_builds_users,
    sort_builds_users_public,
    update_build_content
)

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
    user = User.objects.get(id=request.user.id)

    if request.user.id is not build.author.id:
        build.views =+ 1
        build.save()

    user_liked = False
    user_disliked = False

    if request.user.is_authenticated:
        if build.likes.filter(id=request.user.id).exists():
            user_liked = True
        if build.dislikes.filter(id=request.user.id).exists():
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

    builds = sort_builds_standard(sort_by_likes, sort_by_price, sort_by_views)

    paginator = Paginator(builds, 15)
    page = request.GET.get('page')
    builds_paginator = paginator.get_page(page)

    return render(request, "builds.html", {"builds": builds_paginator})

@csrf_exempt
def like_build(request, build_id):
    """Like a build, unlike if already liked"""
    if request.user.is_authenticated:
        build = Builds.objects.get(id=build_id)
        user = User.objects.get(id=request.user.id)
        if build.likes.filter(id=request.user.id).exists():
            build.like_count -= 1
            like_count = build.like_count
            dislike_count = build.dislike_count
            liked = False
            disliked = False
            build.likes.remove(user)
            build.save()
        else:
            if build.dislikes.filter(id=request.user.id).exists():
                if build.dislike_count >= 0:
                    build.dislike_count -= 1
                else: 
                    build.dislike =+ 1
                build.dislikes.remove(user)
            build.like_count =+ 1
            like_count = build.like_count
            dislike_count = build.dislike_count
            liked = True
            disliked = False
            build.likes.add(user)
            build.save()
        return JsonResponse({
            'like_count': like_count,
            'dislike_count': dislike_count,
            'liked': liked,
            'disliked': disliked
        })

@csrf_exempt
def dislike_build(request, build_id):
    """Like a build, unlike if already liked"""
    if request.user.is_authenticated:
        build = Builds.objects.get(id=build_id)
        user = User.objects.get(id=request.user.id)
        if build.dislikes.filter(id=request.user.id).exists():
            build.dislike_count -= 1
            like_count = build.like_count
            dislike_count = build.dislike_count
            disliked = False
            liked = False
            build.dislikes.remove(user)
            build.save()
        else:
            if build.likes.filter(id=request.user.id).exists():
                build.like_count -= 1
                build.likes.remove(user)
            build.dislike_count =+ 1
            like_count = build.like_count
            dislike_count = build.dislike_count
            liked = False
            disliked = True
            build.dislikes.add(user)
            build.save()
        return JsonResponse({
            'like_count': like_count,
            'dislike_count': dislike_count,
            'liked': liked,
            'disliked': disliked
        })

def users_builds(request, username):
    """All of a users build"""
    sort_by_price = request.GET.get('sort_by_price')
    sort_by_likes = request.GET.get('sort_by_likes')
    sort_by_views = request.GET.get('sort_by_views')
    user = User.objects.get(username=username)
    if request.user.id == user.id:
        builds = sort_builds_users(user, sort_by_likes, sort_by_price, sort_by_views)
    else:
        builds = sort_builds_users_public(user, sort_by_likes, sort_by_price, sort_by_views)

    paginator = Paginator(builds, 15)
    page = request.GET.get('page')
    builds_paginator = paginator.get_page(page)

    return render(request, "my_builds.html", {"builds": builds_paginator})

def edit_build(request, build_id):
    """Edit a build"""
    exterior_category = ExteriorCategory.objects.all()
    engine_category = EngineCategory.objects.all()
    running_category = RunningCategory.objects.all()
    interior_category = InteriorCategory.objects.all()
    build = Builds.objects.get(id=build_id)

    if request.method == "POST":
        update_build_content(
            build,
            exterior_category,
            engine_category,
            running_category,
            interior_category,
            request
        )
        return redirect('view_build', build_id)
    context = {
        'exterior': exterior_category,
        'engine': engine_category,
        'running': running_category,
        'interior': interior_category,
        'build': build
    }
    return render(request, "edit.html", context)

@csrf_exempt
def delete_row(request, row_id, table, build_id):
    """Delete row from a build when editing"""
    build = Builds.objects.get(id=build_id)
    if request.method == "POST":
        if table == "exterior-table":
            row = Exterior.objects.get(id=row_id)
            part_price = row.price
            row.delete()
            result = True
        elif table == "engine-table":
            row = Engine.objects.get(id=row_id)
            part_price = row.price
            row.delete()
            result = True
        elif table == "running-gear-table":
            row = Running.objects.get(id=row_id)
            part_price = row.price
            row.delete()
            result = True
        elif table == "interior-table":
            row = Interior.objects.get(id=row_id)
            part_price = row.price
            row.delete()
            result = True
        else:
            result = False
            total = build.total
        if result:
            old_total = build.total
            new_total = old_total - part_price
            build.total = new_total
            build.save()

    deleted = {
        'result': result,
        'total': new_total
    }
    return JsonResponse(deleted)

@login_required
def delete_build(request, build_id):
    """Delete a Build"""
    build = Builds.objects.get(id=build_id)
    if request.user.is_authenticated and request.user.id is build.author.id:
        build.delete()
        messages.success(request, "Build Deleted.")
        return redirect('users_build')
