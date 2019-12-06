from django.shortcuts import render, HttpResponseRedirect, reverse
from buggy.models import Bugs
from buggy.forms import Ticket, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


def index(request):
    html = 'index.html'
    all_tickets = Bugs.objects.all().order_by('posted')
    new = Bugs.objects.filter(
        status='N').order_by('posted')
    in_progress = Bugs.objects.filter(
        status='P').order_by('-posted')
    done = Bugs.objects.filter(
        status='D').order_by('posted')
    invalid = Bugs.objects.filter(
        status='I').order_by('posted')
    return render(request, html, {
        'all_tickets': all_tickets,
        'new': new,
        'in_progress': in_progress,
        'done': done,
        'invalid': invalid
    }
    )


def view_single_ticket(request, id):
    html = 'ticket.html'
    single_ticket = Bugs.objects.filter(id=id)
    return render(request, html, {'single_ticket': single_ticket})


def add(request):
    html = 'add.html'
    if request.method == 'POST':
        form = Ticket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Bugs.objects.create(
                user_ticket_creator=request.user,
                title=data['title'],
                description=data['description'],
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = Ticket()
    return render(request, html, {'form': form})


def edit(request, id):
    html = 'edit.html'
    edits = Bugs.objects.get(id=id)
    if request.method == 'POST':
        form = Ticket(request.POST, initial={
            'title': edits.title,
            'description': edits.description
        })
        if form.is_valid():
            edits.title = form.cleaned_data['title']
            edits.description = form.cleaned_data['description']
            edits.save()
            return HttpResponseRedirect(reverse('homepage'))
    form = Ticket(initial={
        'title': edits.title,
        'description': edits.description
    })
    return render(request, html, {'form': form})


def loginview(request):
    html = 'login.html'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get('next', reverse('homepage'))
                )
    form = LoginForm()
    return render(request, html, {'form': form})


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def mainlist(request, id):
    html = 'status.html'
    user = User.objects.get(pk=id)
    creator = Bugs.objects.filter(user_ticket_creator_id=id)
    assigned = Bugs.objects.filter(user_assigned_ticket_id=id)
    completed = Bugs.objects.filter(user_completed_ticket_id=id)
    return render(request, html, {
        'user': user,
        'created': creator,
        'assigned': assigned,
        'completed': completed
    })
