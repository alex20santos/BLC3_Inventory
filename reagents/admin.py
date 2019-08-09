from django.contrib import admin

# Register your models here.
from reagents.models import ReagentGroup, Reagent, OutputMovementReagent, InputMovementReagent

admin.site.register(ReagentGroup)
admin.site.register(Reagent)
admin.site.register(OutputMovementReagent)
admin.site.register(InputMovementReagent)
