# -*- encoding: utf-8 -*-
# Author: Ricardo Dani
# E-mail: ricardodani@gmail.com

def get_in_list(d, k, sl):
    '''
    Gets a `d` dictonary-like object, a `k` key and a `sl` suggestions list.
    Returns a item from the dictionary if the `k` exists in `d`
    and is in `sl`, otherwise, returns the first item of `sl`.

    i.e:

    >>> get_in_list({}, 'test', ('a', 'b'))
    >>> 'a'
    >>> get_in_list({'test': 'b'}, 'test', ('a', 'b'))
    >>> 'b'
    >>> get_in_list({'test': 'c'}, 'test', ('a', 'b'))
    >>> 'a'
    '''
    # get item from `d` or default if not exists the key
    item = d.get(k, sl[0])
    # if the item exists, verify if it's in the sl
    return sl[0] if item not in sl else item
