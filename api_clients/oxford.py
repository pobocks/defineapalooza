import attr
from attr import Factory

@attr.s(slots=True)
class OxfordClient: 
    headers = attr.ib(default=Factory(dict))
    
