import os

# conftest is run before main.py when you run pytest.

# This env variable is auto
# removed once testing is completed.
os.environ["ENV"] = "Testing"
