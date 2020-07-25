from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from .models import *

def create_build_id():
    """Create random build id and check if already in db or not"""
    build_id = get_random_string(length=16, allowed_chars=('abcdefghijklmnopqrstuvwxyz' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))

    if Builds.objects.filter(build_id=build_id).exists():
        while not Builds.objects.filter(build_id=build_id).exists():
            build_id = get_random_string(length=16, allowed_chars=('abcdefghijklmnopqrstuvwxyz' 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
    return build_id

def check_visibility(user_input):
    if user_input == "Public":
        private = False
    else:
        private = True
    return private

def convert_purchased(checkbox_input):
    if checkbox_input == "on":
        purchased = True
    else:
        purchased = False
    return purchased

def create_car(request):
    car = Cars.objects.create(
        make=request.POST.get('make'),
        model=request.POST.get('model'),
        trim=request.POST.get('trim'),
        year=request.POST.get('year'),
        price=float(request.POST.get('price'))
    )
    return car
            
def get_heading_contents_exterior(request, heading):
    heading_ids = []
    for item in heading:
        heading_model = ExteriorCategory.objects.get(id=item.id)
        link = request.POST.get('exterior_' + str(item.id) + '_link')
        if link is not None:
            purchased = convert_purchased(request.POST.get('exterior_' + str(item.id) + '_purchased'))
            part = Exterior.objects.create(
                exterior_category=heading_model,
                link=link,
                price=float(request.POST.get('exterior_' + str(item.id) + '_price')),
                purchased=purchased
            )
            part.save()
            heading_ids.append(part.id)
    return heading_ids

def get_heading_contents_engine(request, heading):
    heading_ids = []
    for item in heading:
        heading_model = EngineCategory.objects.get(id=item.id)
        link = request.POST.get('engine_' + str(item.id) + '_link')
        if link is not None:
            purchased = convert_purchased(request.POST.get('engine_' + str(item.id) + '_purchased'))
            part = Engine.objects.create(
                engine_category=heading_model,
                link=link,
                price=float(request.POST.get('engine_' + str(item.id) + '_price')),
                purchased=purchased
            )
            part.save()
            heading_ids.append(part.id)
    return heading_ids

def get_heading_contents_running(request, heading):
    heading_ids = []
    for item in heading:
        heading_model = RunningCategory.objects.get(id=item.id)
        link = request.POST.get('running_' + str(item.id) + '_link')
        if link is not None:
            purchased = convert_purchased(request.POST.get('running_' + str(item.id) + '_purchased'))
            part = Running.objects.create(
                running_category=heading_model,
                link=link,
                price=float(request.POST.get('running_' + str(item.id) + '_price')),
                purchased=purchased
            )
            part.save()
            heading_ids.append(part.id)
    return heading_ids

def get_heading_contents_interior(request, heading):
    heading_ids = []
    for item in heading:
        heading_model = InteriorCategory.objects.get(id=item.id)
        link = request.POST.get('interior_' + str(item.id) + '_link')
        if link is not None:
            purchased = convert_purchased(request.POST.get('interior_' + str(item.id) + '_purchased'))
            part = Interior.objects.create(
                interior_category=heading_model,
                link=link,
                price=float(request.POST.get('interior_' + str(item.id) + '_price')),
                purchased=purchased
            )
            part.save()
            heading_ids.append(part.id)
    return heading_ids

def new_build_content(request, exterior_category, engine_category,
                      running_category, interior_category):
    user = User.objects.get(id=request.user.id)
    private = check_visibility(request.POST.get('visibility'))
    price_hidden = check_visibility(request.POST.get('price-visibility'))
    car = create_car(request)
    gen_build_id = create_build_id()
    
    build = Builds.objects.create(
        build_id=gen_build_id,
        author=user,
        name=request.POST.get('build_name'),
        total=float(request.POST.get('total')),
        private=private,
        price_hidden=price_hidden,
        car=car
    )

    # Add Author to liked list
    build.likes.add(user)
    
    # Adds exterior collection to record
    exterior = get_heading_contents_exterior(request, exterior_category)
    if exterior is not None:
        for item in exterior:
            part = Exterior.objects.get(id=item)
            build.exterior_parts.add(part)

    # Adds Engine collection to record
    engine = get_heading_contents_engine(request, engine_category)
    if engine is not None:
        for item in engine:
            part = Engine.objects.get(id=item)
            build.engine_parts.add(part)

    # Adds Running Gear collection to record
    running = get_heading_contents_running(request, running_category)
    if running is not None:
        for item in running:
            part = Running.objects.get(id=item)
            build.running_gear_parts.add(part)

    # Adds Interior collection to record
    interior = get_heading_contents_interior(request, interior_category)
    if interior is not None:
        for item in interior:
            part = Interior.objects.get(id=item)
            build.interior_parts.add(part)
    build.save()
    return build.build_id

def update_heading_contents_exterior(request, heading):
    new_heading_ids = []
    for item in heading:
        link = request.POST.get('exterior_' + str(item.id) + '_link')
        price = request.POST.get('exterior_' + str(item.id) + '_price')
        if link is not None:
            purchased = convert_purchased(request.POST.get('exterior_' + str(item.id) + '_purchased'))
            part, created = Exterior.objects.get_or_create(
                exterior_category=item,
                defaults={
                    'link':link,
                    'price': float(price),
                    'purchased':purchased 
                }
            )
            if created:    
                part.save()
                new_heading_ids.append(part.id)
            elif not created and part.link is not link or park.price is not price or part.purchased is not purchased:
                part.link = link
                part.price = float(price)
                part.purchased = purchased
                part.save()
    return new_heading_ids

def update_heading_contents_engine(request, heading):
    new_heading_ids = []
    for item in heading:
        link = request.POST.get('engine_' + str(item.id) + '_link')
        price = request.POST.get('engine_' + str(item.id) + '_price')
        if link is not None:
            purchased = convert_purchased(request.POST.get('engine_' + str(item.id) + '_purchased'))
            part, created = Engine.objects.get_or_create(
                engine_category=item,
                defaults={
                    'link':link,
                    'price': float(price),
                    'purchased':purchased 
                }
            )
            if created:    
                part.save()
                new_heading_ids.append(part.id)
            elif not created and part.link is not link or park.price is not price or part.purchased is not purchased:
                part.link = link
                part.price = float(price)
                part.purchased = purchased
                part.save()
    return new_heading_ids

def update_heading_contents_running(request, heading):
    new_heading_ids = []
    for item in heading:
        link = request.POST.get('running_' + str(item.id) + '_link')
        price = request.POST.get('running_' + str(item.id) + '_price')
        if link is not None:
            purchased = convert_purchased(request.POST.get('running_' + str(item.id) + '_purchased'))
            part, created = Running.objects.get_or_create(
                running_category=item,
                defaults={
                    'link':link,
                    'price': float(price),
                    'purchased':purchased 
                }
            )
            if created:    
                part.save()
                new_heading_ids.append(part.id)
            elif not created and part.link is not link or park.price is not price or part.purchased is not purchased:
                part.link = link
                part.price = float(price)
                part.purchased = purchased
                part.save()
    return new_heading_ids

def update_heading_contents_interior(request, heading):
    new_heading_ids = []
    for item in heading:
        link = request.POST.get('interior_' + str(item.id) + '_link')
        price = request.POST.get('interior_' + str(item.id) + '_price')
        if link is not None:
            purchased = convert_purchased(request.POST.get('interior_' + str(item.id) + '_purchased'))
            part, created = Interior.objects.get_or_create(
                interior_category=item,
                defaults={
                    'link':link,
                    'price': float(price),
                    'purchased':purchased 
                }
            )
            if created:    
                part.save()
                new_heading_ids.append(part.id)
            elif not created and part.link is not link or park.price is not price or part.purchased is not purchased:
                part.link = link
                part.price = float(price)
                part.purchased = purchased
                part.save()
    return new_heading_ids

def update_car(request, build):
    car = Cars.objects.get(id=build.car.id)
    car.make = request.POST.get('make')
    car.model = request.POST.get('model')
    car.trim = request.POST.get('trim')
    car.year = request.POST.get('year')
    car.price = float(request.POST.get('price'))
    car.save()

def update_build_content(build, exterior, engine, running, interior, request):
    if float(request.POST.get('total')) is not build.total:
        build.total = float(request.POST.get('total'))
    private = check_visibility(request.POST.get('visibility'))
    if private is not build.private:
        build.private = private
    price_hidden = check_visibility(request.POST.get('price-visibility'))
    if price_hidden is not build.price_hidden:
        build.price_hidden = price_hidden
    car = update_car(request, build)
    # Adds exterior collection to record
    new_exterior = update_heading_contents_exterior(request, exterior)
    if new_exterior is not None:
        for item in new_exterior:
            part = Exterior.objects.get(id=item)
            build.exterior_parts.add(part)

    # Adds Engine collection to record
    new_engine = update_heading_contents_engine(request, engine)
    if new_engine is not None:
        for item in new_engine:
            part = Engine.objects.get(id=item)
            build.engine_parts.add(part)

    # Adds Running Gear collection to record
    running = update_heading_contents_running(request, running)
    if running is not None:
        for item in running:
            part = Running.objects.get(id=item)
            build.running_gear_parts.add(part)

    # Adds Interior collection to record
    interior = update_heading_contents_interior(request, interior)
    if interior is not None:
        for item in interior:
            part = Interior.objects.get(id=item)
            build.interior_parts.add(part)
    build.save()

def sort_builds_standard(sort_options):
    if sort_options is not None:
        builds = Builds.objects.filter(private=False).order_by(sort_options)
    else:
        builds = Builds.objects.filter(private=False)

    return builds

def sort_builds_users(user, sort_options):
    if sort_options is not None:
        builds = Builds.objects.filter(author=user).order_by(sort_options)
    else:
        builds = Builds.objects.filter(author=user)

    return builds

def sort_builds_users_public(user, sort_options):

    if sort_options is not None:
        builds = Builds.objects.filter(author=user, private=False).order_by(sort_options)
    else:
        builds = Builds.objects.filter(author=user, private=False)

    return builds

def delete_manytomany_relations(build):
    """Delete all manytomany in tables"""
    for items in build.exterior_parts.all():
        item.delete()
    for items in build.engine_parts.all():
        item.delete()
    for items in build.running_gear_parts.all():
        item.delete()
    for items in build.interior_parts.all():
        item.delete()