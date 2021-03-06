#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Django settings for NakServer project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g^4)0h@ir_n!azd^wh8*+p6*y1#uvsjd%d4lzyv_egwyj^$hi_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH=False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Nak',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'NakServer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'NakServer.wsgi.application'

# DATABASE_NAME = '/opt/datebase/vote.db'
# DATABASE_NAME = 'vote.db'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'naksoft',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST':'localhost',
        'PORT': '3306',
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': DATABASE_NAME,
#         'USER': '',
#         'PASSWORD': '',
#         'HOST':'',
#         'PORT': '',
#     }
# }

DATABASE_NAME = '/opt/datebase/vote.db'
# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases



# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# HERE = os.path.dirname(os.path.dirname(__file__))
# MEDIA_ROOT = os.path.join(HERE, 'static/').replace('\\', '/')
# MEDIA_URL = '/static/'


# STATIC_ROOT 表示资源的根目录路径
# STATIC_URL 表示资源的访问url
# STATICFILES_DIRS 表示子资源的访问url和目录

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'HsEdu')
STATIC_ROOT = os.path.join(STATIC_ROOT, 'static')


TempDir = os.path.join(os.getcwd(), 'Nak')
TEMPLATE_DIRS = [os.path.join(TempDir, 'templates'),]
print "TEMPLATE_DIRS",TEMPLATE_DIRS
# STATICFILES_DIRS = (
#     # Put strings here, like "/home/html/static" or "C:/www/django/static".
#     # Always use forward slashes, even on Windows.
#     # Don't forget to use absolute paths, not relative paths.
#     os.path.join(HERE,'static').replace('\\','/'),
# )

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = False
# EMAIL_HOST = 'smtp.qq.com'
# EMAIL_PORT = 995
# EMAIL_HOST_USER = '609853524@qq.com'
# EMAIL_HOST_PASSWORD = 'caojj_123'
# DEFAULT_FROM_EMAIL = '609853524@qq.com'

#邮件配置
EMAIL_HOST = 'smtp.qq.com'                   #SMTP地址
EMAIL_PORT = 465                               #SMTP端口
EMAIL_HOST_USER = '609853524@qq.com'        #我自己的邮箱
EMAIL_HOST_PASSWORD = 'caojj_123'            #我的邮箱密码
EMAIL_SUBJECT_PREFIX = u'[Test Mail]'        #为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True                           #与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
#管理员站点
SERVER_EMAIL = '609853524@qq.com'       #The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
 
