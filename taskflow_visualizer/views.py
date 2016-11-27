from django.http import JsonResponse
from django.shortcuts import render
from taskflow_visualizer.taskflow import get_all_jobs


def index(request):
    return render(request, 'index.html')


def graph(request):
    return render(request, 'graph.html')


def flows(request):
    data = get_all_jobs()
    return JsonResponse(data)
