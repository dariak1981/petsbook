from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import context
from django.urls import reverse
from django.forms import models as forms_models
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin



class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/'
