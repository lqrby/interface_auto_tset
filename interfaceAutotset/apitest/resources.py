
from import_export import resources
from .models import Case
class CaseResource(resources.ModelResource):
    class Meta:
        model = Case
        skip_unchanged = True   
        report_skipped = False
        import_id_fields = ('case_number',)
        fields=[
            'id',
            'whether_version',
            'version',
            'url_name',
            'domain_or_ipaddress',
            'port',
            "url",
            'method',
            'pre_case_id',
            'pre_fields',
            'assert_type',
            'case_number',
            "parameter_interpretation",
            'variable_parameters',
            'request_parameters',
            "expect_result",
            'pass_or_not',
            'remark',
        ]
        excloud = (
            'headers',
            'interface_status',
            'run',
            'response',
            'update_time',
        )

        
        
