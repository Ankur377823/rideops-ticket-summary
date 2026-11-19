from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="RideOps escalation check", layout="wide")

# Engineering verdicts that mean the ticket did not need an engineer.
AVOIDABLE = [
    "Config issue - returned to L1",
    "Insufficient info - returned to L1",
    "Duplicate of known issue",
    "Not a bug - how-to",
    "Not reproducible",
]


@st.cache_data
def load():
    df = pd.read_csv(Path(__file__).parent / "data" / "rideops_support_tickets.csv")
    df["escalated"] = df["escalated_to_eng"] == "Yes"
    df["avoidable"] = df["eng_outcome"].isin(AVOIDABLE)
    return df


df = load()

st.title("RideOps escalation check")
st.write(
    "How many tickets does L1 support send to engineering, "
    "and how many of those did engineering not need to see?"
)

# Filters
st.sidebar.header("Filters")
tiers = st.sidebar.multiselect("Client tier", sorted(df["client_tier"].unique()))
priorities = st.sidebar.multiselect("Priority", sorted(df["priority"].unique()))
if tiers:
    df = df[df["client_tier"].isin(tiers)]
if priorities:
    df = df[df["priority"].isin(priorities)]

if df.empty:
    st.warning("No tickets match these filters.")
    st.stop()

esc = df[df["escalated"]]
done = esc[esc["eng_outcome"].notna()]  # escalations engineering has ruled on

# Headline numbers
c1, c2, c3, c4 = st.columns(4)
c1.metric("Tickets", len(df))
c2.metric("Escalated", len(esc), f"{len(esc) / len(df):.0%} of tickets", delta_color="off")
if len(done):
    c3.metric("Fixed by eng", int((done["eng_outcome"] == "Fixed").sum()))
    c4.metric(
        "Avoidable",
        int(done["avoidable"].sum()),
        f"{done['avoidable'].mean():.0%} of escalations",
        delta_color="off",
    )
else:
    st.info("No escalated tickets in this selection.")
    st.stop()

left, right = st.columns(2)

with left:
    st.subheader("What engineering said")
    st.bar_chart(done["eng_outcome"].value_counts(), horizontal=True)

with right:
    st.subheader("Avoidable escalations by category")
    by_cat = (
        done.groupby("category")
        .agg(escalated=("ticket_id", "count"), avoidable=("avoidable", "sum"))
        .sort_values("avoidable", ascending=False)
    )
    by_cat["avoidable %"] = (100 * by_cat["avoidable"] / by_cat["escalated"]).round(0)
    st.dataframe(by_cat, width="stretch")

st.subheader("Avoidable escalations by agent")
by_agent = (
    done.groupby("assigned_agent")
    .agg(escalated=("ticket_id", "count"), avoidable=("avoidable", "sum"))
    .sort_values("avoidable", ascending=False)
)
by_agent["avoidable %"] = (100 * by_agent["avoidable"] / by_agent["escalated"]).round(0)
st.dataframe(by_agent, width="stretch")

st.subheader("The avoidable tickets")
st.dataframe(
    done[done["avoidable"]][
        ["ticket_id", "client_name", "category", "priority", "description", "assigned_agent", "eng_outcome"]
    ],
    width="stretch",
    hide_index=True,
)
