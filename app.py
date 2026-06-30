"""
MyTwin — Personal Academic Analytics Dashboard
Student: Aswadh B Pramod | Problem: G1 | Segment: Analytics Engineering
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from data_loader import load_marks, load_attendance, load_cgpa_summary, load_students

st.set_page_config(page_title="MyTwin — Academic Dashboard", page_icon="🎓", layout="wide")

# ---------- Load data ----------
marks = load_marks()
attendance = load_attendance()
cgpa = load_cgpa_summary()
students = load_students()

me = students[students["profile_type"] == "self"].iloc[0]

st.title("🎓 MyTwin — My Academic Dashboard")
st.caption(f"{me['name']} · Rank #{int(me['rank_in_section'])} in section · Overall CGPA: {me['overall_cgpa']}")

tab1, tab2, tab3, tab4 = st.tabs(["📌 My Snapshot", "📈 Trends", "🎯 What-If Simulator", "🤝 Peer Benchmarking"])

# ============================================================
# TAB 1 — My Snapshot
# ============================================================
with tab1:
    st.subheader("Where I stand right now")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall CGPA", f"{me['overall_cgpa']:.2f}")
    col2.metric("Avg Attendance", f"{me['avg_attendance']:.1f}%")
    col3.metric("Section Rank", f"#{int(me['rank_in_section'])}")
    latest_sem = cgpa.dropna(subset=["tgpa"])["semester"].max()
    latest_tgpa = cgpa[cgpa["semester"] == latest_sem]["tgpa"].values[0]
    col4.metric(f"Latest TGPA (Sem {latest_sem})", f"{latest_tgpa:.2f}")

    st.divider()

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Subject-wise performance (latest completed semester)**")
        latest = marks[marks["semester"] == latest_sem].dropna(subset=["overall_pct"])
        fig = px.bar(
            latest.sort_values("overall_pct"),
            x="overall_pct", y="subject_name", orientation="h",
            color="overall_pct", color_continuous_scale="RdYlGn",
            labels={"overall_pct": "Overall %", "subject_name": ""},
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("**Subjects needing attention (Sem 4, current)**")
        sem4 = marks[marks["semester"] == 4].copy()
        sem4_attend = sem4[["subject_name", "attendance_pct", "ca_pct"]].sort_values("attendance_pct")
        for _, row in sem4_attend.iterrows():
            status = "🔴 Critical" if row["attendance_pct"] < 75 else ("🟡 Warning" if row["attendance_pct"] < 85 else "🟢 Safe")
            st.write(f"{status} — **{row['subject_name']}** — {row['attendance_pct']:.0f}% attendance, CA: {row['ca_pct']:.0f}%")

    st.divider()
    st.markdown("**Grade distribution across all completed semesters**")
    completed = marks.dropna(subset=["grade_point"])
    grade_counts = completed["grade"].value_counts().reindex(["O", "A+", "A", "B+", "B", "C", "D", "E", "F"]).dropna()
    fig2 = px.bar(x=grade_counts.index, y=grade_counts.values,
                  labels={"x": "Grade", "y": "Number of subjects"},
                  color=grade_counts.values, color_continuous_scale="Blues")
    fig2.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig2, use_container_width=True)

# ============================================================
# TAB 2 — Trends
# ============================================================
with tab2:
    st.subheader("How I'm trending over time")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**TGPA across semesters**")
        cgpa_plot = cgpa.dropna(subset=["tgpa"])
        fig3 = px.line(cgpa_plot, x="semester", y="tgpa", markers=True,
                       labels={"semester": "Semester", "tgpa": "TGPA"})
        fig3.update_traces(line_color="#4F8BF9", line_width=3, marker_size=10)
        fig3.update_layout(height=350, yaxis_range=[0, 10])
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        st.markdown("**Cumulative CGPA trend**")
        fig4 = px.line(cgpa_plot, x="semester", y="cumulative_cgpa", markers=True,
                       labels={"semester": "Semester", "cumulative_cgpa": "Cumulative CGPA"})
        fig4.update_traces(line_color="#FF6B6B", line_width=3, marker_size=10)
        fig4.update_layout(height=350, yaxis_range=[0, 10])
        st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    st.markdown("**Average attendance per semester**")
    att_by_sem = attendance.groupby("semester")["attendance_pct"].mean().reset_index()
    fig5 = px.bar(att_by_sem, x="semester", y="attendance_pct",
                  labels={"semester": "Semester", "attendance_pct": "Avg Attendance %"},
                  color="attendance_pct", color_continuous_scale="RdYlGn", range_color=[50, 100])
    fig5.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="75% LPU minimum")
    fig5.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

    st.divider()
    st.markdown("**Attendance vs CA score — is there a correlation?**")
    merged = marks.dropna(subset=["attendance_pct", "ca_pct"])
    fig6 = px.scatter(merged, x="attendance_pct", y="ca_pct", color="semester",
                      size="credits", hover_data=["subject_name"],
                      labels={"attendance_pct": "Attendance %", "ca_pct": "CA Score %"})
    fig6.update_layout(height=400)
    st.plotly_chart(fig6, use_container_width=True)
    corr = merged["attendance_pct"].corr(merged["ca_pct"])
    st.info(f"📊 Correlation coefficient: **{corr:.2f}** — " +
            ("a noticeable positive relationship between attendance and CA scores." if corr > 0.3
             else "a weak relationship — attendance alone doesn't fully explain CA scores."))

# ============================================================
# TAB 3 — What-If Simulator
# ============================================================
with tab3:
    st.subheader("🎯 What if I score X in my remaining Sem 4 exams?")

    sem4 = marks[marks["semester"] == 4].copy()
    st.markdown("Set your **expected ETE score (%)** for each Sem 4 subject:")

    projected_rows = []
    cols = st.columns(2)
    for i, (_, row) in enumerate(sem4.iterrows()):
        with cols[i % 2]:
            target_ete = st.slider(
                f"{row['subject_name']}", 0, 100, 60, key=f"ete_{i}"
            )
        ca = row["ca_pct"] or 0
        mtt = row["mtt_pct"] or 0
        overall = round(ca * 0.3 + mtt * 0.2 + target_ete * 0.5, 2)
        gp = (10 if overall >= 90 else 9 if overall >= 80 else 8 if overall >= 70
              else 7 if overall >= 60 else 6 if overall >= 50 else 5 if overall >= 40 else 0)
        projected_rows.append({
            "subject_name": row["subject_name"], "credits": row["credits"],
            "projected_pct": overall, "projected_gp": gp
        })

    proj_df = pd.DataFrame(projected_rows)
    proj_tgpa = round((proj_df["projected_gp"] * proj_df["credits"]).sum() / proj_df["credits"].sum(), 2)

    st.divider()
    c1, c2 = st.columns([1, 2])
    with c1:
        st.metric("Projected Sem 4 TGPA", f"{proj_tgpa}")
        prev_cgpa = cgpa.dropna(subset=["tgpa"])
        prev_credits = prev_cgpa["total_credits"].sum()
        prev_weighted = (prev_cgpa["tgpa"] * prev_cgpa["total_credits"]).sum()
        sem4_credits = sem4["credits"].sum()
        new_cgpa = round((prev_weighted + proj_tgpa * sem4_credits) / (prev_credits + sem4_credits), 2)
        st.metric("Projected Overall CGPA", f"{new_cgpa}", delta=f"{round(new_cgpa - me['overall_cgpa'], 2)}")

    with c2:
        fig7 = px.bar(proj_df, x="subject_name", y="projected_pct",
                      labels={"subject_name": "", "projected_pct": "Projected %"},
                      color="projected_pct", color_continuous_scale="RdYlGn", range_color=[40, 100])
        fig7.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig7, use_container_width=True)

# ============================================================
# TAB 4 — Peer Benchmarking (Mini-Extension)
# ============================================================
with tab4:
    st.subheader("🤝 How do I compare to my peers?")
    st.caption("Comparing against 3 anonymised profiles: Top Performer, Average Peer, At-Risk Student")

    metrics = ["overall_cgpa", "avg_attendance", "rank_in_section"]
    display_df = students[["name", "profile_type"] + metrics].copy()
    display_df.columns = ["Name", "Type", "CGPA", "Attendance %", "Section Rank"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.divider()

    top = students[students["profile_type"] == "top"].iloc[0]
    st.markdown("### 📊 Gap Analysis — Me vs Top Performer")
    g1, g2, g3 = st.columns(3)
    g1.metric("CGPA gap", f"{top['overall_cgpa'] - me['overall_cgpa']:.2f}", delta_color="inverse")
    g2.metric("Attendance gap", f"{top['avg_attendance'] - me['avg_attendance']:.1f}%", delta_color="inverse")
    g3.metric("Rank gap", f"{int(me['rank_in_section'] - top['rank_in_section'])} positions", delta_color="inverse")

    st.divider()
    st.markdown("### 🕸️ Profile Comparison (Radar Chart)")

    radar_metrics = ["overall_cgpa", "avg_attendance"]
    fig8 = go.Figure()
    colors = {"self": "#4F8BF9", "top": "#2ECC71", "average": "#F39C12", "at_risk": "#E74C3C"}
    for _, row in students.iterrows():
        values = [row["overall_cgpa"] * 10, row["avg_attendance"]]  # scale CGPA to 0-100
        fig8.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=["CGPA (x10)", "Attendance %", "CGPA (x10)"],
            fill='toself', name=row["name"],
            line_color=colors.get(row["profile_type"], "#999")
        ))
    fig8.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=450)
    st.plotly_chart(fig8, use_container_width=True)

    st.divider()
    st.markdown("### 💡 What I need to do to close the gap")
    if me['avg_attendance'] < 75:
        st.warning(f"⚠️ My attendance ({me['avg_attendance']:.0f}%) is below LPU's 75% minimum. This is the single biggest lever — Top Performer maintains {top['avg_attendance']:.0f}%.")
    st.write(f"- Top Performer studies **{top['study_hours_per_day']}/day** vs my **{me['study_hours_per_day']}**")
    st.write(f"- Closing even half the attendance gap could meaningfully lift my CA and MTT scores based on the correlation seen in the Trends tab")

st.divider()
st.caption("Built as part of the 2nd Year B.Tech CSE-AIDE Analytics Engineering Internship · MyTwin · G1")
