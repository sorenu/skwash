from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
import json



def search(request, as_json=False):
    q = request.GET.get('q')
    typeahead = request.GET.get('typeahead')

    users = User.objects.filter(
        Q(username__icontains=q) |
        Q(email__icontains=q)
        )

    if as_json:
        return HttpResponse(serializers.serialize('json', users, fields=('username', 'email')))
    if typeahead:
        a = [u.username for u in users]
        return HttpResponse(json.dumps(a), content_type='application/json')
    return render(request, 'website/search_result.html', {'result': users})