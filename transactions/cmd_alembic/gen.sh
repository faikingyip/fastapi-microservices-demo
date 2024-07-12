#!/bin/bash

gen() {
  if [ -z "$1" ]; then
    echo "Error: Provide a revision message."
    echo "Usage: $0 \"your revision message\""
    return 1
  fi

  REVISION_MESSAGE=$1

  
  alembic revision --autogenerate -m "$REVISION_MESSAGE"
  
}


gen "$@"