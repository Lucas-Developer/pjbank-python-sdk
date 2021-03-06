#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pjbank.api import PJBankAPI

class ContaDigital(PJBankAPI):
    """docstring for ContaDigital."""
    def __init__(self, credencial=None, chave=None, webhook_chave=None):
        super().__init__()
        self._endpoint_base = "contadigital"
        self._webhook_chave = webhook_chave

    def automatico(f):
        def wrapper(self, *args, **kwargs):
            if kwargs['c']:
                self.credencial = kwargs['c']
            if kwargs['ch']:
                self.chave = kwargs['ch']
            kwargs.pop('c')
            kwargs.pop('ch')
            return f(self, *args, **kwargs)
        return wrapper

    @property
    def webhook_chave(self):
        return self._webhook_chave

    @webhook_chave.setter
    def webhook_chave(self, chave):
        self._webhook_chave = chave

    def credenciar(self, dados):
        super().credenciar(dados)
        self.webhook_chave = self.resposta_credenciamento['webhook_chave']
        return self

    def _consulta(self, endpoint=None):
        headers = self.headers_chave        
        response = self._get(endpoint, headers)
        return response.json()   

    @automatico    
    def dados_conta(self):
        return self._consulta()
    @automatico        
    def documentos(self):
        return self._consulta(['documentos'])
    
    @automatico    
    def status_socio(self, email):
        return self._consulta(['administradores', email])

    @automatico    
    def administradores(self):
        return self._consulta(['administradores'])