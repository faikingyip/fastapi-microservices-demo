#!/bin/bash

# Stop the Minikube cluster
minikube stop

# Delete the Minikube cluster
minikube delete

# Optional: Remove Minikube configuration and data
rm -rf ~/.minikube