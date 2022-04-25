import os

from invoke import Collection, Config, Exit, task

VIRTUAL_ENV = "venv"
DOCKER_IMAGE_NAME = "entity-extraction"


@task
def install(ctx):
    """
    task which installs all the requirements present.
    """
    print("************ Install is started ************")
    ctx.run("pip --no-cache-dir install -r requirements.txt")
    print("************ Install is completed ************")

@task
def google_credentials(ctx):
    """
        task which setups the google_credentials
    """
    print("************ Checking if variables needed by application are present or not ****************")
    google_credentials = ctx.run(f"echo $GOOGLE_APPLICATION_CREDENTIALS").stdout.strip()
    if google_credentials == '':
        message = "GOOGLE_APPLICATION_CREDENTIALS environment variable are not present, please follow README.md file."
        raise Exit(message)

@task
def local_run(ctx):
    """
    task which starts the venv and runs the service.
    """
    print("************ local_run command is started ************")
    os.environ['FLASK_ENV'] = 'development'
    ctx.run("python run.py")
    print("************ local_run command is completed ************")


@task
def docker_clean(ctx):
    """
    task used to clean unused docker images
    """
    docker_exists = ctx.run(f"docker ps --filter ancestor={DOCKER_IMAGE_NAME} -q")
    image_exists = ctx.run(f"docker images {DOCKER_IMAGE_NAME} -a -q")
    if docker_exists.stdout:
        ctx.run(f"docker stop `docker ps --filter ancestor={DOCKER_IMAGE_NAME} -q`")
        ctx.run(f"docker rm `docker ps -a --filter ancestor={DOCKER_IMAGE_NAME} -q`")
    else:
        print(f"--------------| Container for image {DOCKER_IMAGE_NAME} does not exists! |--------------")
    if image_exists.stdout:
        ctx.run(f"docker rmi `docker images {DOCKER_IMAGE_NAME} -a -q` --force")
    else:
        print(f"--------------| Image {DOCKER_IMAGE_NAME} not exists! |--------------")

@task
def docker_build(ctx):
    """
    task which builds the docker image for the service
    """
    ctx.run(f"docker build -t {DOCKER_IMAGE_NAME} .")


@task
def local_docker_run(ctx):
    """
    task which run the docker image in local development
    """
    print("--------------| local_docker_run command is started |---------------")
    ctx.run(f"docker run -d -p 5000:5000 --env-file .env {DOCKER_IMAGE_NAME}")
    print("--------------| local_docker_run command is completed |---------------")

@task
def clean(ctx):
    """
    task used to clean pytest, dvc, and other cache.
    """
    ctx.run(f"rm -rf {VIRTUAL_ENV}")
    ctx.run("find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete")


@task(post=[google_credentials, install, local_run])
def local_dev(ctx):
    """
    task used to setup the system for local development
    by installing the dependencies in the virtual env.
    """
    print("*********** Starting local dev *************")


@task(post=[docker_build, local_docker_run])
def local_docker(ctx):
    """
    task used to build and run the docker image
    """
    print("*********** Starting docker *************")

# Add all tasks to the namespace
ns = Collection(install, google_credentials, local_run, local_dev, local_docker_run, docker_build,
                local_docker_run, local_docker, clean, docker_clean)
# setting this true to provide console output to commands while running
# config = Config(defaults={"run": {"pty": True}})
# ns.configure(config)
