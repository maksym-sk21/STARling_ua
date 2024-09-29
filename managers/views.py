from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def manager_area(request):
    return render(request, 'managers/manager_area.html')
