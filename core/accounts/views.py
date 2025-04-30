from django.shortcuts import render
from django.http import HttpResponse
import time
from accounts.tasks import sendEmail
from django.views.decorators.cache import cache_page

def send_email(request):
    sendEmail.delay()
    return HttpResponse("<h1>Done sending</h1>")

# @cache_page(60)