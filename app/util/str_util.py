# -*- coding: UTF-8 -*-
import string
import struct
import socket
import os
import time
import uuid
from hashlib import md5
import threading
import random
import binascii




###生成11位随机码
###id + CN + 随机码



def random_code(id,length):
    prefix = hex(int(id))[2:]+ 'c'
    length = length - len(prefix)
    #print string.ascii_letters
    chars=string.digits
    return prefix + ''.join([random.choice(chars) for i in range(length)])


def create_uinque_code():
    _inc = random.randint(0, 0xFFFFFF)
    _inc_lock = threading.Lock()

    oid = ""

    oid += struct.pack(">i", int(time.time()))

    m = md5()
    m.update(socket.gethostname())
    oid += m.digest()[0:3]

    oid += struct.pack(">H", os.getpid() % 0xFFFF)

    _inc_lock.acquire()
    oid += struct.pack(">i", _inc)[1:4]
    _inc = (_inc + 1) % 0xFFFFFF
    _inc_lock.release()

    return binascii.hexlify(oid)



def create_uuid():
    id = str(uuid.uuid1())
    return  id.replace('-','')