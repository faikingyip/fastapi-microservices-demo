#!/bin/bash

commit_and_push() {
  if [ -z "$1" ]; then
    echo "Error: No commit message provided."
    echo "Usage: $0 \"your commit message\""
    return 1
  fi

  COMMIT_MESSAGE=$1

  git add .
  git commit -m "$COMMIT_MESSAGE"
  git push origin main
}


commit_and_push "$@"