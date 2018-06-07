from mongoengine import *


class NewsModel(Document):
    title = StringField(min_length=3, required=True, unique=True)
    link = URLField(verify_exists=True, required=True)
    text = StringField(min_length=100, required=True)
    published = DateTimeField(required=True)
    views = IntField(min_value=0, required=True)

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