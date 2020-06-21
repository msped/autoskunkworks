from django.contrib.auth.models import User
from .models import *

def votes(user_email, build_votes):
    if user_email in build_votes:
        return True
    return False

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
        heading_model = ExteriorCategory.objects.get(id=item.id)
        link = request.POST.get('engine_' + str(item.id) + '_link')
        if link is not None:
            purchased = convert_purchased(request.POST.get('engine_' + str(item.id) + '_purchased'))
            part = Engine.objects.create(
                exterior_category=heading_model,
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
        heading_model = ExteriorCategory.objects.get(id=item.id)
        link = request.POST.get('running_' + str(item.id) + '_link')
        if link is not None:
            purchased = convert_purchased(request.POST.get('running_' + str(item.id) + '_purchased'))
            part = Running.objects.create(
                exterior_category=heading_model,
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
        heading_model = ExteriorCategory.objects.get(id=item.id)
        link = request.POST.get('interior_' + str(item.id) + '_link')
        if link is not None:
            purchased = convert_purchased(request.POST.get('interior_' + str(item.id) + '_purchased'))
            part = Interior.objects.create(
                exterior_category=heading_model,
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

    car = create_car(request)
    
    build = Builds.objects.create(
        author=user,
        name=request.POST.get('build_name'),
        total=float(request.POST.get('total')),
        private=private,
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

def update_build_content(exterior, engine, running, interior, request):

    record = {
        'total': float(request.form.get('total')),
        'visibility': request.form.get('visibility'),
        'car': {
            'make': request.form.get('make'),
            'model': request.form.get('model'),
            'trim': request.form.get('trim'),
            'year': request.form.get('year'),
            'price': float(request.form.get('price'))
        },
    }

    # Adds exterior collection to record
    record.update({'exterior': get_heading_contents(request, exterior,
                                                    'exterior_')})

    # Adds Engine collection to record
    record.update({'engine': get_heading_contents(request, engine,
                                                  'engine_')})

    # Adds Running Gear collection to record
    record.update({'running': get_heading_contents(request, running,
                                                   'running_')})

    # Adds Interior collection to record
    record.update({'interior': get_heading_contents(request, interior,
                                                    'interior_')})

    return record
