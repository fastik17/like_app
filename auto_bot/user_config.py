from enum import Enum


class UsersConfiguration(Enum):
    number_of_users = 4
    max_posts_per_user = 4
    max_like_per_user = 2
    url = 'http://127.0.0.1:8000/v1/'
