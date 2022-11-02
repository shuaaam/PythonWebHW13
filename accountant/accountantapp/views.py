from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from datetime import datetime
from .models import Category, Actions, User
from django.db.models import Sum
from .forms import CategoryForm, ActionsForm

# Create your views here.
def main(request):
    actions = Actions.objects.order_by('-added').all()[:10]
    balance = Actions.objects.aggregate(balance=Sum('sum'))
    return render(request, 'accountantapp/index.html', {'Last transactions': actions, 'Balance': balance['balance']})


@login_required
def new_category(request):
    if request.method == 'POST':
        name = request.POST['name']
        if name:
            category = Category(name=name)
            category.save()
        return redirect(to='/')
    return render(request, 'accountantapp/new_category.html', {})


@login_required
def new_action(request):
    if request.method == 'POST':
        ac_sum = request.POST['sum']
        type = request.POST['type']
        if type == "0":
           ac_sum = 0 - int(ac_sum)
        category_name = request.POST['category']
        if ac_sum and type:
            category = Category.objects.get(name=category_name)
            action = Actions(sum=ac_sum, type=type, category=category)
            action.save()
        return redirect(to='/')

    categories = Category.objects.all()
    return render(request, 'accountantapp/new_action.html', {"categories": categories})


@login_required
def detail(request):
    if request.GET.get('datetime_from', False) and request.GET.get('datetime_to', False):
        actions = Actions.objects.filter(
            created_at__range=[request.GET['datetime_from'], request.GET['datetime_to']])
        balance = 0
        income = 0
        spendings = 0
        if actions:
            for action in actions:
                balance = balance + int(action.sum)
                if action.type is True:
                    income = income + int(action.sum)
                elif action.type is False:
                    spendings = spendings + int(action.sum) * -1
        return render(request, 'accountantapp/detail.html',
                      {'actions': actions,
                       'datetime_to': datetime.strptime(request.GET['datetime_to'], '%Y-%m-%dT%H:%M'),
                       'datetime_from': datetime.strptime(request.GET['datetime_from'], '%Y-%m-%dT%H:%M'), 'balance': balance,
                       'income': income,
                       'spendings': spendings})

    return render(request, 'accountantapp/detail.html', {'datetime_to': request.GET.get('datetime_to', False),
                                                              'datetime_from': request.GET.get('datetime_from', False)})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'accountantapp/signup.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                return redirect('loginuser')
            except IntegrityError as err:
                return render(request, 'accountantapp/signup.html',
                              {'form': UserCreationForm(), 'error': 'Username already exist!'})

        else:
            return render(request, 'accountantapp/signup.html',
                          {'form': UserCreationForm(), 'error': 'Password did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'accountantapp/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'accountantapp/login.html',
                          {'form': AuthenticationForm(), 'error': 'Username or password didn\'t match'})
        login(request, user)
        return redirect('main')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('main')