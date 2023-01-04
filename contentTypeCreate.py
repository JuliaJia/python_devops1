import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE','DevOpsSystem.settings')
django.setup(set_prefix=False)


from django.contrib.auth.models import ContentType,Permission

ctn = 'cmdb'
mn = 'citype'
cnm = 'can_citype'
pnm = '允许访问CMDB'

ct = ContentType.objects.create(app_label=ctn,model=mn)
permission = Permission.objects.create(
    codename=cnm,
    name=pnm,
    content_type=ct
)

