import requests

def _check_url(url:str, port:int) -> None:
    if not isinstance(port, int):
        raise TypeError(f"port must be an instance of type int, got {type(port)}.")
    if not isinstance(url, str):
        raise TypeError(f"url must be an instance of type str, got {type(url)}.")
    if port < 1 or port > 65535:
        raise ValueError(f"port must be within [1-65535], got {port}.")

class Instrument:
    def __init__(self, url:str, port:int, sn:str=None) -> None:
        _check_url(url, port)
        self.url = url
        self.port = port
        if sn != None:
            self.sn = sn
        else: self.sn = ''

    def write(self, command:str) -> None:
        r = requests.post('http://' + str(self.url) + ':' + str(self.port) + '/' + self.sn, headers={'Content-Type': 'text/plain'}, data=command)
        r.raise_for_status()

    def query(self, command:str) -> str:
        r = requests.get('http://' + str(self.url) + ':' + str(self.port) + '/' + self.sn, headers={'Content-Type': 'text/plain'}, data=command)
        r.raise_for_status()
        print(r.content)
        return r.content.decode('ascii')