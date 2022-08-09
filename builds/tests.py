import json
from django.test import TestCase
from .models import *
from .utils import *
from .views import *

# Create your tests here.

# Models 
class BuildTests(TestCase):
    """Test Builds App"""

    # Set Up
    def setUp(self):
        # User
        self.user = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'mspe',
            'email': 'test@gmail.com',
            'password': 'testpassword'
        }
        User.objects.create_user(**self.user)
        ExteriorCategory.objects.create(
            title="Sideskirts",
            name="sideskirts"
        )
        EngineCategory.objects.create(
            title="Exhaust",
            name="exhuast"
        )
        RunningCategory.objects.create(
            title="Wheels",
            name="wheels"
        )
        InteriorCategory.objects.create(
            title="Steering Wheel",
            name="steering_wheel"
        )
        ex_cat = ExteriorCategory.objects.create(
            title="Front Splitter",
            name="front_splitter"
        )
        en_cat = EngineCategory.objects.create(
            title="Remap",
            name="remap"
        )
        ru_cat = RunningCategory.objects.create(
            title="Suspension",
            name="suspension"
        )
        in_cat = InteriorCategory.objects.create(
            title="Harness",
            name="harness"
        )
        Exterior.objects.create(
            exterior_category=ex_cat,
            link='https://carbonwurks.com/shop/exterior/a-class-front-spoiler-extension/',
            price=595.00,
            purchased=True
        )
        Engine.objects.create(
            engine_category=en_cat,
            link='https://www.ebay.co.uk/p/552299957?iid=123190033794&chn=ps&norover=1&mkevt=1&mkrid=710-134428-41853-0&mkcid=2&itemid=123190033794&targetid=909243431449&device=c&mktype=pla&googleloc=1007242&poi=&campaignid=10195651607&mkgroupid=107296279612&rlsatarget=aud-629407027585:pla-909243431449&abcId=1145985&merchantid=7398324&gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zkvDbECip8gnYYYB0idBJnMMNWsLkAU-YrzfCv_4uYdH7rJC-snPUYaAplZEALw_wcB',
            price=849.99,
            purchased=False
        )
        Running.objects.create(
            running_category=ru_cat,
            link='https://www.ebay.co.uk/itm/48-230971-Bilstein-B16-PSS-Coilover-Kit-For-Mercedes-A-Class-12-W176/362936026458?fits=Plat_Gen%3AW176&epid=5013641733&hash=item5480ac455a:g:fWwAAOSwbHpdzQto',
            price=1374.37,
            purchased=False
        )
        Interior.objects.create(
            interior_category=in_cat,
            link='https://www.nickygrist.com/turn-one-6-point-harness?gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zk1hYxZwwU5cFC6Y8EC1L4wJU1uvVCXhhcJ9gFRMdp48FqC7kWGOtAaAiRxEALw_wcB',
            price=119.94,
            purchased=False
        )
        Cars.objects.create(
            make='Mercedes',
            model='A Class',
            trim='A250',
            year='2013',
            price=12500,
            purchased=True
        )
        # create build
        user = User.objects.get(username="mspe")
        ex = Exterior.objects.all().first()
        en = Engine.objects.all().first()
        ru = Running.objects.all().first()
        inte = Interior.objects.all().first()
        car = Cars.objects.all().first()
        build = Builds.objects.create(
            build_id=create_build_id(),
            author=user,
            name="Test",
            price_hidden=False,
            total=1000,
            private=False,
            car=car
        )
        build.exterior_parts.add(ex)
        build.engine_parts.add(en)
        build.running_gear_parts.add(ru)
        build.interior_parts.add(inte)
        build.likes.add(user)

    # ExteriorCategory
    def test_exterior_category_model(self):
        response = ExteriorCategory(
            title="Front Splitter",
            name="front_splitter"
        )
        response.save()
        self.assertEqual(response.title, 'Front Splitter')
        self.assertEqual(response.name, 'front_splitter')
        self.assertEqual(str(response), 'Front Splitter')

    # EngineCategory
    def test_engine_category_model(self):
        response = EngineCategory(
            title="Remap",
            name="remap"
        )
        response.save()
        self.assertEqual(response.title, 'Remap')
        self.assertEqual(response.name, 'remap')
        self.assertEqual(str(response), 'Remap')

    # RunningCategory
    def test_running_category_model(self):
        response = RunningCategory(
            title="Suspension",
            name="suspension"
        )
        response.save()
        self.assertEqual(response.title, 'Suspension')
        self.assertEqual(response.name, 'suspension')
        self.assertEqual(str(response), 'Suspension')

    # InteriorCategory
    def test_interior_category_model(self):
        response = InteriorCategory(
            title="Harness",
            name="harness"
        )
        response.save()
        self.assertEqual(response.title, 'Harness')
        self.assertEqual(response.name, 'harness')
        self.assertEqual(str(response), 'Harness')

    # Domains
    def test_domains_model(self):
        """Test domains model plus str"""
        d = Domains(
            domain='ebay',
            price_element='prcIsum',
            attr='1'
        )

        self.assertEqual(d.domain, 'ebay')
        self.assertEqual(d.price_element, 'prcIsum')
        self.assertEqual(d.attr, '1')
        self.assertEqual(str(d), 'ebay')

    # Exterior
    def test_exterior(self):
        """Test exterior"""
        category = ExteriorCategory.objects.all().first()
        exterior = Exterior(
            exterior_category=category,
            link='https://carbonwurks.com/shop/exterior/a-class-front-spoiler-extension/',
            price=595.00,
            purchased=True
        )
        exterior.save()
        self.assertEqual(exterior.link, 'https://carbonwurks.com/shop/exterior/a-class-front-spoiler-extension/')
        self.assertEqual(exterior.price, 595.00)
        self.assertTrue(exterior.purchased)

    # Engine
    def test_engine(self):
        """Test engine"""
        category = EngineCategory.objects.all().first()
        engine = Engine(
            engine_category=category,
            link='https://www.ebay.co.uk/p/552299957?iid=123190033794&chn=ps&norover=1&mkevt=1&mkrid=710-134428-41853-0&mkcid=2&itemid=123190033794&targetid=909243431449&device=c&mktype=pla&googleloc=1007242&poi=&campaignid=10195651607&mkgroupid=107296279612&rlsatarget=aud-629407027585:pla-909243431449&abcId=1145985&merchantid=7398324&gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zkvDbECip8gnYYYB0idBJnMMNWsLkAU-YrzfCv_4uYdH7rJC-snPUYaAplZEALw_wcB',
            price=849.99,
            purchased=False
        )
        engine.save()
        self.assertEqual(engine.link, 'https://www.ebay.co.uk/p/552299957?iid=123190033794&chn=ps&norover=1&mkevt=1&mkrid=710-134428-41853-0&mkcid=2&itemid=123190033794&targetid=909243431449&device=c&mktype=pla&googleloc=1007242&poi=&campaignid=10195651607&mkgroupid=107296279612&rlsatarget=aud-629407027585:pla-909243431449&abcId=1145985&merchantid=7398324&gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zkvDbECip8gnYYYB0idBJnMMNWsLkAU-YrzfCv_4uYdH7rJC-snPUYaAplZEALw_wcB')
        self.assertEqual(engine.price, 849.99)
        self.assertFalse(engine.purchased)

    # Running
    def test_running(self):
        """Test running"""
        category = RunningCategory.objects.all().first()
        running = Running(
            running_category=category,
            link='https://www.ebay.co.uk/itm/48-230971-Bilstein-B16-PSS-Coilover-Kit-For-Mercedes-A-Class-12-W176/362936026458?fits=Plat_Gen%3AW176&epid=5013641733&hash=item5480ac455a:g:fWwAAOSwbHpdzQto',
            price=1374.37,
            purchased=False
        )
        running.save()
        self.assertEqual(running.link, 'https://www.ebay.co.uk/itm/48-230971-Bilstein-B16-PSS-Coilover-Kit-For-Mercedes-A-Class-12-W176/362936026458?fits=Plat_Gen%3AW176&epid=5013641733&hash=item5480ac455a:g:fWwAAOSwbHpdzQto')
        self.assertEqual(running.price, 1374.37)
        self.assertFalse(running.purchased)

    # Interior
    def test_interior(self):
        """Test interior"""
        category = InteriorCategory.objects.all().first()
        interior = Interior(
            interior_category=category,
            link='https://www.nickygrist.com/turn-one-6-point-harness?gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zk1hYxZwwU5cFC6Y8EC1L4wJU1uvVCXhhcJ9gFRMdp48FqC7kWGOtAaAiRxEALw_wcB',
            price=119.94,
            purchased=False
        )
        interior.save()
        self.assertEqual(interior.link, 'https://www.nickygrist.com/turn-one-6-point-harness?gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zk1hYxZwwU5cFC6Y8EC1L4wJU1uvVCXhhcJ9gFRMdp48FqC7kWGOtAaAiRxEALw_wcB')
        self.assertEqual(interior.price, 119.94)
        self.assertFalse(interior.purchased)

    # Cars
    def test_car_model(self):
        """Test car model"""
        car = Cars(
            make='Mercedes',
            model='A Class',
            trim='A250',
            year=2013,
            price=12500,
            purchased=True
        )
        car.save()
        self.assertEqual(car.make, 'Mercedes')
        self.assertEqual(car.model, 'A Class')
        self.assertEqual(car.trim, 'A250')
        self.assertEqual(car.year, 2013)
        self.assertEqual(car.price, 12500)
        self.assertTrue(car.purchased)
        self.assertEqual(str(car), 'Mercedes A Class A250')

    # Builds
    def test_builds_model(self):
        """Test builds model"""
        user = User.objects.get(username="mspe")
        ex = Exterior.objects.all().first()
        en = Engine.objects.all().first()
        ru = Running.objects.all().first()
        inte = Interior.objects.all().first()
        car = Cars.objects.all().first()
        build = Builds.objects.create(
            build_id=create_build_id(),
            author=user,
            name="Test 2",
            price_hidden=False,
            total=1000,
            private=False,
            car=car
        )
        build.exterior_parts.add(ex)
        build.engine_parts.add(en)
        build.running_gear_parts.add(ru)
        build.interior_parts.add(inte)
        build.likes.add(user)

        self.assertEqual(build.author.username, user.username)
        self.assertEqual(build.name, "Test 2")
        self.assertFalse(build.price_hidden)
        self.assertEqual(build.total, 1000)
        self.assertFalse(build.private)
        self.assertEqual(build.car.make, 'Mercedes')
        self.assertEqual(build.car.model, 'A Class')
        self.assertEqual(build.car.trim, 'A250')
        self.assertEqual(build.car.year, 2013)
        self.assertEqual(build.car.price, 12500)
        self.assertTrue(build.car.purchased)
        self.assertTrue(build.exterior_parts.get(pk=ex.id), ex)
        self.assertTrue(build.engine_parts.get(pk=en.id), en)
        self.assertTrue(build.running_gear_parts.get(pk=ru.id), ru)
        self.assertTrue(build.interior_parts.get(pk=inte.id), inte)
        self.assertEqual(str(build), 'Test 2')
        self.assertEqual(build.like_count, 1)
        self.assertTrue(build.likes.get(pk=user.id), user)

    # Create Build Get
    def test_create_page_response_not_logged_in(self):
        """Test create page response while not logged in, should be 302"""
        response = self.client.get('/builds/create/')
        self.assertEqual(response.status_code, 302)

    def test_create_page_response_logged_in(self):
        """Test create page response while logged in, should be 200"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/builds/create/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>Create a new plan</h1>', response.content)

    # Create Build Post
    def test_create_build_post(self):
        """Test post of data through create page, should redirect to view page"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        data = {
            'build_name': 'mspeTest',
            'total': 1000.00,
            'private': "off",
            'price_hidden': "off",
            'make': 'Mercedes',
            'model': 'A Class',
            'trim': 'A250',
            'year': '2013',
            'price': 12500,
            'car_purchased': "on",
            'exterior_1_link': 'https://carbonwurks.com/shop/exterior/a-class-front-spoiler-extension/',
            'exterior_1_price': 595.00,
            'exterior_1_purchased': "off",
            'engine_1_link': 'https://www.ebay.co.uk/p/552299957?iid=123190033794&chn=ps&norover=1&mkevt=1&mkrid=710-134428-41853-0&mkcid=2&itemid=123190033794&targetid=909243431449&device=c&mktype=pla&googleloc=1007242&poi=&campaignid=10195651607&mkgroupid=107296279612&rlsatarget=aud-629407027585:pla-909243431449&abcId=1145985&merchantid=7398324&gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zkvDbECip8gnYYYB0idBJnMMNWsLkAU-YrzfCv_4uYdH7rJC-snPUYaAplZEALw_wcB',
            'engine_1_price': '1000',
            'engine_1_purchased': "on",
            'running_1_link': 'https://www.ebay.co.uk/itm/48-230971-Bilstein-B16-PSS-Coilover-Kit-For-Mercedes-A-Class-12-W176/362936026458?fits=Plat_Gen%3AW176&epid=5013641733&hash=item5480ac455a:g:fWwAAOSwbHpdzQto',
            'running_1_price': 295.00,
            'running_1_purchased': "off",
            'interior_1_link': 'https://www.nickygrist.com/turn-one-6-point-harness?gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zk1hYxZwwU5cFC6Y8EC1L4wJU1uvVCXhhcJ9gFRMdp48FqC7kWGOtAaAiRxEALw_wcB',
            'interior_1_price': 500.00,
            'interior_1_purchased': "off"
        }
        result = self.client.post(
            '/builds/create',
            data=data,
            follow=True
        )
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<h1> mspeTest</h1>' , result.content)

    # Builds Get
    def test_builds_page_response(self):
        """Test builds page response, should be 200"""
        response = self.client.get('/builds/')
        self.assertEqual(response.status_code, 200)

    # Edit Build Get
    def test_edit_page_response_logged_in(self):
        """Test response of edit page while logged in, should return 200"""
        build = Builds.objects.all().first()
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.get('/builds/edit/'+str(build.build_id) + '/')
        self.assertEqual(response.status_code, 200)

    def test_edit_page_response_not_logged_in(self):
        """Test response of edit page while not logged in, should return 302"""
        build = Builds.objects.all().first()
        response = self.client.get(
            '/builds/edit/'+str(build.build_id) + '/'
        )
        self.assertEqual(response.status_code, 302)

    # Edit Build Post
    def test_update_build_post(self):
        """Test Post data for updating a build"""
        build = Builds.objects.get(name='Test')
        interior = Interior.objects.get(
            link='https://www.nickygrist.com/turn-one-6-point-harness?gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zk1hYxZwwU5cFC6Y8EC1L4wJU1uvVCXhhcJ9gFRMdp48FqC7kWGOtAaAiRxEALw_wcB',
            price=119.94,
        )
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.post(
            '/builds/edit/' + build.build_id,
            {
                'total': 750.00, # changed
                'private': "off",
                'price_hidden': "off",
                'make': 'Mercedes',
                'model': 'B Class',
                'trim': 'A250',
                'year': '2013',
                'price': 12500,
                'car_purchased': "on",
                'exterior_1_link': 'https://carbonwurks.com/shop/exterior/a-class-front-spoiler-extension/',
                'exterior_1_price': 595.00,
                'exterior_1_purchased': "off",
                'engine_1_link': 'https://www.ebay.co.uk/p/552299957?iid=123190033794&chn=ps&norover=1&mkevt=1&mkrid=710-134428-41853-0&mkcid=2&itemid=123190033794&targetid=909243431449&device=c&mktype=pla&googleloc=1007242&poi=&campaignid=10195651607&mkgroupid=107296279612&rlsatarget=aud-629407027585:pla-909243431449&abcId=1145985&merchantid=7398324&gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zkvDbECip8gnYYYB0idBJnMMNWsLkAU-YrzfCv_4uYdH7rJC-snPUYaAplZEALw_wcB',
                'engine_1_price': '1000',
                'engine_1_purchased': "on",
                'running_1_link': 'https://www.ebay.co.uk/itm/48-230971-Bilstein-B16-PSS-Coilover-Kit-For-Mercedes-A-Class-12-W176/362936026458?fits=Plat_Gen%3AW176&epid=5013641733&hash=item5480ac455a:g:fWwAAOSwbHpdzQto',
                'running_1_price': 295.00,
                'running_1_purchased': "off",
                'interior_1_link': 'https://www.nickygrist.com/turn-one-6-point-harness?gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zk1hYxZwwU5cFC6Y8EC1L4wJU1uvVCXhhcJ9gFRMdp48FqC7kWGOtAaAiRxEALw_wcB',
                'interior_1_price': 500.00,
                'interior_1_purchased': "off"
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<td>\n                            B Class\n', response.content)
        self.assertIn(b'Total Price: <strong>750.0</strong>', response.content)

    def test_update_build_new_headings(self):
        """Test Post data for updating a build with new headings"""
        build = Builds.objects.get(name='Test')
        new_ex = ExteriorCategory.objects.get(title='Sideskirts')
        new_en = EngineCategory.objects.get(title='Exhaust')
        new_ru = RunningCategory.objects.get(title='Wheels')
        new_in = InteriorCategory.objects.get(title='Steering Wheel')
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.post(
            '/builds/edit/' + build.build_id,
            {
                'total': 750.00,
                'private': "off",
                'price_hidden': "off",
                'make': 'Mercedes',
                'model': 'B Class',
                'trim': 'A250',
                'year': '2013',
                'price': 12500,
                'car_purchased': "on",
                'exterior_1_link': 'https://carbonwurks.com/shop/exterior/a-class-front-spoiler-extension/',
                'exterior_1_price': 595.00,
                'exterior_1_purchased': "off",
                'engine_1_link': 'https://www.ebay.co.uk/p/552299957?iid=123190033794&chn=ps&norover=1&mkevt=1&mkrid=710-134428-41853-0&mkcid=2&itemid=123190033794&targetid=909243431449&device=c&mktype=pla&googleloc=1007242&poi=&campaignid=10195651607&mkgroupid=107296279612&rlsatarget=aud-629407027585:pla-909243431449&abcId=1145985&merchantid=7398324&gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zkvDbECip8gnYYYB0idBJnMMNWsLkAU-YrzfCv_4uYdH7rJC-snPUYaAplZEALw_wcB',
                'engine_1_price': 1000,
                'engine_1_purchased': "on",
                'running_1_link': 'https://www.ebay.co.uk/itm/48-230971-Bilstein-B16-PSS-Coilover-Kit-For-Mercedes-A-Class-12-W176/362936026458?fits=Plat_Gen%3AW176&epid=5013641733&hash=item5480ac455a:g:fWwAAOSwbHpdzQto',
                'running_1_price': 295.00,
                'running_1_purchased': "off",
                'interior_1_link': 'https://www.nickygrist.com/turn-one-6-point-harness?gclid=Cj0KCQjwpZT5BRCdARIsAGEX0zk1hYxZwwU5cFC6Y8EC1L4wJU1uvVCXhhcJ9gFRMdp48FqC7kWGOtAaAiRxEALw_wcB',
                'interior_1_price': 500.00,
                'interior_1_purchased': "off",

                'exterior_'+ str(new_ex.id) +'_link': 'https://carbonwurks.com/shop/exterior/acla-class-carbon-fibre-side-skirt-extensions/',
                'exterior_'+ str(new_ex.id) +'_price': 100.00,
                'exterior_'+ str(new_ex.id) +'_purchased': "off",
                'engine_'+ str(new_en.id) +'_link': 'https://clptuning.co.uk/product/remus-cat-back-exhaust-mercedes-a45cla45-amg/',
                'engine_'+ str(new_en.id) +'_price': 1000,
                'engine_'+ str(new_en.id) +'_purchased': "on",
                'running_'+ str(new_ru.id) +'_link': 'https://www.wheelbasealloys.com/alloy-wheels/ava/hsf-013/gun-metal/20-inch-wider-rear/mercedes/c-class-amg/c63s',
                'running_'+ str(new_ru.id) +'_price': 100.00,
                'running_'+ str(new_ru.id) +'_purchased': "off",
                'interior_'+ str(new_in.id) +'_link': 'https://carbonwurks.com/shop/interior/audi-r8-carbon-fibre-steering-wheel/',
                'interior_'+ str(new_in.id) +'_price': 100.00,
                'interior_'+ str(new_in.id) +'_purchased': "off"

            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'https://carbonwurks.com/shop/exterior/acla-class-carbon-fibre-side-skirt-extensions/', response.content)
        self.assertIn(b'https://clptuning.co.uk/product/remus-cat-back-exhaust-mercedes-a45cla45-amg/', response.content)
        self.assertIn(b'https://www.wheelbasealloys.com/alloy-wheels/ava/hsf-013/gun-metal/20-inch-wider-rear/mercedes/c-class-amg/c63s', response.content)
        self.assertIn(b'https://carbonwurks.com/shop/interior/audi-r8-carbon-fibre-steering-wheel/', response.content)

    # View Build Get
    def test_view_page_response(self):
        """Test response of view page"""
        build = Builds.objects.all().first()
        response = self.client.get('/builds/'+ str(build.build_id) + '/')
        self.assertEqual(response.status_code, 200)

    # Like a build liked before
    def like_a_build_liked_already(self):
        """Liking a build already liked should remove the like"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        build = Builds.objects.get(name="Test")
        response = self.client.get('/builds/like/' + str(build.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {
                'like_count': 0,
                'dislike_count': 0,
                'liked': False,
                'disliked': False
            }
        )
    
    # Like a Build Not liked before
    def like_build_not_liked(self):
        """Test reponse on liking a build not liked before"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        build = Builds.objects.get(name="Test")
        response = self.client.get('/builds/like/' + str(build.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {
                'like_count': 1,
                'dislike_count': 0,
                'liked': True,
                'disliked': False
            }
        )
        
    # # Dislike a build where already liked
    def dislike_a_build_where_already_liked(self):
        """Dislike a build where already liked"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        build = Builds.objects.get(name="Test")
        build.like_count = 1
        response = self.client.get('/builds/dislike/' + str(build.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {
                'like_count': 0,
                'dislike_count': 1,
                'liked': False,
                'disliked': True
            }
        )
    
    # Dislike a build disliked before
    def dislike_build_disliked_before(self):
        """Dislike a build already disliked"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        build = Builds.objects.get(name="Test")
        response = self.client.get('/builds/dislike/' + str(build.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {
                'like_count': 0,
                'dislike_count': 0,
                'liked': False,
                'disliked': False
            }
        )
        
    # Dislike a Build Not disliked before
    def dislike_a_build_not_disliked(self):
        """dislike a build not disliked before"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        build = Builds.objects.get(name="Test")
        response = self.client.get('/builds/dislike/' + str(build.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {
                'like_count': 0,
                'dislike_count': 1,
                'liked': False,
                'disliked': True
            }
        )

    # Like a build where already disliked
    def like_a_build_already_disliked(self):
        """like a build already disliked"""
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        build = Builds.objects.get(name="Test")
        response = self.client.get('/builds/like/' + str(build.id) + '/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding="utf8"),
            {
                'like_count': 1,
                'dislike_count': 0,
                'liked': True,
                'disliked': False
            }
        )

    # Run like and dislike test in certain order
    def test_like_dislike_routes_in_order(self):
        self.like_a_build_liked_already()
        self.like_build_not_liked()
        self.dislike_a_build_where_already_liked()
        self.dislike_build_disliked_before()
        self.dislike_a_build_not_disliked()
        self.like_a_build_already_disliked()

    # Delete Build
    def delete_build_not_logged_in(self):
        """Test delete a build while not logged in, should return 302"""
        build = Builds.objects.get(name="Test")
        response = self.client.get('/builds/delete/'+ str(build.id) + '/')
        self.assertEqual(response.status_code, 302)

    def delete_build_logged_in(self):
        """Test delete a build while not logged in, should return 200"""
        build = Builds.objects.get(name="Test")
        self.client.post(
            '/user/login/',
            self.user,
            follow=True
        )
        response = self.client.get(
            '/builds/delete/'+ str(build.id) + '/',
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Build Deleted.',
            response.content
        )
    
    def test_delete_views(self):
        self.delete_build_not_logged_in()
        self.delete_build_logged_in()

    # Get Web Price
    def test_get_web_price_id(self):
        """Test Get Web Price by id"""
        Domains.objects.create(
            domain='ebay',
            price_element='prcIsum',
            attr='1'
        )
        response = self.client.post(
            '/builds/get-web-price/',
            {
                'url': 'https://www.ebay.co.uk/itm/GENUINE-A45-AMG-Rear-Diffuser-Sport-Edition-Mercedes-Benz-W176-A-Class-NEW/132794845019?epid=23008548439&hash=item1eeb30875b:g:D1MAAOSwx-9WvwlE'
            }
        )
        self.assertIn(b'214.96', response.content)

    def test_get_web_price_class(self):
        """Test Get Web Price by class"""
        Domains.objects.create(
            domain='throtl',
            price_element='price-item--regular',
            attr='2'
        )
        response = self.client.post(
            '/builds/get-web-price/',
            {
                'url': 'https://throtl.com/products/air-lift-performance-15-20-mercedes-c-class-w205-c63-a-78580'
            }
        )
        self.assertIn(b'1195.00', response.content)

    def test_get_web_price_no_domain(self):
        """Test Get Web Price no domain stored"""
        Domains.objects.create(
            domain='carid',
            price_element='prod-price',
            attr='2'
        )
        response = self.client.post(
            '/builds/get-web-price/',
            {
                'url': 'https://carbonwurks.com/shop/exterior/a-class-front-spoiler-extension/'
            }
        )
        self.assertIn(b'0', response.content)

    # Check Visibility Public 
    def test_check_visibility_public(self):
        """Test check_visibility when input is public, should return False"""
        response = check_visibility("Public")
        self.assertFalse(response)

    # Check Visibility Private 
    def test_check_visibility_private(self):
        """Test check_visibility when input is private, should return True"""
        response = check_visibility("Private")
        self.assertTrue(response)

    # Convert Purchase On
    def test_convert_purchased_on(self):
        """Test convert_purchased when input is on, should return True"""
        response = convert_purchased("on")
        self.assertTrue(response)

    # Convert Purchase Off
    def test_convert_purchased_off(self):
        """Test convert_purchased when input is off, should return False"""
        response = convert_purchased("off")
        self.assertFalse(response)

    # get_heading_contents_exterior

    # get_heading_contents_engine

    # get_heading_contents_running 

    # get_heading_contents_interior

    # new build content

    # update_heading_contents_exterior

    # update_heading_contents_engine

    # update_heading_contents_running 

    # update_heading_contents_interior

    # update car

    # update build content 