from django.shortcuts import render, HttpResponseRedirect, reverse
from buggy.models import Bugs
from buggy.forms import Ticket, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    html = 'index.html'
    New = Bugs.objects.filter(
        Status='New').order_by('-posted')
    In_Progress = Bugs.objects.filter(
        Status='In_Progress').order_by('-posted')
    Done = Bugs.objects.filter(
        Status='Done').order_by('-posted')
    Invalid = Bugs.objects.filter(
        Status='Invalid').order_by('-posted')
    return render(request, html, {
        'New': New,
        'In_progress': In_Progress,
        'Done': Done,
        'Invalid': Invalid
    })


def view_single_ticket(request, id):
    html = 'ticket.html'
    single_ticket = Bugs.objects.filter(id=id)
    return render(request, html, {'single_ticket': single_ticket})


@login_required
def add(request):
    html = 'add.html'
    if request.method == 'POST':
        form = Ticket(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Bugs.objects.create(
                user_ticket_creator=request.user,
                Title=data['Title'],
                Description=data['Description'],
                Status=data['Status']
            )
            return HttpResponseRedirect(reverse('/'))
    form = Ticket()
    return render(request, html, {'form': form})


@login_required
def edit(request, id):
    html = 'edit.html'
    edits = Bugs.objects.get(id=id)
    if request.method == 'POST':
        form = Ticket(request.POST, edits=edits)
        form.save()
        if edits.Status == "Done":
            edits.user_completed_ticket = edits.user_ticket_creator
            edits.user_ticket_creator = None
            form.save()
        elif edits.Status == "Invalid":
            edits.user_ticket_creator = None
            edits.edits.user_completed_ticket = None
            form.save()
        elif edits.Status == "In_Progress":
            edits.user_assigned_ticket = None
            edits.user_assigned_ticket = edits.edits.user_ticket_creator
            edits.user_completed_ticket = None
            form.save()
        elif edits.user_assigned_ticket is not None:
            edits.Status = "In_Progress"
            edits.user_completed_ticket = None
            form.save()
        return HttpResponseRedirect(reverse('/'))
    form = Ticket()
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
                    request.GET.get('next', reverse('/'))
                )
    form = LoginForm()
    return render(request, html, {'form': form})


def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def mainlist(request, id):
    html = 'status.html'
    creator = Bugs.objects.filter(user_ticket_creator=id)
    assigned = Bugs.objects.filter(user_assigned_ticket=id)
    completed = Bugs.objects.filter(user_completed_ticket=id)
    return render(request, html, {
        'Created': creator,
        'Assigned': assigned,
        'Completed': completed
    })
