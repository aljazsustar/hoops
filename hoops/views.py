from django.shortcuts import render, get_object_or_404, redirect
from . import forms
from .models import Attempt, Practice, BasicStats
from django.utils import timezone
from datetime import datetime


def index(request):
    return render(request, '../templates/index/index.html')


def practice(request):
    practices = Practice.objects.order_by('-date')[:1]
    basic_stats = BasicStats.objects.order_by('-practice__date')[:1]

    if request.method == 'POST':
        form = forms.PracticeForm(request.POST)

        if form.is_valid():
            attempts = form.cleaned_data['total_shots']
            successful = form.cleaned_data['total_made']
            new_attempt = Attempt(attempts=attempts, attempts_successful=successful)

            if len(practices) == 0:
                new_practice = Practice()
                new_practice.save()
                BasicStats(total_made=successful, total_shots=attempts, practice=new_practice).save()
                new_attempt.practice = new_practice
            elif practices[0].date != timezone.now().date():
                new_practice = Practice()
                new_practice.save()
                BasicStats(total_made=successful, total_shots=attempts, practice=new_practice).save()
                new_attempt.practice = new_practice
            else:
                new_attempt.practice = practices[0]
                bs = basic_stats[0]
                bs.total_made += successful
                bs.total_shots += attempts
                bs.save()

            new_attempt.save()
    form = forms.PracticeForm(initial={'total_shots': 10})
    return render(request, '../templates/practice/practice.html', {'form': form})


def stats(request):
    s = BasicStats.objects.all()
    shots_data = []

    for stat in s:
        date = stat.practice.date
        shots_data.append({
            'x': date.__str__,
            'y': stat.total_made
        })
    return render(request, '../templates/stats/stats.html', {'stats': s, 'data': shots_data})


def practice_detail(request, pk):
    p = get_object_or_404(Practice, pk=pk)
    b_raw = BasicStats.objects.filter(practice_id=pk)
    basic_stats = b_raw[0]
    form = forms.PracticeForm(initial={'total_shots': basic_stats.total_shots, 'total_made': basic_stats.total_made})
    practice_form = forms.EditPracticeForm(initial={'date': p.date})
    return render(request, '../templates/practice_detail/practice_detail.html',
                  {'form': form, 'practice_form': practice_form,
                   'practice': p})


def update_practice(request, pk):

    if request.method == 'POST':
        attempts_form = forms.PracticeForm(request.POST)
        practice_form = forms.EditPracticeForm(request.POST)

        if attempts_form.is_valid() and practice_form.is_valid():
            p = get_object_or_404(Practice, pk=pk)
            shots_made = attempts_form.cleaned_data['total_made']
            shots_total = attempts_form.cleaned_data['total_shots']
            date = practice_form.cleaned_data['date']
            basic_stats_raw = BasicStats.objects.filter(practice_id=p.id)

            basic_stats = basic_stats_raw[0]
            basic_stats.total_shots = shots_total
            basic_stats.total_made = shots_made
            basic_stats.save()

            p.date = date
            p.save()
    return redirect('/stats')
