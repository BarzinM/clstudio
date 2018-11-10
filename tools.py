import os
import subprocess

def get_length(filename):
    import re
    result = subprocess.Popen(["ffprobe", filename],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.readlines()
    result = [x for x in output if b"Duration" in x]
    result = result[0].decode("utf-8")
    result = re.search('Duration: (.*), start', result).group(1)
    return result

def full_time_to_seconds(string):

    values = [float(s) for s in string.split(":")]
    sec = values[-1]
    length = len(values)

    if length > 1:
        sec = values[-2] * 60 + sec
    if length > 2:
        sec = values[-3] * 60 + sec

    return sec


def second_to_full_time(seconds):
    if type(seconds) == str:
        seconds = float(seconds)
    s = seconds % 60
    rest = int(seconds - s)
    rest = rest // 60
    m = rest % 60
    h = rest // 60

    output = "%i:%i:%2.3f" % (h, m, s)
    return output


def string_time_to_float(t):
    if ":" in t:
        return full_time_to_seconds(t)
    else:
        return float(t)


def is_file(path):
    return os.path.isfile(path)
