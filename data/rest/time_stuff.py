def to_seconds(time_string):
    array = time_string.split(':')
    return 3600*int(array[0])+60*int(array[1])+int(array[2].split('.')[0])