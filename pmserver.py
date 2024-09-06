import pyvisa
import re
import flask
import waitress
import markupsafe
from typing import Any

app = flask.Flask(__name__)
power_meters = []

def _extract_ids(input:str) -> dict:
    m = re.match(r'^(?P<prefix>(?P<type>USB)\d*)(::(?P<vendor_id>[^\s:]+))'
                    r'(::(?P<device_id>[^\s:]+(\[.+\])?))(::(?P<serial>[^\s:]+))?'
                    r'(::(?P<suffix>INSTR))$', input, re.I)
    return m.groupdict()

def _connect(sn:str=None, vid:int=0x1313, did:int=0x8078, read_term:str='\n', write_term:str='\n', suppress_output:bool=False, timeout:int=1000) -> pyvisa.Resource:
    rm = pyvisa.ResourceManager()
    for dev in rm.list_resources():
        try:
            m = _extract_ids(dev)
            if int(m['vendor_id'], 16) == vid and int(m['device_id'], 16) == did \
                and (sn == None or sn == m['serial']):
                if not suppress_output:
                    print(f'Connecting to {m['serial']}')
                ret = rm.open_resource(dev, read_termination=read_term, write_termination=write_term, timeout=timeout)
                power_meters.append(ret)
                return ret
        except:
            continue
    raise RuntimeError('Power Meter not found')

def connect(sn:str=None, vid:int=0x1313, did:int=0x8078, read_term:str='\n', write_term:str='\n', suppress_output:bool=False, timeout:int=1000) -> pyvisa.Resource:
    for v in power_meters:
        m = _extract_ids(v.resource_name)

        if (sn == m['serial'] or sn == None) and vid == int(m['vendor_id'], 16) and did == int(m['device_id'], 16):
            if read_term == v.read_termination and timeout == v.timeout and write_term == v.write_termination:
                return v
            else:
                v.close()
                power_meters.remove(v)
    return _connect(sn=sn, vid=vid, did=did, read_term=read_term, write_term=write_term, suppress_output=suppress_output, timeout=timeout)


def query(sn:str, vid:int, did:int):
    args = {'rt': ('read_term', str), 
            'wt': ('write_term', str), 
            'to': ('timeout', int)}
    pm = connect(sn=sn, vid=vid, did=did
                 , **{args[k][0]:args[k][1](markupsafe.escape(v)) for k, v in flask.request.args.items() if v != None})
    print('Recv: ' + flask.request.get_data(as_text=True))
    if pm == None:
        flask.abort(404)
    if flask.request.method == 'GET':
        return pm.query(flask.request.get_data(as_text=True))
    elif flask.request.method == 'POST':
        pm.write(flask.request.get_data(as_text=True))
        return ('', 204)
    else:
        flask.abort(400)

@app.route('/<sn>/<int:vid>/<int:did>', methods=['GET', 'POST'])
def query_full(sn:str, vid:int, did:int):
    return query(sn=markupsafe.escape(sn), vid=markupsafe.escape(vid), did=markupsafe.escape(did))

@app.route('/<sn>', methods=['GET', 'POST'])
def query_sn(sn:str):
    return query(sn=markupsafe.escape(sn), vid=0x1313, did=0x8078)

@app.route('/', methods=['GET', 'POST'])
def query_default():
    return query(sn=None, vid=0x1313, did=0x8078)

if __name__ == "__main__":
    import argparse
    import socket
    import waitress
    
    parser = argparse.ArgumentParser(description='ThorlabsPM100D server')
    parser.add_argument('-p', '--port', metavar='port', required=False, type=int, 
                        help='port number')

    args = parser.parse_args()
    port = args.port if args.port is not None else 8002
    ip = socket.gethostbyname(socket.gethostname())
    print(f"Server starting on {ip} port {port}")
    waitress.serve(app, port=port)