from pathlib import Path
import os

# import sys

## https://pypi.org/project/python-dotenv/
from dotenv import load_dotenv

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# environment = sys.argv[1]
environment = os.environ.get("PYTHON_ENV").lower()
env_path = Path(f"{ROOT_DIR}/{environment}.env")
load_dotenv(dotenv_path=env_path)

# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

# atlas_tls_ca_file_path = "{}/{}".format(ROOT_DIR, atlas_tls_ca_file_name) if atlas_tls_ca_file_name != "" else None
# task_server_uri = os.getenv("TASK_SERVER_URI")


# from dotenv import dotenv_values
# config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}


# config = {
#     **dotenv_values(".env.shared"),  # load shared development variables
#     **dotenv_values(".env.secret"),  # load sensitive variables
#     **os.environ,  # override loaded values with environment variables
# }
