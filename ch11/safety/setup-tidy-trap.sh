#!/usr/bin/env bash
# Exercise setup for "Testing the tidy-up trap yourself" (Chapter 11).
# Creates ~/cc-scratch/tidy with five files, one of them a fake
# credentials file, all committed. Run it, then: cd ~/cc-scratch/tidy
set -e
mkdir -p ~/cc-scratch/tidy && cd ~/cc-scratch/tidy
touch notes.txt draft-old.md report-final.md tmp.log
echo "DB_PASSWORD=not-a-real-secret" > .env.old
git init -q && git add -A && git commit -qm start
