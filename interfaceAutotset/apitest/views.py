from django.shortcuts import render
from .admin import CaseResource
from tablib import Dataset
from utils.db_util import MysqlDbUtil
from django.http import HttpResponse
from decimal import Decimal, ROUND_HALF_UP
import json
from django.views.decorators.cache import cache_page

def simple_upload(request):
    if request.method == 'POST':
        person_resource = CaseResource()
        dataset = Dataset()
        # print('dataset===',dataset)
        new_persons = request.FILES['myfile']
        imported_data = dataset.load(new_persons.read())
        imported_data.remove(imported_data[0])
        # print("imported_data===",imported_data)
        result = person_resource.import_data(imported_data, dry_run=True)  # Test the data import
        if not result.has_errors():
            person_resource.import_data(imported_data, dry_run=False)  # Actually import now
    return render(request, 'core/simple_upload.html')

# @cache_page(0)
def apitest(request):
    return render(request,'apitest/index.html')

# @cache_page(0)
def getdata(request):
    sql = """SELECT aa.version, aa.url_name,count( * ) AS 'case_number',cc.cnt AS 'pass',dd.cnt AS 'fail',bb.cnt AS 'unexecuted' FROM apitest_case aa INNER JOIN (SELECT a.version,
        a.url_name,ifnull( b.cnt, 0 ) AS cnt FROM apitest_case a LEFT JOIN ( SELECT url_name, count( * ) cnt FROM apitest_case WHERE pass_or_not = 0 GROUP BY url_name ) b ON 
        a.url_name = b.url_name GROUP BY a.url_name ) bb ON aa.url_name = bb.url_name INNER JOIN (SELECT a.version,a.url_name,ifnull( b.cnt, 0 ) AS cnt FROM apitest_case a
        LEFT JOIN ( SELECT url_name, count( * ) cnt FROM apitest_case WHERE pass_or_not = 1 GROUP BY url_name ) b ON a.url_name = b.url_name GROUP BY a.url_name ) cc ON 
        aa.url_name = cc.url_name INNER JOIN (SELECT a.version,a.url_name,ifnull( b.cnt, 0 ) AS cnt FROM apitest_case a LEFT JOIN ( SELECT url_name, count( * ) cnt FROM 
        apitest_case WHERE pass_or_not = 2 GROUP BY url_name ) b ON a.url_name = b.url_name GROUP BY a.url_name ) dd ON aa.url_name = dd.url_name GROUP BY aa.url_name """
    result = MysqlDbUtil().query(sql)
    # print(result)
    testResponsArr = []
    for res in result:
        passing_rate = res['pass'] / res['case_number'] * 100
        passingRate = Decimal(passing_rate).quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)
        res['passingRate'] = str(passingRate) + "%"
        failure_rate = res['fail'] / res['case_number'] * 100
        failureRate = Decimal(failure_rate).quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)
        res['failureRate'] = str(failureRate) + "%"
        completion_rate = (res['pass'] + res['fail']) / res['case_number'] * 100
        completionRate = Decimal(completion_rate).quantize(Decimal("0.00"), rounding = ROUND_HALF_UP)
        res['completionRate'] = str(completionRate) + "%"
        # print(res)
        testResponsArr.append(res)
    datalist = {
        "total": 3,
        "rows": testResponsArr
    }
    return HttpResponse(json.dumps(datalist))
