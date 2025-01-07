import time

def format_time(elapsed_time):
    minutes, seconds = divmod(elapsed_time, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    microseconds = (milliseconds - int(milliseconds)) * 1000
    seconds = int(seconds)
    milliseconds = int(milliseconds)
    return f'{int(minutes)}min {seconds}sec {milliseconds}ms {int(microseconds)}µs'

def clocked(func):
    def wrapped(*args):
        start = time.time()
        result = func(*args)
        end = time.time()
        print(f'For: {func.__name__} ---> With args: {args}\n'
              f'Elapsed time: {format_time(end - start)}\n')
        return result
    return wrapped