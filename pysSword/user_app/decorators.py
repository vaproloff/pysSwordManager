from django.shortcuts import redirect


def reauthenticate_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('reauthenticate', False):
            request.session['forward'] = request.get_full_path()
            return redirect('reauthenticate')

        return view_func(request, *args, **kwargs)

    return _wrapped_view
