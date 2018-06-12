from mongoengine import *
from datetime import date
from datetime import timedelta, datetime
#import  cursed.cursed.settings

class NewsModel(Document):
    title = StringField(min_length=3, required=True)
    link = URLField(verify_exists=True, required=True)
    text = StringField(min_length=100, required=True)
    published = DateTimeField(required=True)
    views = IntField(min_value=0, required=True)
    cluster = IntField(min_value=0, max_value = 200)

    @property
    def to_dict(self):
        data = {
            'title': self.title,
            'link': self.link,
            'text': self.text,
            'published': self.published,
            'views': self.views
        }
        return data

    def __str__(self):
        return self.title


def add_news(title, link, text, published, views):
    news = NewsModel()

    exist = NewsModel.objects(title=title)

    if exist:
        print("THIS NEWS ALREADY EXIST")
        return

    if title is None or link is None or text is None or published is None or views is None:
        return
    news.title = title
    news.link = link
    news.text = text
    news.published = published
    news.views = views

    news.save()


def get_news():
    return NewsModel.objects()


def get_news_by_title(title):
    return NewsModel.objects.filter(title__in=title)


def update_news_with_cluster(object, cluster):
    object.update(**{"set__cluster" : cluster})

def get_news_by_cluster(cluster):
    return NewsModel.objects(cluster=cluster).order_by("-views")


def get_last_week():
    date_N_days_ago = date.today() - timedelta(days=7)
    return NewsModel.objects(Q(published__gte=date_N_days_ago)&Q(published__lte=date.today())).order_by('-views').limit(30)


def get_last_month():
    date_N_days_ago = date.today() - timedelta(days=31)
    return NewsModel.objects(Q(published__gte=date_N_days_ago)&Q(published__lte=date.today())).order_by('-views').limit(30)


def get_list_for_plot_by_count():
    result = []
    for i in range(0,200):
        result.append(NewsModel.objects(cluster=i).count())
    return result

def get_list_for_plot_by_views():
    result = []
    for i in range(0,200):
        result.append(NewsModel.objects(cluster=i).sum('views'))
    return result


def get_list_for_plot_by_date():
    result = []
    for i in range(1, 31):
        date_N_days_ago = date.today() - timedelta(days=i)
        date_Nminus1_days_ago = date_N_days_ago - timedelta(days=1)
        result.append(NewsModel.objects(Q(published__gte=date_Nminus1_days_ago)&Q(published__lte=date_N_days_ago)).count())
    return result


def get_list_for_plot_by_date_with_cluster(cluster):
    result = []
    for i in range(1, 31):
        date_N_days_ago = date.today() - timedelta(days=i)
        date_Nminus1_days_ago = date_N_days_ago - timedelta(days=1)
        result.append(NewsModel.objects(Q(published__gte=date_Nminus1_days_ago)&Q(published__lte=date_N_days_ago)&Q(cluster=cluster)).count())
    return result