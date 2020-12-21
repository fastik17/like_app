import requests
from faker import Faker
from faker.providers import internet
import json
import random
import logging

from user_config import UsersConfiguration
fake = Faker()
fake.add_provider(internet)


def get_headers(access):
    return {'Authorization': f'JWT {access}'}


class Bot(object):
    def __init__(self, number_of_users, max_posts_per_user, max_like_per_user, url):
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_like_per_user = max_like_per_user
        self.url = url

    def create_user(self):
        name = fake.name().split(' ', 1)
        data = {'email': fake.email(),
                'password': fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True),
                'first_name': name[0],
                'last_name': name[1]}
        response = requests.post(url=self.url + 'auth/signup/', data=data)
        if response.status_code == 201:
            login_response = requests.post(url=self.url + 'auth/',
                                           data={'email': data.get('email'),
                                                 'password': data.get('password')})
            token_data = json.loads(login_response.content)
            return token_data
        return None

    def token_verify(self, token_data):
        access = token_data.get('access')
        refresh = token_data.get('refresh')
        jwt_verification = requests.post(url=self.url + 'auth/verify/',
                                         headers={
                                         'Authorization': f'JWT {access}'},
                                         data={'token': access})
        if jwt_verification.status_code != 200:
            response = requests.post(url=self.url + 'auth/refresh/',
                                     headers={
                                         'Authorization': f'JWT {refresh}'})
            token_data = json.loads(response.content)
            access = token_data.get('access')
            refresh = token_data.get('refresh')
        return access, refresh

    def create_posts(self, token_data):

        post_counter = 0
        for _ in range(random.randint(1, int(self.max_posts_per_user))):
            post_data = {
                'title': fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None),
                'body': fake.text(max_nb_chars=250, ext_word_list=None)
            }
            access, refresh = self.token_verify(token_data=token_data)
            response = requests.post(url=self.url + 'posts/',
                                     headers={
                                         'Authorization': f'JWT {access}'},
                                     data=post_data)
            if response.status_code == 201:
                post_counter += 1
        return post_counter

    def create_likes(self, token_data):
        access, refresh = self.token_verify(token_data=token_data)

        response = requests.get(url=self.url + 'posts/',
                                headers={'Authorization': f'JWT {access}'})
        likes = json.loads(response.text)
        liked = 0
        id = likes.get('id')
        response = requests.post(url=self.url + f'posts/{id}/like/',
                                 headers={'Authorization': f'JWT {access}'})
        if response.status_code == 401:
            access, refresh = self.token_verify(token_data=token_data)
            requests.post(url=self.url + f'posts/{id}/like/',
                          headers={'Authorization': f'JWT {access}'})
        liked += 1
        return liked


if __name__ == "__main__":

    number_of_users = UsersConfiguration.number_of_users.value
    max_posts_per_user = UsersConfiguration.max_posts_per_user.value
    max_like_per_user = UsersConfiguration.max_like_per_user.value
    url = UsersConfiguration.url.value
    bot = Bot(number_of_users=number_of_users,
              max_posts_per_user=max_posts_per_user,
              max_like_per_user=max_like_per_user,
              url=url)
    posts_counter = 0
    liked_counter = 0
    for _ in range(int(number_of_users)):
        token_data = bot.create_user()
        posts_counter += bot.create_posts(token_data=token_data)
        liked_counter += bot.create_likes(token_data=token_data)

    print(f"{number_of_users} user(s) was(were) created. "
          f"{posts_counter} post(s) was(were) created. "
          f"{liked_counter} like(s) was(were) created.")
