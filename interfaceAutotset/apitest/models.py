from base64 import encode
from django.db import models
import django.utils.timezone as timezone
from django.contrib import admin
from django.contrib.auth.models import User 
from django.utils.html import format_html
from django import forms


class Case(models.Model):
    """
    # 测试用例
    """
    whether_version_choices = (
        (0, '版本'),
        (1, '活动'),
        (2, '其它'),
    )
    whether_version = models.IntegerField('是否版本', default=0, choices=whether_version_choices)
    version = models.CharField('版本名称', max_length=50,default='未知')
    url_name = models.CharField('接口名称', max_length=50,default='未知接口名称')

    domain_or_ipaddress = models.CharField('域名或IP地址',default="http://123.57.42.55", max_length=100, blank=False, null=True)

    port_choices = (
        (20100, '20100'),
        (20010, '20010'),
        (20020, '20020'),
        (20800, '20800'),
        (8080, '8080'),
        (0, '无'),
    )
    port = models.IntegerField('端口', default=0, choices=port_choices)

    url = models.CharField('请求地址(url)',default='', max_length=512)

    headers = models.TextField(verbose_name='headers请求头', default='', blank=True, null=True)

    method_choices = (
        ('post', 'POST'),
        ('get', 'GET'),
    )
    method = models.CharField('请求方法', default='post', max_length=10, choices=method_choices)

    pre_case_id = models.IntegerField('前置用例(id)',default=0)
    
    pre_fields = models.TextField('前置字段', default='[]', max_length=512,blank=True, null=True)

    case_number = models.CharField('用例编号', max_length=32,blank=True, null=True )

    parameter_interpretation = models.TextField('参数释意', max_length=512,blank=True, null=True)

    variable_parameters = models.TextField('变动参数', max_length=512,blank=True, null=True)

    request_parameters = models.TextField('请求参数',default="")

    interfaceStatus = (
        (0, '正常'),
        (1, '已关闭'),
        (2, '已废弃'),
        (3, '预留'),
    )
    interface_status = models.IntegerField('接口状态',default=0, choices=interfaceStatus)

    run_choices = (
        ('yes', '是'),
        ('no', '否'),
    )
    run = models.CharField('是否运行', default="yes", max_length=4, choices=run_choices )

    assert_choices = (
        (0, '无'),
        (1, 'options'),
        (2, 'options_item'),
        (3, 'options_list'),
        (4, 'options_item_list'),
    )
    assert_type = models.IntegerField('断言类型', choices=assert_choices,default=0)

    expect_result = models.CharField('预期结果',default="", max_length=256, blank=True, null=True)

    response = models.TextField('响应数据', default="",max_length=1024, blank=True, null=True)

    def shortResponse(self):
        return str(self.response)[:150]
    shortResponse.short_description = '响应数据'
    
    pass_choices = (
        (0, '未知'),
        (1, '通过'),
        (2, '不通过'),
    )
    pass_or_not = models.IntegerField('测试结果', default=0, choices=pass_choices,blank=True,null=True)

    def ispass_color_state(self):
        if self.pass_or_not == 1:
            assign_state_name = '通过'
            color_code = 'green'
        elif self.pass_or_not == 2:
            color_code = 'yellow' #'red'
            assign_state_name = '不通过'
        else:
            color_code = '#9D9D9D'
            assign_state_name = '未知'
            
        return format_html(
            '<span style="color:{};">{}</span>',
            color_code,
            assign_state_name,
        )
    ispass_color_state.short_description = '测试结果'
    
    update_time = models.DateTimeField('更新时间', auto_now=True)
    
    remark = models.CharField('备注', max_length=100, default="", blank=True, null=True)
    
    class Meta:
        verbose_name = '测试用例表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.url_name)













    
    
    

    
