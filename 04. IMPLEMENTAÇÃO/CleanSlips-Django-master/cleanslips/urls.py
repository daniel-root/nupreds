from django.urls import path
from cleanslips import views

urlpatterns = [
    path(r'campus=<campus>&template=<template>', views.upload, name='uplink'),
    path(r'', views.home, name='uplink'),
    path(r'find', views.find, name='uplink'),
    path(r'home', views.home, name='uplink'),
    path(r'docs', views.docs, name='uplink'),
    path(r'contact', views.contact, name='uplink'),
]