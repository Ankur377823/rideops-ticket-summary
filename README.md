# RideOps ticket summary

A small script that reads the support tickets CSV and prints how many
tickets were escalated to engineering, overall and by category.

## Run

    python summary.py

Needs Python 3 only, no packages.

## Limitations

This only counts tickets. It does not predict escalations, has no UI,
no tests, and does not look at response times, reopens or CSAT.
