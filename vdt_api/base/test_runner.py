from django.test.runner import DiscoverRunner
from django.core.management import call_command

class CustomTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # Chạy migrate trước khi thiết lập database cho test
        call_command('migrate')
        return super().setup_databases(**kwargs)