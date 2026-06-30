"""
data_loader.py — Loads and cleans MyTwin data from the raw Excel files.
Handles LPU-specific quirks: CA as "x/100" text, mixed attendance formats, etc.
"""

import pandas as pd
import re
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), "data", "raw")


def _parse_fraction(val):
    """Convert 'x/100' style strings to a float. Returns None for '-' or NaN."""
    if pd.isna(val):
        return None
    val = str(val).strip()
    if val in ("-", "", "nan"):
        return None
    if "/" in val:
        try:
            num, denom = val.split("/")
            return round(float(num) / float(denom) * 100, 2)
        except Exception:
            return None
    try:
        return float(val)
    except Exception:
        return None


def _normalize_attendance(val):
    """Attendance comes as 0.95 (sem1/2/4) or 1 (sem3, meaning 100%). Normalize to %."""
    if pd.isna(val):
        return None
    val = str(val).strip()
    if val in ("-", "", "nan"):
        return None
    val = float(val)
    if val <= 1:
        return round(val * 100, 1)
    return round(val, 1)


GRADE_POINTS = {"O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "D": 4, "E": 2, "F": 0}


def load_marks():
    """Load all 4 semesters of marks, clean and combine into one DataFrame."""
    frames = []
    for sem in [1, 2, 3, 4]:
        path = os.path.join(RAW_DIR, f"marks_sem{sem}_A.xlsx")
        df = pd.read_excel(path)
        df.columns = [c.strip().lower() for c in df.columns]

        df["ca_pct"] = df["ca"].apply(_parse_fraction)
        df["mtt_pct"] = df["mtt"].apply(_parse_fraction)
        df["ete_pct"] = df["ete"].apply(_parse_fraction)
        df["attendance_pct"] = df["attendance_pct"].apply(_normalize_attendance)
        df["grade"] = df["grade"].astype(str).str.strip().replace("nan", None)
        df["grade_point"] = df["grade"].map(GRADE_POINTS)

        # overall % score per subject (weighted: CA 30%, MTT 20%, ETE 50% — approx LPU pattern)
        def overall(row):
            parts, weights = [], []
            if row["ca_pct"] is not None:
                parts.append(row["ca_pct"]); weights.append(0.3)
            if row["mtt_pct"] is not None:
                parts.append(row["mtt_pct"]); weights.append(0.2)
            if row["ete_pct"] is not None:
                parts.append(row["ete_pct"]); weights.append(0.5)
            if not parts:
                return None
            total_w = sum(weights)
            return round(sum(p * w for p, w in zip(parts, weights)) / total_w, 2)

        df["overall_pct"] = df.apply(overall, axis=1)
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    return combined


def load_attendance():
    frames = []
    for sem in [1, 2, 3, 4]:
        path = os.path.join(RAW_DIR, f"attendance_sem{sem}_A.xlsx")
        df = pd.read_excel(path)
        df.columns = [c.strip().lower() for c in df.columns]
        df["attendance_pct"] = df["attendance_pct"].apply(_normalize_attendance)
        df["classes_held"] = pd.to_numeric(df["classes_held"], errors="coerce")
        df["classes_attended"] = pd.to_numeric(df["classes_attended"], errors="coerce")
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    return combined


def load_cgpa_summary():
    path = os.path.join(RAW_DIR, "cgpa_summary_A.xlsx")
    df = pd.read_excel(path)
    df.columns = [c.strip().lower() for c in df.columns]
    # Compute cumulative CGPA as running credit-weighted avg of TGPA
    df = df.sort_values("semester")
    df["cum_credits"] = df["total_credits"].cumsum()
    df["weighted"] = df["tgpa"] * df["total_credits"]
    df["cumulative_cgpa"] = (df["weighted"].cumsum() / df["cum_credits"]).round(2)
    return df


def _normalize_pct(val):
    """Handle the mixed 0.82 vs 98.25 format in students file."""
    if pd.isna(val):
        return None
    val = float(val)
    if val <= 1:
        return round(val * 100, 1)
    return round(val, 1)


def load_students():
    path = os.path.join(RAW_DIR, "students__1__A.xlsx")
    df = pd.read_excel(path)
    df.columns = [c.strip().lower() for c in df.columns]
    df["avg_attendance"] = df["avg_attendance"].apply(_normalize_pct)

    # Fill overall_cgpa for self (S001) using avg of available semester CGPAs
    sem_cols = ["sem1_cgpa", "sem2_cgpa", "sem3_cgpa", "sem4_cgpa"]
    mask = df["overall_cgpa"].isna()
    df.loc[mask, "overall_cgpa"] = df.loc[mask, sem_cols].mean(axis=1).round(2)
    return df


if __name__ == "__main__":
    print("=== MARKS ===")
    m = load_marks()
    print(m[["semester", "subject_name", "ca_pct", "mtt_pct", "ete_pct", "overall_pct", "grade", "grade_point"]])

    print("\n=== ATTENDANCE ===")
    a = load_attendance()
    print(a[["semester", "subject_name", "attendance_pct"]])

    print("\n=== CGPA SUMMARY ===")
    c = load_cgpa_summary()
    print(c)

    print("\n=== STUDENTS ===")
    s = load_students()
    print(s)
