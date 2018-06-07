# -*- coding: utf-8 -*-
import scrapy
from cursed import NewsModel

from dateutil import parser


def scrap_notebook(request):
        title = request.css('.news-full__title ::text').extract_first()
        views = request.css('.icon-views ::text').extract_first()
        if views[len(views) - 1] == 'т':
            views = views.replace('т', '0')
            views = float(views) * 1000
        published = request.css('.news-full__date ::text').extract_first()
        text = ''.join(request.css('.news-full__text p::text').extract())
        link = request.css('.btn-printer ::attr(href)').extract_first()
        NewsModel.add_news(title, link, text, parse_date(published), views)


class ObozSpider(scrapy.Spider):
    name = 'oboz'
    start_urls = ['https://www.obozrevatel.com']

    def parse(self, response):
        archive_day = response.meta.get("archive_day")
        archive_month = response.meta.get("archive_month")
        if archive_day is None or archive_month is None:
            archive_day = 1
            archive_month = 5
        elif archive_day == 31:
            archive_day = 1
            archive_month += 1
        elif archive_day == 5 and archive_month == 6:
            return

        if archive_day < 10:
            archive_day = '0' + str(archive_day)
        if archive_month < 10:
            archive_month = '0' + str(archive_month)

        curr_link = 'https://www.obozrevatel.com/archive/' + str(archive_day) + "-" + str(archive_month) + "-2018.htm"
        req = scrapy.Request(url=curr_link)
        req.meta['archive_day'] = int(archive_day) + 1
        req.meta['archive_month'] = int(archive_month)
        yield req
        for sub_link in response.css('.news-title-img-text__title ::attr(href)'):
            yield response.follow(sub_link.extract(), callback=scrap_notebook)


def parse_date(date):
    date_list = date.split(' ')
    month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
           'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    month = month_list.index(date_list[1]) + 1
    if month < 10:
        month = '0' + str(month)
    date = date.replace(date_list[1], str(month))
    return parser.parse(date)