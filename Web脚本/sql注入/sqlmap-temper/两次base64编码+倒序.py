from lib.core.compat import xrange
from lib.core.enums import PRIORITY
import base64

__priority__ = PRIORITY.LOW

def dependencies():
    pass

def space(payload):
    if payload:
        retVal = ""
        quote, doublequote, firstspace = False, False, False

        for i in xrange(len(payload)):
            if not firstspace:
                if payload[i].isspace():
                    firstspace = True
                    retVal += chr(0x09)
                    continue

            elif payload[i] == '\'':
                quote = not quote

            elif payload[i] == '"':
                doublequote = not doublequote

            elif payload[i] == " " and not doublequote and not quote:
                retVal += chr(0x09)
                continue

            retVal += payload[i]

    return retVal

def tamper(payload, **kwargs):
    payload = payload[::-1]
    payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    payload = payload[::-1]
    payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    return space(payload)

