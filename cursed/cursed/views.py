from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect
from django.http import HttpResponse

from cursed import NewsModel

import plotly
import plotly.graph_objs as go
from django.contrib.auth.models import User #Здесь все юзеры, тa модель нах не нужна
from django.contrib import auth
from django.contrib.auth import logout as django_logout
from django.template import Context, loader
from datetime import timedelta, date


def all_news(request):
    news_list = NewsModel.get_news()
    return render(request, 'all_news.html', locals())


def cluster(request, cluster):
    news_list = NewsModel.get_news_by_cluster(cluster)
    list_for2 = NewsModel.get_list_for_plot_by_date_with_cluster(cluster)
    dates = []
    for i in range(1,30):
        dates.append(date.today() - timedelta(days=i))
    trace2 = go.Bar(
        x=dates,
        y=list_for2,
        name='dates'
    )
    data2 = [trace2]
    layout = go.Layout(
        barmode='group'
    )
    fig2 = go.Figure(data=data2, layout=layout)
    div2 = plotly.offline.plot(fig2, show_link=False, auto_open=False, output_type='div')

    return render(request, 'all_news.html', locals())


def last_week(request):
    news_list = NewsModel.get_last_week()
    return render(request, 'news_by_date.html', locals())


def last_month(request):
    news_list = NewsModel.get_last_month()
    return render(request, 'news_by_date.html', locals())


def graph_count(request):
    list_for = NewsModel.get_list_for_plot_by_count()
    cluster = []
    for i in range(200):
        cluster.append(i)
    trace1 = go.Bar(
        x=cluster,
        y=list_for,
        name='clusters'
    )
    data = [trace1]
    layout = go.Layout(
        barmode='group'
    )
    fig = go.Figure(data=data, layout=layout)
    div = plotly.offline.plot(fig, show_link=False, auto_open=False, output_type='div')


    list_for2 = NewsModel.get_list_for_plot_by_date()
    dates = []
    for i in range(1,30):
        dates.append(date.today() - timedelta(days=i))
    trace2 = go.Bar(
        x=dates,
        y=list_for2,
        name='dates'
    )
    data2 = [trace2]
    fig2 = go.Figure(data=data2, layout=layout)
    div2 = plotly.offline.plot(fig2, show_link=False, auto_open=False, output_type='div')

    list_for3 = NewsModel.get_list_for_plot_by_views()

    trace3 = go.Bar(
        x=cluster,
        y=list_for3,
        name='dates'
    )
    data3 = [trace3]
    fig3 = go.Figure(data=data3, layout=layout)
    div3 = plotly.offline.plot(fig3, show_link=False, auto_open=False, output_type='div')

    return render(request, 'plot.html', locals())