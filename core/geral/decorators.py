# -*- encoding: utf-8 -*-

from lojas.models import Shopping

def indica_shopping(funcao):
    def _wrap(*args, **kwargs):
        request = args[0]
        cookie_shopping = request.COOKIES.get('shp_id', None)
        slug = kwargs['slug']
        if slug:
            shopping = Shopping.objects.filter(slug=slug)[:1]
            if shopping:
                kwargs['shp_id'] = shopping[0].id
        elif cookie_shopping:
            kwargs['shp_id'] = cookie_shopping
        else:
            kwargs['shp_id'] = 1

        return funcao(*args, **kwargs)
    return _wrap