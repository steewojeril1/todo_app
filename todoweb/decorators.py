from django.shortcuts import redirect
def sign_in_required(fn):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            return redirect('custom_login')
    return wrapper