import urllib, urllib2
import base64
import StringIO

class BaseParser(object):
    """
    Grabbers may be used outside of django environment as standalone script.
    Do not import packages depend on django.
    suggested usage:
    """
    def __init__(self):
        super(BaseParser, self).__init__()
        self.require_captcha = False
        self.status = 0
        self.captcha_img_url = ''

    def setUp(self,**kwargs):
        self.username = kwargs['username']
        self.password = kwargs['password']
        if self.require_captcha:
            try:
                self.captcha = kwargs.get('captcha')
            except:
                raise LookupError('captcha required')

    def run(self):
    
    def _fetch_img(self):

        encoded_captcha = StringIO.StringIO()
        base64.encode(captcha,encoded_captcha)
        encoded_captcha.getvalue()

    def work_flow_type(self):
        if not self.require_captcha:
            return {
                'status':1,
            }
        if self.require_captcha:


class TeapotParser(BaseParser):
    def __init__(self):
        super(TeapotParser, self).__init__()
        self.require_captcha = True

    def run(self):
