from format import Header
from message import Pack

CON = 0
"""Confirmable message type."""

NON = 1
"""Non-confirmable message type."""

ACK = 2
"""Acknowledgement message type."""

RST = 3
"""Reset message type"""

types = {0: 'CON',
         1: 'NON',
         2: 'ACK',
         3: 'RST'}

EMPTY = 0
GET = 1
POST = 2
CUSTOM = 3
requests = {1: 'GET',
            2: 'POST',
            3: 'CUSTOM',}

responses = {65: '2.01 Created',
             67: '2.03 Valid',
             132: '4.04 Not Found'}
