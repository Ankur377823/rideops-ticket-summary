# RideOps escalation check

A small Streamlit app over the RideOps support tickets. It answers one question:

**How many tickets does L1 support send to engineering, and how many of those did engineering not need to see?**

An escalation is counted as *avoidable* when engineering closed it as a config
issue, insufficient info, a duplicate of a known issue, a how-to, or not reproducible.

On the full data set: 1,444 tickets, 486 escalated (34%), 211 fixed by
engineering, 275 avoidable (57% of escalations).

## What it shows

- Headline numbers, with filters for client tier and priority
- What engineering said about the escalated tickets
- Avoidable escalations by category and by L1 agent
- The list of avoidable tickets

## Run

    pip install -r requirements.txt
    streamlit run app.py

## Limitations

This is a descriptive view only. It does not predict whether a new ticket
should be escalated, has no tests, and does not look at response times,
reopens or CSAT.
