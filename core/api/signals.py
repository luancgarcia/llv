# -*- encoding: utf-8 -*-

def apiuser_post_save(sender, **kwargs):
    f = kwargs['instance']
    if not f.token:
        f.token = f.create_token(f.shopping.first().slug if f.shopping.all() else f.email)
        f.save()
