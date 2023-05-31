import time
import time

def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return "{:02d}:{:02d}".format(int(minutes), int(seconds))

def run_stopwatch():
    start_time = None

    while True:
        user_input = input("Press ENTER to start/stop or 'q' to quit: ")

        if user_input.lower() == 'q':
            break

        if start_time is None:
            start_time = time.time()
        else:
            elapsed_time = time.time() - start_time
            print("Elapsed time:", format_time(elapsed_time))

    print("Goodbye!")

run_stopwatch()
