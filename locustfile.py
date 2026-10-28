from faker import Faker
from locust import HttpUser, task, SequentialTaskSet, TaskSet, constant_throughput
import random

fake = Faker('ru_RU')
# print(fake.address())

class BrowseShop(TaskSet):
    weight = 5

    @task(5)
    def open_home(self):
        self.client.get('/')

    @task(5)
    def open_catalog(self):
        self.client.get('/tovar/')

    @task(5)
    def open_news(self):
        self.client.get('/news/')

    @task(5)
    def open_promotions(self):
        self.client.get('/promotion/')

    @task(5)
    def open_brands(self):
        self.client.get('/brend/')

class RegisterFlow(SequentialTaskSet):
    weight = 1

    def on_start(self):
        response = self.client.get('/registration/')
        self.csrf = response.cookies['csrftoken']

    @task
    def open_registration(self):
        response = self.client.get('/registration/')
        self.csrf = response.cookies['csrftoken']

    @task
    def register_user(self):
        password = 'ZooShop_' + str(fake.random_int(min=100000, max=999999))
        user_data = {
            'username': fake.user_name() + str(fake.random_int(min=100, max=999)),
            'email': fake.email(),
            'password1': password,
            'password2': password,
                'csrfmiddlewaretoken': self.csrf,
        }

        self.client.post('/registration/', data=user_data, headers={
            'X-CSRFToken': self.csrf,
            'Referer': 'http://127.0.0.1:8000/registration/',
        })

class WebsiteUser(HttpUser):
    wait_time = constant_throughput(1)
    tasks = [
        BrowseShop,
        RegisterFlow,
    ]
