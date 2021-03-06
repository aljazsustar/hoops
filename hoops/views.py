from django.shortcuts import render, get_object_or_404, redirect
from . import forms
from .models import Attempt, Practice, BasicStats, WeatherConditions, recalculate_basic_stats, \
    recalculate_basic_stats_on_delete
from .openweather import Weather
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .calculactions import Statistics


@login_required(login_url='/login')
def index(request):
    conditions = Weather(location='ljubljana').get_current_conditions()
    advanced_stats = Statistics(request.user.id)
    practices = Practice.objects.filter(user_id=request.user.id)
    basic_stats = []
    for p in practices:
        if BasicStats.objects.filter(practice_id=p.id).exists():
            stat = BasicStats.objects.get(practice_id=p.id)
        else:
            p.delete()
            continue
        weather = WeatherConditions.objects.get(practice_id=p.id) if WeatherConditions.objects.filter(
            practice_id=p.id).exists() else None
        basic_stats.append({'practice': p, 'basic_stats': stat, 'weather': weather})
        predicted = int(advanced_stats.predict(conditions['wind_speed'], conditions['temp'], conditions['humidity']))
    return render(request, '../templates/index/index.html', {'stats': basic_stats, 'predicted': predicted})


@login_required(login_url='/login')
def practice(request):
    practices = Practice.objects.filter(user_id=request.user.id, date=timezone.now().date())[:1]

    if request.method == 'POST':
        form = forms.PracticeForm(request.POST)

        if form.is_valid():
            attempts = form.cleaned_data['total_shots']
            successful = form.cleaned_data['total_made']
            new_attempt = Attempt(attempts=attempts, attempts_successful=successful)

            if len(practices) == 0:
                new_practice = Practice()
                new_practice.user_id = request.user.id
                new_practice.date = timezone.now().date()
                new_practice.save()
                BasicStats(total_made=successful, total_shots=attempts, practice=new_practice).save()
                new_attempt.practice = new_practice
                new_attempt.save()
                conditions = Weather(location='ljubljana').get_current_conditions()
                weather = WeatherConditions(temperature=conditions['temp'], wind_speed=conditions['wind_speed'],
                                            conditions=conditions['conditions'], humidity=conditions['humidity'],
                                            practice=new_practice)
                weather.save()
            elif practices[0].date != timezone.now().date():
                new_practice = Practice()
                new_practice.user_id = request.user.id
                new_practice.date = timezone.now().date()
                new_practice.save()
                BasicStats(total_made=successful, total_shots=attempts, practice=new_practice).save()
                new_attempt.practice = new_practice
                conditions = Weather(location='ljubljana').get_current_conditions()
                weather = WeatherConditions(temperature=conditions['temp'], wind_speed=conditions['wind_speed'],
                                            conditions=conditions['conditions'], humidity=conditions['humidity'],
                                            practice=new_practice)
                weather.save()
                new_attempt.save()
            else:
                new_attempt.practice = practices[0]
                new_attempt.save()
                recalculate_basic_stats(practices[0].id, new_attempt.pk)

    form = forms.PracticeForm(initial={'total_shots': 10})
    return render(request, '../templates/practice/practice.html', {'form': form})


@login_required(login_url='/login')
def stats(request):
    s = BasicStats.objects.filter(practice__user_id=request.user.id).order_by('practice__date')
    shots_data = []
    percent_data = []
    for stat in s:
        if stat.total_shots == 0:
            stat.delete()
            continue

        date = stat.practice.date
        shots_data.append({
            'x': date.__str__(),
            'y': stat.total_made
        })
        percent_data.append({
            'x': date.__str__(),
            'y': int(round((stat.total_made / stat.total_shots) * 100))
        })
    return render(request, '../templates/stats/stats.html', {'stats': s, 'data': shots_data, 'p_data': percent_data})


@login_required(login_url='/login')
def practice_detail(request, pk):
    p = get_object_or_404(Practice, pk=pk)
    basic_stats = BasicStats.objects.get(practice_id=pk)
    attempts = Attempt.objects.filter(practice_id=pk)
    form = forms.PracticeForm(initial={'total_shots': basic_stats.total_shots, 'total_made': basic_stats.total_made})
    practice_form = forms.EditPracticeForm(initial={'date': p.date})
    data = [a.attempts_successful for a in attempts]
    labels = [i for i in range(1, len(attempts) + 1)]
    js_data = {
        'data': data,
        'labels': labels
    }
    return render(request, '../templates/practice_detail/practice_detail.html',
                  {'form': form, 'practice_form': practice_form,
                   'practice': p, 'basic_stats': basic_stats, 'attempts': attempts, 'js_data': js_data})


@login_required(login_url='/login')
def update_practice(request, pk):
    if request.method == 'POST':
        practice_form = forms.EditPracticeForm(request.POST)

        if practice_form.is_valid():
            p = get_object_or_404(Practice, pk=pk)
            date = practice_form.cleaned_data['date']
            p.date = date
            p.save()
    return redirect('/stats')


@login_required(login_url='/login')
def delete_practice(request, pk):
    to_delete = Practice.objects.get(id=pk, user_id=request.user.id)
    to_delete.delete()
    return redirect('/stats')


@login_required(login_url='/login')
def edit_attempt(request, pk):
    attempt = get_object_or_404(Attempt, pk=pk)

    if request.method == 'POST':
        form = forms.EditAttemptForm(request.POST)
        if form.is_valid():
            attempts = form.cleaned_data['attempts']
            attempts_successful = form.cleaned_data['attempts_successful']
            attempt.attempts_successful = attempts_successful
            attempt.attempts = attempts
            attempt.save()
            recalculate_basic_stats(attempt.practice.pk, attempt.pk)
            return redirect('/')

    form = forms.EditAttemptForm(
        initial={'attempts': attempt.attempts, 'attempts_successful': attempt.attempts_successful})
    return render(request, 'attempt/edit_attempt.html', {'form': form, 'attempt': attempt})


def register(request):
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('hoops:index')

    form = forms.RegistrationForm
    return render(request, 'auth/register.html', {'form': form})


@login_required(login_url='/login')
def logout_request(request):
    logout(request)
    return redirect('hoops:index')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hoops:index')

    form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


@login_required(login_url='/login')
def user_profile(request):
    cities = Weather.get_cities()
    user = User.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = forms.EditUserForm(request.POST)
        if form.is_valid():
            form.save(commit=False)

    form = forms.EditUserForm(initial={'email': user.email, 'username': user.username}, instance=user)
    return render(request, 'user/profile.html', {'cities': cities, 'form': form})


@login_required(login_url='/login')
def delete_attempt(request, pk):
    attempt = get_object_or_404(Attempt, pk=pk)
    to_delete = Attempt.objects.get(id=pk, practice__user_id=request.user.id)
    bs = recalculate_basic_stats_on_delete(to_delete.practice.pk, pk)
    if bs.total_shots == 0:
        p = Practice.objects.filter(user_id=request.user.id, attempt=attempt)
        p.delete()
    to_delete.delete()

    return redirect('/stats')


@login_required(login_url='/login')
def advanced(request):
    advanced_stats = Statistics(request.user.id)
    pearson = Statistics(request.user.id).correlation()[0] \
        if Statistics(request.user.id).correlation()[0] is not None else None

    data = []
    for (w, s) in zip(advanced_stats.wind_speeds, advanced_stats.shots_made):
        data.append({'x': w, 'y': s})
    print(data)
    return render(request, 'stats/advanced.html', {'correlation': pearson, 'data': data})
