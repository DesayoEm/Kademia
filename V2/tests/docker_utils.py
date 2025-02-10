import docker
from .test_db import TEST_DB_URL
import time

def is_container_ready(container):
    container.reload()
    return container.status =='running'

def wait_for_stable_status(container, duration = 3, interval = 1):
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < duration:
        if is_container_ready(container):
            stable_count +=1
        else:
            stable_count = 0
        if stable_count <= duration/interval:
            return True
        time.sleep(interval)
    return False




def start_database_container():
    client = docker.from_env()
    container_name = 'testtrakademik'

    try:
        existing_container = client.containers.get(container_name)
        print(f"Container {container_name} exists. stopping and removing...")
        existing_container.stop()
        existing_container.remove()
        print(f"Container {container_name} stopped and removed")
    except docker.errors.NotFound:
        print(f"Container {container_name} does not exist")


    container_config = {
        'name': container_name,
        'image': 'postgres:16.1-alpine3.19',
        'detach': True,
        'ports':{'5432':5433},
        'environment':{
            'POSTGRES_USER': 'postgres',
            'POSTGRES_PASSWORD': TEST_DB_URL,
            'POSTGRES_DB': 'testtrakademik'
        },
    }
    container = client.containers.run(**container_config)

    while not is_container_ready(container):
        time.sleep(1)
    if not wait_for_stable_status(container):
        raise RuntimeError('Container did not stabilize on time')
    return container


