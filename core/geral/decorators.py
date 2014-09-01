# -*- encoding: utf-8 -*-

from .models import Shopping

def indica_shopping(funcao):
    def _wrap(*args, **kwargs):
        request = args[0]
        chave_shooping = kwargs.get('shp_id', None)

        if not chave_shooping:
            slug = request.GET.get('shopping', None)
            if not slug:
                kwargs['shp_id'] = 1
            else:
                shopping = Shopping.objects.filter(slug=slug)[:1]
                if shopping:
                    kwargs['shp_id'] = shopping[0].id
        else:
            kwargs['shp_id'] = chave_shooping

        return funcao(*args, **kwargs)
    return _wrap