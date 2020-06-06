# -*- coding: utf-8 -*-
from __future__ import print_function
import logging
import os
import subprocess
import sys
try:
    from subprocess import DEVNULL
except ImportError:
    # Python 3.2 or below
    import os
    import atexit
    DEVNULL = os.open(os.devnull, os.O_RDWR)
    atexit.register(lambda fd: os.close(fd), DEVNULL)

def get_usable_ffmpeg(cmd):
    try:
        p = subprocess.Popen([cmd, '-version'], stdin=DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        vers = out.split('\n')[0].split()
        assert (vers[0] == 'ffmpeg' and vers[2][0] > '0') or (vers[0] == 'avconv')
        try:
            v = vers[2][1:] if vers[2][0] == 'n' else vers[2]
            version = [int(i) for i in v.split('.')]
        except:
            version = [1, 0]
        return cmd, 'ffprobe', version
    except:
        return None

FFMPEG, FFPROBE, FFMPEG_VERSION = get_usable_ffmpeg('ffmpeg') or get_usable_ffmpeg('avconv') or (None, None, None)
if logging.getLogger().isEnabledFor(logging.DEBUG):
    LOGLEVEL = ['-loglevel', 'info']
    STDIN = None
else:
    LOGLEVEL = ['-loglevel', 'quiet']
    STDIN = DEVNULL

def has_ffmpeg_installed():
    return FFMPEG is not None

# Given a list of segments and the output path, generates the concat
# list and returns the path to the concat list.


def ffmpeg_concat_av(files, output):
    print('Merging video parts... ')
    params = [FFMPEG] + LOGLEVEL
    for file in files:
        if os.path.isfile(file): params.extend(['-i', file])
    params.extend(['-c', 'copy'])
    params.append(output)
    if subprocess.call(params, stdin=STDIN):
        print('Merging without re-encode failed.\nTry again re-encoding audio... ')
        try: os.remove(output)
        except IOError: pass
        params = [FFMPEG] + LOGLEVEL
        for file in files:
            if os.path.isfile(file): params.extend(['-i', file])
        params.extend(['-c:v', 'copy'])
        params.extend(['-c:a', 'aac'])
        params.extend(['-strict', 'experimental'])
        params.append(output)
        return subprocess.call(params, stdin=STDIN)
    else:
        return 0







