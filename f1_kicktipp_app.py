# f1_kicktipp_app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="F1 Kicktipp Analyse", page_icon="🏎️", layout="wide")

# ---- Einstellungen ----
RACE_POINTS = {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
QUALI_POINTS = {1: 4, 2: 3, 3: 2, 4: 1}
WM_BONUS = 20
CONSOLATION_POINT = 1

# ---- Funktionen ----
def max_points_per_race():
    return sum(RACE_POINTS.values()) + sum(QUALI_POINTS.values())

def calculate_championship_status(participants, races_remaining):
    max_points_remaining = races_remaining * max_points_per_race()
    max_points_with_wm = max_points_remaining + (2 * WM_BONUS)
    sorted_participants = sorted(participants, key=lambda x: x["points"], reverse=True)
    leader = sorted_participants[0]

    margin = leader["points"] - sorted_participants[1]["points"]
    champion_decided = margin > max_points_with_wm

    return {
        "leader": leader,
        "sorted": sorted_participants,
        "max_remaining": max_points_with_wm,
        "champion_decided": champion_decided,
        "margin": margin,
    }

# ---- UI ----
st.title("🏁 Formel 1 Kicktipp Analyse")

st.sidebar.header("🔧 Eingaben")
races_remaining = st.sidebar.number_input("Verbleibende Rennen", min_value=0, max_value=24, value=4)
st.sidebar.write("---")

st.sidebar.markdown("### Teilnehmer hinzufügen")
default_data = [
    {"Name": "Ich (Du)", "Punkte": 415, "Fahrer-WM Tipp": "Max Verstappen", "Team-WM Tipp": "McLaren"},
    {"Name": "David", "Punkte": 337, "Fahrer-WM Tipp": "Oscar Piastri", "Team-WM Tipp": "McLaren"},
]
df = st.data_editor(pd.DataFrame(default_data), num_rows="dynamic", key="participants_editor")

participants = [
    {"name": row["Name"], "points": row["Punkte"], "driver_wm_tip": row["Fahrer-WM Tipp"], "team_wm_tip": row["Team-WM Tipp"]}
    for _, row in df.iterrows()
]

if len(participants) < 2:
    st.warning("Bitte mindestens zwei Teilnehmer eingeben, um den Vergleich zu berechnen.")
    st.stop()

# ---- Berechnung ----
result = calculate_championship_status(participants, races_remaining)

leader = result["leader"]
max_points = result["max_remaining"]

col1, col2, col3 = st.columns(3)
col1.metric("🏆 Leader", leader["name"])
col2.metric("📈 Punkte", leader["points"])
col3.metric("🏁 Noch zu vergeben", max_points)

st.divider()

# ---- Tabelle ----
st.subheader("📊 Aktueller Punktestand")
df_sorted = pd.DataFrame([
    {"Name": p["name"], "Punkte": p["points"], "Fahrer-WM Tipp": p["driver_wm_tip"], "Team-WM Tipp": p["team_wm_tip"]}
    for p in result["sorted"]
])
st.dataframe(df_sorted, use_container_width=True)

# ---- Analyse ----
st.divider()
st.subheader("🔍 Championship Analyse")

leader_name = leader["name"]
margin = result["margin"]

if result["champion_decided"]:
    st.success(f"🏆 {leader_name} ist uneinholbar – bereits CHAMPION!")
else:
    st.warning(f"⚔️ {leader_name} führt mit {margin} Punkten. Noch nicht sicher!")
    st.caption(f"Noch {max_points} Punkte verfügbar – rechnerisch kann jemand aufholen.")

# ---- Szenarien ----
st.divider()
st.subheader("🎯 Szenarienanalyse")

for p in result["sorted"]:
    best = p["points"] + (races_remaining * max_points_per_race()) + (2 * WM_BONUS)
    worst = p["points"]
    st.markdown(
        f"**{p['name']}** – Aktuell: {p['points']} • Best Case: {best} • Worst Case: {worst}"
    )