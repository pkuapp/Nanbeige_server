
class BaseParser(object):
    """
    Grabbers may be used outside of django environment as standalone script.
    Do not import packages depend on django.
    suggested usage:
    """
    def __init__(self):
        super(BaseParser, self).__init__()

    def setUp(self,):

    def get_parse_flow_type(self):
        if self.parse_flow_type:
            return self.parse_flow_type
        else:
            return 0, 'transparent'


    def 