# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import PBKDF2PasswordHasher


class CustomPBKDF2PasswordHasher(PBKDF2PasswordHasher):
    iterations = PBKDF2PasswordHasher.iterations * 50
