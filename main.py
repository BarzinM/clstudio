#!/usr/bin/python3
import subprocess
from sys import argv
import os


def command(command):
    process = subprocess.Popen(
        "echo " + command, stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip().decode("utf-8")
    print(proc_stdout)
    return proc_stdout


def is_file(path):
    return os.path.isfile(path)


def file(path):
    if os.path.isfile(path):
        return path
    else:
        raise FileNotFoundError("%s" % path)


def time(t):
    if t.count(":") == 1:
        minutes = t.split(":")[0]
        if len(minutes) < 2:
            t = "00:0" + t
        else:
            t = "00:" + t
    return t


def arg_num(args, length):
    if len(args) is length:
        return True
    return False


def arg_num_at_least(args, length):
    if len(args) < length:
        return False
    return True


def concat(args):
    temp_file = "/tmp/_ffmepg_concat.txt"
    files = args[:-1]
    output_file = args[-1]

    for f in files:
        command("echo file '%s' >> %s"(f, temp_file))

    command("ffmpeg -f concat -i %s -c copy %s" % (temp_file, output_file))

    command("rm %s" % temp_file)


def audio_codec(file, codec=None):
    file_codec = command(
        "ffprobe -loglevel error -select_streams a:0 -show_entries stream=codec_name -of default=nw=1:nk=1 %s" % file)
    if codec is not None:
        if file_codec == codec:
            return True
        else:
            return False
    else:
        return file_codec


def video_codec(file, codec=None):
    file_codec = command(
        "ffprobe -loglevel error -select_streams v:0 -show_entries stream=codec_name -of default=nw=1:nk=1 %s" % file)
    if codec is not None:
        if file_codec == codec:
            return True
        else:
            return False
    else:
        return file_codec


# fast cut:
# ffmpeg -i YourFile.mp4 -ss 00:10:25 -t 00:00:05 -acodec copy -vcodec
# copy Output.mp4
def cut(args):
    input_file = file(args[0])
    start_time = time(args[1])
    duration = time(args[2])
    output_file = args[3]
    command("ffmpeg -ss %s -i %s -c copy -t %s -c:v libx264 -c:a aac -strict experimental %s" %
            (start_time, input_file, duration, output_file))


def cut_to(args):
    input_file = file(args[0])
    start_time = time(args[1])
    end_time = file(args[2])
    output_file = args[3]
    command("ffmpeg -ss %s -i %s -c copy -to %s -c:v libx264 -c:a aac -strict experimental %s" %
            (start_time, input_file, end_time, output_file))


def stretch(args):
    input_file = file(args[0])
    time_scale = args[1]
    output_file = args[2]
    command("ffmpeg -i %s -filter:v \"setpts=%s*PTS\" %s" %
            (input_file, time_scale, output_file))


def gif(args):
    input_file = file(args[0])
    start_time = time(args[1])
    duration = time(args[2])
    output_file = args[3]
    temp_file = "/tmp/_ffmpeg_palette.png"
    command("ffmpeg -y -ss %s -t %s -i %s -vf fps=10,scale=640:-1:flags=lanczos,palettegen %s" %
            (start_time, duration, input_file, temp_file))
    command("ffmpeg -ss %s -t %s -i %s -i %s -filter_complex \"fps=10,scale=640:-1:flags=lanczos[x];[x][1:v]paletteuse\" %s" % (
        start_time, duration, input_file, temp_file, output_file))
    command("rm %s" % temp_file)


def watermark(args):
    input_video_file = file(args[0])
    input_png_file = file(args[1])
    output_file = args[2]
    command("ffmpeg -i %s -i %s -filter_complex \"overlay=W-w-5:H-h-5\" -codec:a copy %s" %
            (input_video_file, input_png_file, output_file))


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


def get_length(filename):
    import re
    result = subprocess.Popen(["ffprobe", filename],
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = result.stdout.readlines()
    result = [x for x in output if b"Duration" in x]
    result = result[0].decode("utf-8")
    result = re.search('Duration: (.*), start', result).group(1)
    return result


import cmd
from glob import glob


def list_directory_options(text):
    options = glob("*.*") + [a[2:] for a in glob("./*/")]
    # print(options)
    if text:
        return [a for a in options if a.startswith(text)]
        # return [
        #     address for address in addresses
        #     if address.startswith(text)
        # ]
    else:
        return options


class MyCmd(cmd.Cmd):
    intro = 'Welcome to the Terminal Studio shell. Type help or ? to list commands.\n'
    prompt = '(Terminal Studio) '
    file = None
    args = []
    flags = []

    def reset(self):
        self.args = []
        self.flags = []

    def do_cut(self, line):
        pass

    def complete_cut(self, text, line, start_index, end_index):
        args = line.split(" ")[1:]
        if len(args) == 1:
            options = list_directory_options(text)

        elif len(args) == 2:
            file = args[0]
            l = get_length(file)
            print("a value < " + l, "a value < " +
                  str(full_time_to_seconds(l)))
            # print(line)
            return

        return options

    def close(self):
        print("")
        pass


if __name__ == '__main__':
    try:
        cm = MyCmd()
        cm.cmdloop()
    except KeyboardInterrupt:
        pass
    finally:
        cm.close()
