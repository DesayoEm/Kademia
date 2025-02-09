import docker
from test_db import TEST_DB_URL

def start_docker_container():
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
        'ports':{'5432':'5433'},
        'environment':{
            'POSTGRES_USER': 'postgres',
            'POSTGRES_PASSWORD': TEST_DB_URL
        },
    }
    container = client.containers.run()
