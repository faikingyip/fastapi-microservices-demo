#!/bin/bash


echo -e "\n\n=============================="
echo -e "RUNNING FLAKE8..........\n"
docker compose run --rm app sh -c "flake8"

echo -e "\n\n"