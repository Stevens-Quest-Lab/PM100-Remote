import requests
from ThorlabsPM100 import ThorlabsPM100
from typing import Optional
from types import NoneType

def _check_url(url:str, port:int) -> NoneType:
    """
    Validates the url

    Parameters
    ----------
    url : str
        the base url
    port : int
        the remote server port

    Returns
    -------
    None

    Raises
    ------
    TypeError
        when the inputs are not in the correct format
    ValueError
        when the port number is invalid
    """
    if not isinstance(port, int):
        raise TypeError(f"port must be an instance of type int, got {type(port)}.")
    if not isinstance(url, str):
        raise TypeError(f"url must be an instance of type str, got {type(url)}.")
    if port < 1 or port > 65535:
        raise ValueError(f"port must be within [1-65535], got {port}.")

class Instrument:
    """
    HTTP backend for Thorlabs PM100 interface

    Attributes
    ----------
    url : str
        the base url
    port : int
        the remote server port
    sn : Optional[str]
        designate the serial number if multiple devices are connected to the server
    """
    def __init__(self, url:str, port:int, sn:Optional[str]=None) -> None:
        _check_url(url, port)
        self.url = url
        self.port = port
        if sn != None:
            self.sn = sn
        else: self.sn = ''
        self.power_meter = ThorlabsPM100(inst=self)

    def write(self, command:str) -> None:
        r = requests.post('http://' + str(self.url) + ':' + str(self.port) + '/' + self.sn, headers={'Content-Type': 'text/plain'}, data=command)
        r.raise_for_status()

    def query(self, command:str) -> str:
        r = requests.get('http://' + str(self.url) + ':' + str(self.port) + '/' + self.sn, headers={'Content-Type': 'text/plain'}, data=command)
        r.raise_for_status()
        print(r.content)
        return r.content.decode('ascii')