# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from datetime import datetime
from lagou.settings import SQL_DATETIME_FORMAT


def get_num(text):
    pattern = re.match('.*?(\d+).*', text)
    if pattern:
        nums = int(pattern.group(1))
    else:
        nums = 0
    return nums


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    position_id = scrapy.Field()
    position_name = scrapy.Field()
    company_id = scrapy.Field()
    company_size = scrapy.Field()
    finance_stage = scrapy.Field()
    company_type_list = scrapy.Field()
    skill_labes = scrapy.Field()
    create_time = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    business_zones = scrapy.Field()
    salary = scrapy.Field()
    work_year = scrapy.Field()
    job_nature = scrapy.Field()
    education = scrapy.Field()
    position_advantage = scrapy.Field()
    linestaion = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            insert into lagou_job(position_id, position_name, company_id, company_size, finance_stage, company_type_list, skill_labes,
             create_time, city, district, business_zones, salary, work_year, job_nature, education, position_advantage, linestaion)
             values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)      
        '''
        create_time = datetime.strptime(self['create_time'], SQL_DATETIME_FORMAT)
        #position_id = int(self['position_id'])
        #company_id = int(self['company_id'])
        company_size = get_num(self['company_size'])
        business_zones = ','.join(self['business_zones']) if self['business_zones'] else ''
        linestaion = ''.join(self['linestaion']) if self['linestaion'] else ''
        # skill_lables business_zones linestaion
        params = (self['position_id'], self['position_name'], self['company_id'], company_size, self['finance_stage'], self['company_type_list'],\
                  self['skill_labes'], create_time, self['city'], self['district'], business_zones, self['salary'],\
                  self['work_year'], self['job_nature'], self['education'], self['position_advantage'], linestaion)
        return insert_sql, params