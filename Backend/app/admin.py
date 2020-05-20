from django.contrib import admin

from .models import (CustomToken, CustomUser, Donation, HelpProgram,
                     Organization, PhoneNumbers)

admin.site.register(CustomUser)
admin.site.register(CustomToken)
admin.site.register(Donation)
admin.site.register(HelpProgram)
admin.site.register(Organization)
admin.site.register(PhoneNumbers)
