import subprocess
import re
import time
from collections import deque
import csv
from concurrent.futures import ProcessPoolExecutor, as_completed
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

parents = [50, 100, 150, 300, 500]
children = [100, 200, 300, 500, 1000]
starting_population_multipliers = [1, 2, 3]
mutation_probs = [1/29, 0.01, 0.05, 0.1]
tsp_name = "bays29"
timeout_seconds = 300  # 5 minutes timeout

def run_genetic_algorithm(params):
    parents, children, mutation, multiplier = params
    command = [
        'python', 'main.py',
        '-p', str(parents),
        '-c', str(children),
        '-m', str(mutation),
        '-s', str(multiplier),
        '-n', 'False',
        '-u', '1',
        '-t', tsp_name
    ]
    start_time = time.time()
    try:
        process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cost_history = deque(maxlen=101)
        generation_count = 0
        last_cost = None
        converged = False

        logging.info(f"Process started for {params}")

        while True:
            line = process.stdout.readline()
            if not line:
                break
            generation_match = re.search(r'Generation #(\d+)', line)
            cost_match = re.search(r'Generation #\d+ \((\d+),', line)

            if generation_match:
                current_generation = int(generation_match.group(1))
                generation_count = current_generation

            if cost_match:
                cost = int(cost_match.group(1))
                last_cost = cost
                cost_history.append(cost)

                if len(cost_history) == cost_history.maxlen and cost_history[0] == cost:
                    converged = True
                    process.terminate()
                    logging.info(f"Convergence achieved for {params} at generation {current_generation}")
                    break

            if time.time() - start_time > timeout_seconds:
                process.terminate()
                logging.warning(f"Process timed out for {params}")
                break

        process.wait()
        elapsed_time = time.time() - start_time

        if converged:
            return (parents, children, multiplier, mutation, last_cost, 'Converged', generation_count, elapsed_time)
        elif time.time() - start_time > timeout_seconds:
            return (parents, children, multiplier, mutation, last_cost, 'Timed out', generation_count, elapsed_time)
        return (parents, children, multiplier, mutation, last_cost, 'Completed', generation_count, elapsed_time)

    except subprocess.TimeoutExpired:
        process.kill()
        return (parents, children, multiplier, mutation, last_cost, 'Timeout', generation_count, time.time() - start_time)
    except Exception as e:
        return (parents, children, multiplier, mutation, None, 'Error', generation_count, time.time() - start_time)

def process_all_combinations():
    task_params = [(p, c, m, s) for p in parents for c in children for m in mutation_probs for s in starting_population_multipliers]
    local_results = []
    for params in task_params:
        result = run_genetic_algorithm(params)
        local_results.append(result)
    return local_results

results = []
with ProcessPoolExecutor(max_workers=16) as executor:
    futures = [executor.submit(process_all_combinations) for _ in range(16)]
    for future in as_completed(futures):
        results.extend(future.result())

def save_results_to_csv(results, filename='ga_results.csv'):
    headers = ['Parents', 'Children', 'Multiplier', 'Mutation Probability', 'Cost', 'Status', 'Generations', 'Time (seconds)']
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(headers)
        for result in results:
            writer.writerow(result)

save_results_to_csv(results)
logging.info("Results have been saved to 'ga_results.csv'.")
