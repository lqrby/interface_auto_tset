from django import forms
from django.contrib import admin
from .models import Case
from django.contrib.admin.helpers import ActionForm
# import tablib
from django.http import HttpResponse
from openpyxl import Workbook
from class_api_test import ClassTestCase
from import_export import resources
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from .resources import CaseResource
# from django.db.models import Count, Sum, Min, Max, DateTimeField
# from django.db.models.functions import Trunc

admin.site.site_title = '软件接口自动化测试系统'
admin.site.site_header = '软件接口自动化测试系统'

def get_next_in_date_hierarchy(request, date_hierarchy):
    if date_hierarchy + '__day' in request.GET:
        return 'hour'
    if date_hierarchy + '__month' in request.GET:
        return 'day'
    if date_hierarchy + '__year' in request.GET:
        return 'week'
    return 'month'

@admin.register(Case)
class CaseAdmin(ImportExportModelAdmin):
    actions = ['run_all']
    # 对接资源类
    resource_class = CaseResource
    # 文章列表里显示想要显示的字段
    list_display = ('id','version','url_name',"url","pre_case_id","pre_fields","assert_type","port","parameter_interpretation",'case_number','variable_parameters','request_parameters','interface_status','run',"expect_result",'shortResponse','ispass_color_state','update_time','remark')
    # 满20条数据就自动分页
    list_per_page = 10
    #后台数据列表排序方式,负号表示降序排序
    ordering = ('-update_time',)
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id','version', 'url_name', 'ispass_color_state', 'url',"pre_case_id","pre_fields","parameter_interpretation",'variable_parameters','request_parameters')
    # list_editable 设置默认可编辑字段
    list_editable = ['run','port','remark','interface_status',"expect_result","assert_type"] #"pre_fields",
    # 筛选器
    list_filter = ("whether_version","version","run","pass_or_not",'interface_status')  # 过滤器
    search_fields = ("id","whether_version","url",'case_number',"run","pass_or_not","url_name",'remark')  # 搜索字段
    # 是否显示action选择的个数
    actions_selection_counter = True
    #批量设置是否运行
    def set_run_yes(self, request, queryset):
        queryset.update(run='yes')
    set_run_yes.short_description = '设置运行为:yes'

    def set_run_no(self, request, queryset):
        queryset.update(run='no')
    set_run_no.short_description = '设置运行为:no'

    
    '''选择运行'''
    def run_select(self, request, queryset):
        caseid_list = request.POST.getlist('_selected_action')
        if len(caseid_list) > 0:
            ClassTestCase().runSelectAllCase(caseid_list)
    run_select.short_description = '批量运行'

    def changelist_view(self, request, extra_context=None):
        try:
            action = self.get_actions(request)[request.POST['action']][0]
            action_acts_on_all = action.acts_on_all
        except (KeyError, AttributeError):
            action_acts_on_all = False
        if action_acts_on_all:
            post = request.POST.copy()
            post.setlist(admin.helpers.ACTION_CHECKBOX_NAME, self.model.objects.values_list('id', flat=True))
            request.POST = post
        return super(CaseAdmin, self).changelist_view(request, extra_context)

    '''全部运行'''
    def run_all(self, request, queryset):
        all_list = Case.objects.all().filter(run='yes').filter(interface_status=0)
        if len(all_list) > 0:
            ClassTestCase().runAllCase()
    run_all.acts_on_all = True
    run_all.short_description = '全部运行(all)'
    

    def export_as_excel(self, request, queryset):
        print("queryset",queryset)
        meta = self.model._meta  # 用于定义文件名, 格式为: app名.模型类名
        field_names = [field.name for field in meta.fields]  # 模型所有字段名
        response = HttpResponse(content_type='application/msexcel')  # 定义响应内容类型
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'  # 定义响应数据格式
        wb = Workbook()  # 新建Workbook
        ws = wb.active  # 使用当前活动的Sheet表
        ws.append(field_names)  # 将模型字段名作为标题写入第一行
        for obj in queryset:  # 遍历选择的对象列表
            for myfield in field_names:
                data = [f'{getattr(obj, field)}' for field in field_names]  # 将模型属性值的文本格式组成列表
            ws.append(data)  # 写入模型属性值
        wb.save(response)  # 将数据存入响应内容
        return response

    export_as_excel.short_description = '选择导出Excel'  # 该动作在admin中的显示文字
    actions = (set_run_yes,set_run_no,run_select,export_as_excel,run_all) 


class XForm(ActionForm):
    x_field = forms.CharField()


class YourModelAdmin(admin.ModelAdmin):
    action_form = XForm

    







