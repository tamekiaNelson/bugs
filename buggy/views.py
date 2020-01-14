from django.shortcuts import render, HttpResponseRedirect, reverse
from buggy.models import Bug
from buggy.forms import Ticket, LoginForm, EditTicket
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    html = 'index.html'
    New = Bug.objects.filter(
        status='New').order_by('-posted')
    In_Progress = Bug.objects.filter(
        status='In_Progress').order_by('-posted')
    Done = Bug.objects.filter(
        status='Done').order_by('-posted')
    Invalid = Bug.objects.filter(
        status='Invalid').order_by('-posted')
    return render(request, html, {
        'New': New,
        'In_Progress': In_Progress,
        'Done': Done,
        'Invalid': Invalid
    })


@login_required
def view_single_ticket(request, id):
    html = 'ticket.html'
    single_ticket = Bug.objects.filter(id=id)
    return render(request, html, {'single_ticket': single_ticket})


@login_required
def add(request):
    html = 'add.html'
    if request.method == 'POST':
        form = Ticket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Bug.objects.create(
                user_ticket_creator=request.user,
                title=data['title'],
                description=data['description'],
                status='New'
            )
            return HttpResponseRedirect(reverse('homepage'))
    form = Ticket()
    return render(request, html, {'form': form})


@login_required
def edit(request, id):
    html = 'edit.html'
    edits = Bug.objects.get(id=id)
    if request.method == 'POST':
        form = EditTicket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['status'] == "Done":
                edits.user_assigned_ticket = None
                edits.user_completed_ticket = edits.user_ticket_creator
                form.save()
            elif data['status'] == "Invalid":
                edits.user_assigned_ticket = None
                edits.user_completed_ticket = None
                form.save()
            elif data['status'] == "In_Progress":
                edits.user_assigned_ticket = edits.user_assigned_ticket
                edits.user_completed_ticket = None
                form.save()
            elif data['status'] == "New":
                edits.status = "New"
                edits.user_completed_ticket = None
                edits.user_assigned_ticket = None
                form.save()
        return HttpResponseRedirect(reverse('homepage'))
    form = EditTicket(instance=edits)
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
    return HttpResponseRedirect(reverse('login'))


def mainlist(request, id):
    html = 'status.html'
    creator = Bug.objects.filter(user_ticket_creator=id)
    assigned = Bug.objects.filter(user_assigned_ticket=id)
    completed = Bug.objects.filter(user_completed_ticket=id)
    return render(request, html, {
        'Created': creator,
        'Assigned': assigned,
        'Completed': completed
    })
