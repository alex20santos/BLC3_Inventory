from django.shortcuts import render, redirect



def homepage(request):
    if request.user.is_authenticated:
        template_name = 'inventory/home.html'
        context = {
            'admin':True,
            'active_page': "dashboard",
        }
        return render(request, template_name, context)

    else:
        return redirect('login')
