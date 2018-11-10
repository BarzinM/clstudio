from tools import is_file, string_time_to_float, get_length

fname = "montage.cls"

with open(fname) as f:
    content = f.readlines()

content = [x.strip() for x in content]


def get_file_name(line):
    input_file_name, rest = line.split(" ", 1)
    # if is_file(input_file_name):
    #     return input_file_name
    # else:
    #     raise FileNotFoundError(input_file_name)
    return input_file_name, rest


def get_time(line):
    rest_1, time = line.split("[", 1)
    time, rest_2 = time.split("]", 1)
    time = time.replace(',', ' ')
    time = time.replace('  ', ' ')
    start, end = time.split(" ")
    start = string_time_to_float(start)
    if end[0] == "+":
        duration = string_time_to_float(end[1:])
        end = start + duration
    else:
        end = string_time_to_float(end)
    rest = rest_1 + " " + rest_2
    rest = rest.replace("  ", " ")
    return start, end, rest
    # print(start, end)


def get_speed(line):
    l = line.split('x', 1)[1:]
    for h in l:
        h = h.split(" ")[0]
        try:
            h = float(h)
            return h
        except ValueError:
            continue
    return 1.


def get_output(line):
    file_name = line.split('>')[1:]
    if len(file_name) > 1:
        raise ValueError("could not understand the output file name")
    elif len(file_name) == 1:
        return file_name[0].strip()
    else:
        return None


def get_extension(file_name):
    if "." in file_name:
        return file_name.split('.')[-1]
    else:
        return None


def generate_file_name(input_file, start, end, speed):
    pass


def iterate(line):
    file_name, line = get_file_name(line)
    in_ext = get_extension(file_name)
    start, end, line = get_time(line)
    if end < 0:
        duration = get_length(file_name)
        end = duration + end
        print("CHECK IMPLEMENTATION", duration, end)
    speed = get_speed(line)
    output = get_output(line)
    if output:
        ext = get_extension(output)
    else:
        ext = None
    if ext == "gif":
        pass
    elif ext is None:
        output = output + '.' + ext

    print(file_name, start, end, speed, output, (in_ext, ext))


for l in content:
    iterate(l)
