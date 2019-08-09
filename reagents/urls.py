from django.urls import path

from reagents.views import AllReagents, EditReagent, create_output, create_input, AllOutputMovements, AllInputMovements, \
    ReagentCreate

urlpatterns = [
    path('new_reagent/', ReagentCreate.as_view(), name='reagent_create'),
    path('all_reagents/', AllReagents.as_view(), name='all_reagents_list'),
    path('edit_reagent/<int:pk>', EditReagent.as_view(), name='edit_reagent'),
    path('remove_stock/<int:reagent_id>', create_output, name='remove_stock_reagents'),
    path('remove_stock/', create_output, name='remove_stock_reagents'),
    path('add_stock/<int:reagent_id>', create_input, name='add_stock_reagents'),
    path('add_stock/', create_input, name='add_stock_reagents'),
    path('output_history/', AllOutputMovements.as_view(), name='output_history_reagents'),
    path('input_history/', AllInputMovements.as_view(), name='input_history_reagents'),

]