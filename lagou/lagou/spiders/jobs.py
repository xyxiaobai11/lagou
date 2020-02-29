# -*- coding: utf-8 -*-
import scrapy
import json
from lagou.items import LagouItem


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['www.lagou.com']
    start_urls = 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput='
    data_urls = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, callback=self.request_data)

    def request_data(self, response):
        for pn in range(1, 10):
            data = {'first': 'true', 'pn': str(pn), 'kd':'python爬虫'}
            yield scrapy.FormRequest(url=self.data_urls, formdata=data)

    def parse(self, response):
        json_data_list = json.loads(response.text)['content']['positionResult']['result']
        if json_data_list:
            for json_data in json_data_list:
                item = LagouItem()
                item['position_id'] = json_data['positionId']
                item['position_name'] = json_data['positionName']
                item['company_id'] = json_data['companyId']
                item['company_size'] = json_data['companySize']
                item['finance_stage'] = json_data['financeStage']
                first_type = json_data['firstType']
                second_type = json_data['secondType']
                third_type = json_data['thirdType']
                item['company_type_list'] = first_type.replace('|', ',')+','+second_type.replace('|', ',')+','+third_type.replace('|', ',')
                item['skill_labes'] = ','.join(json_data['skillLables'])
                item['create_time'] = json_data['createTime']
                item['city'] = json_data['city']
                item['district'] = json_data['district']
                item['business_zones'] = json_data['businessZones']
                item['salary'] = json_data['salary']
                item['work_year'] = json_data['workYear']
                item['job_nature'] = json_data['jobNature']
                item['education'] = json_data['education']
                item['position_advantage'] = json_data['positionAdvantage']
                item['linestaion'] = json_data['linestaion']
                yield item
