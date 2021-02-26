import json
from abc import ABC

from aiohttp_session import AbstractStorage


class ExtendedAbstractStorage(AbstractStorage, ABC):
    def __init__(self, *, cookie_name="AIOHTTP_SESSION", domain=None, max_age=None, path='/', secure=None,
                 httponly=True, encoder=json.dumps, decoder=json.loads, samesite='none'):
        super().__init__(cookie_name=cookie_name, domain=domain, max_age=max_age, path=path, secure=secure,
                         httponly=httponly, encoder=encoder, decoder=decoder)
        self._cookie_params['samesite'] = samesite