from django.test import TestCase
from django.test.client import Client
from django.db.models import Model, CharField, IntegerField, DateField, get_models, get_app
from hyperdrive.utils import yaml_to_field, get_model_from_config
from django.core.urlresolvers import reverse
from hyperdrive.models import BaseModel
import yaml


class BaseModelTest(TestCase):
    stream = """
            users:
                title: Users
                fields:
                    - {id: name, title: Name, type: char}
                    - {id: paycheck, title: Sallary, type: int}
                    - {id: date_joined, title: Date of joined, type: date}
    """

    def test_yaml_to_field(self):
        """function must correctly determine the type of the field in the configuration file"""
        cf = yaml.load(self.stream, Loader=yaml.Loader)
        fields = cf['users']['fields']
        self.assertIsInstance(yaml_to_field(fields[0]['type']), CharField)
        self.assertIsInstance(yaml_to_field(fields[1]['type']), IntegerField)
        self.assertIsInstance(yaml_to_field(fields[2]['type']), DateField)

    def test_get_model_from_config(self):
        """test function get_model_from_config"""
        raw_data = get_model_from_config(stream=self.stream)
        users = next(raw_data)
        self.assertIsInstance(users['fields']['name'], CharField)
        self.assertIsInstance(users['fields']['date_joined'], DateField)
        self.assertIsInstance(users['fields']['paycheck'], IntegerField)

    def test_create_model(self):
        """function should return the valid django-model"""
        class Users(Model):
            raw_data = get_model_from_config(stream=self.stream)
            data = next(raw_data)
            base = BaseModel()
            model = base.finalize(obj=data)

        self.assertEqual(Users.__name__, 'Users')
        self.assertEqual(Users._meta.verbose_name, 'Users')
        self.assertEqual(len(Users._meta.fields), 4)

class TestViews(TestCase):
    fixtures = ['test_fixture.yaml']

    def test_index_page(self):
        """function should return the status code 200"""
        client = Client()
        response = client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)

    def test_show_model_users(self):
        """function should return the status code 200, the correct content type, content to fill the table"""
        client = Client()
        response = client.get(path=reverse('hyper_data', args=['users']),
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertContains(response, 'fields_name')
        self.assertContains(response, 'items')
        self.assertContains(response, 'model')

    def test_adding_data(self):
        """
        function should be sent to the server using the method post.
        If the data is successfully sent then obtain redirect code 302
        """
        client = Client()
        response = client.post(path=reverse('hyper_form', args=['users']),
                               data={'name': 'Johny Walker',
                                     'paycheck': 3500,
                                     'date_joined': '2014-06-09'})
        self.assertEqual(response.status_code, 302)

    def test_inline_edit_data(self):
        """function should send the modified data to the server and return status code 200"""
        models = get_models(get_app(__name__.split('.')[0]))

        for m in models:
            if m.__name__ == 'Users': model = m

        user = model.objects.all()[0]
        client = Client()
        response = client.post(path=reverse('edit'),
                               data={'model': 'Users',
                                     'obj_id': user.pk,
                                     'field_name': 'paycheck',
                                     'value': 555},
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.content, b'1')
