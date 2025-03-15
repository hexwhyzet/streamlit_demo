import time

from analysis import load_data, sequential_calculations
from parallel_analysis import parallel_process_calculations, parallel_thread_calculations


def measure_execution_time(func, *args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    print(f"Execution time: {end_time - start_time:.4f} seconds")
    return result


if __name__ == '__main__':
    file_path = "temperature_data.csv"

    print("Sequential analysis")
    _ = measure_execution_time(sequential_calculations, load_data(file_path))

    print()

    print("Parallel analysis (Processes)")
    _ = measure_execution_time(parallel_process_calculations, load_data(file_path))

    print()

    print("Parallel analysis (Threads)")
    _ = measure_execution_time(parallel_thread_calculations, load_data(file_path))
