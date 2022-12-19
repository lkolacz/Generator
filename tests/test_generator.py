import os
import pytest
import time
import subprocess
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from generator.generation import generate, generate_bulk


@pytest.mark.timeout(2)
def test_generate_miscellaneous_ids():
    generated_ids = set()
    count = 1000
    for _ in range(0, count):
        generated_id = generate()
        assert len(generated_id) == 8
        generated_ids.add(generated_id)
    assert count == len(generated_ids)


@pytest.mark.timeout(5)
def test_generate_bulk_miscellaneous_ids():
    generated_ids = set()
    step = 10000
    loop = 100
    for _ in range(0, loop):
        generated_ids.update(generate_bulk(step))
    assert loop*step == len(generated_ids)  # 1 mln


@pytest.mark.timeout(5)
def test_generate_bulk_via_many_threads_miscellaneous_ids():
    max_workers = multiprocessing.cpu_count()
    databricks = [1000 for _ in range(0, 1000)]
    generated_ids = set()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        workers_ids = list(executor.map((lambda x: list(x)), executor.map(generate_bulk, databricks)))
        for worker_ids in workers_ids:
            generated_ids.update(worker_ids)

    assert len(generated_ids) == 1000000  # 1 mln


@pytest.mark.timeout(10)
def test_continuity_after_reload_miscellaneous_ids():
    generated_ids = set()
    env = os.environ.copy()
    env['PYTHONPATH'] = os.getcwd() + ':' + env.get('PYTHONPATH', '')
    for _ in range(0, 5):
        process = subprocess.Popen(
            ["/usr/bin/env", "python", "-u", "scripts/generate.py"],
            stdout=subprocess.PIPE,
            env=env)
        time.sleep(1)
        process.kill()
        for incoming_id in process.stdout.readlines():
            incoming_id = incoming_id.strip()
            assert incoming_id not in generated_ids
            generated_ids.add(incoming_id)
