from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect
from django.http import HttpResponse

from cursed import NewsModel
from cursed import ClusterElementModel

from django.contrib.auth.models import User #Здесь все юзеры, тa модель нах не нужна
from django.contrib import auth
from django.contrib.auth import logout as django_logout
from django.template import Context, loader


def all_news(request):
    news_list = NewsModel.get_news()
    return render(request, 'all_news.html', locals())


def cluster_els(request):
    elem_list = ClusterElementModel.get_ordered_elements()
    for el in elem_list:
        print(el.title + " ----- " + str(el.cluster))
    news_list = []
    return render(request, 'all_news.html', locals())


def cluster(request, cluster):
    elements = ClusterElementModel.get_elements_by_cluster(cluster)

    titles = [e.title for e in elements]
    news_list = NewsModel.get_news_by_title(titles)
    print(len(news_list))
    return render(request, 'all_news.html', locals())
