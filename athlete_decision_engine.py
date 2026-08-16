import pandas as pd
import matplotlib.pyplot as plt


print("=" * 80)
print("             ATHLETE RISK & DECISION ENGINE")
print("=" * 80)


# ------------------------------------------
# Load Data
# ------------------------------------------

data = pd.read_csv(
    "athlete_monitoring_data.csv"
)

data["Date"] = pd.to_datetime(
    data["Date"]
)

data = data.sort_values(
    ["Athlete", "Date"]
).reset_index(drop=True)


# ------------------------------------------
# Data Validation
# ------------------------------------------

print("\n" + "=" * 80)
print("DATA VALIDATION")
print("=" * 80)

print(f"Rows           : {len(data)}")
print(f"Columns        : {len(data.columns)}")
print(
    f"Missing values : "
    f"{data.isnull().sum().sum()}"
)


# ------------------------------------------
# Create Load Change
# ------------------------------------------

data["Previous_Load"] = (
    data.groupby("Athlete")["Training_Load"]
    .shift(1)
)

data["Load_Change_%"] = (
    (
        data["Training_Load"]
        -
        data["Previous_Load"]
    )
    /
    data["Previous_Load"]
) * 100


data["Load_Change_%"] = (
    data["Load_Change_%"]
    .fillna(0)
)


# ------------------------------------------
# Create Training Load Status
# ------------------------------------------

def classify_load(row):

    load_change = row["Load_Change_%"]

    if load_change > 25:
        return "High Load Increase"

    elif load_change < -25:
        return "Large Load Reduction"

    else:
        return "Stable Load"


data["Load_Status"] = data.apply(
    classify_load,
    axis=1
)


# ------------------------------------------
# Readiness Status
# ------------------------------------------

def classify_readiness(readiness):

    if readiness >= 85:
        return "High"

    elif readiness >= 70:
        return "Moderate"

    else:
        return "Low"


data["Readiness_Status"] = (
    data["Readiness_Score"]
    .apply(classify_readiness)
)


# ------------------------------------------
# Wellness Status
# ------------------------------------------

def classify_wellness(wellness):

    if wellness >= 17:
        return "High"

    elif wellness >= 13:
        return "Moderate"

    else:
        return "Low"


data["Wellness_Status"] = (
    data["Wellness_Score"]
    .apply(classify_wellness)
)


# ------------------------------------------
# Performance Status
# ------------------------------------------

def classify_performance(performance):

    if performance >= 88:
        return "High"

    elif performance >= 80:
        return "Moderate"

    else:
        return "Low"


data["Performance_Status"] = (
    data["Performance_Score"]
    .apply(classify_performance)
)


# ------------------------------------------
# Decision Score
# ------------------------------------------

data["Decision_Score"] = 0


data.loc[
    data["Readiness_Score"] >= 85,
    "Decision_Score"
] += 2


data.loc[
    (
        (data["Readiness_Score"] >= 70)
        &
        (data["Readiness_Score"] < 85)
    ),
    "Decision_Score"
] += 1


data.loc[
    data["Wellness_Score"] >= 17,
    "Decision_Score"
] += 2


data.loc[
    (
        (data["Wellness_Score"] >= 13)
        &
        (data["Wellness_Score"] < 17)
    ),
    "Decision_Score"
] += 1


data.loc[
    data["Performance_Score"] >= 88,
    "Decision_Score"
] += 2


data.loc[
    (
        (data["Performance_Score"] >= 80)
        &
        (data["Performance_Score"] < 88)
    ),
    "Decision_Score"
] += 1


# ------------------------------------------
# Load Penalty
# ------------------------------------------

data.loc[
    data["Load_Change_%"] > 25,
    "Decision_Score"
] -= 2


data.loc[
    data["Load_Change_%"] > 40,
    "Decision_Score"
] -= 1


# ------------------------------------------
# Athlete Status
# ------------------------------------------

def classify_status(score):

    if score >= 5:
        return "READY"

    elif score >= 2:
        return "CAUTION"

    else:
        return "REVIEW"


data["Athlete_Status"] = (
    data["Decision_Score"]
    .apply(classify_status)
)


# ------------------------------------------
# Recommended Action
# ------------------------------------------

def recommend_action(row):

    status = row["Athlete_Status"]

    if status == "READY":

        return (
            "Proceed with planned training "
            "and continue monitoring."
        )

    elif status == "CAUTION":

        return (
            "Review training load, recovery "
            "and athlete response."
        )

    else:

        return (
            "Review athlete status before "
            "progressing planned load."
        )


data["Recommended_Action"] = data.apply(
    recommend_action,
    axis=1
)


# ------------------------------------------
# Display Results
# ------------------------------------------

print("\n" + "=" * 80)
print("ATHLETE DECISION RESULTS")
print("=" * 80)

columns_to_display = [
    "Athlete",
    "Date",
    "Training_Load",
    "Readiness_Score",
    "Wellness_Score",
    "Performance_Score",
    "Load_Status",
    "Athlete_Status",
    "Recommended_Action"
]

print(
    data[
        columns_to_display
    ].to_string(index=False)
)


# ------------------------------------------
# Latest Athlete Status
# ------------------------------------------

latest = (
    data.sort_values("Date")
    .groupby("Athlete")
    .tail(1)
    .copy()
)


print("\n" + "=" * 80)
print("LATEST ATHLETE STATUS")
print("=" * 80)

for _, row in latest.iterrows():

    print(
        f"\nAthlete       : {row['Athlete']}"
    )

    print(
        f"Training Load : "
        f"{row['Training_Load']} AU"
    )

    print(
        f"Readiness     : "
        f"{row['Readiness_Score']}%"
    )

    print(
        f"Wellness      : "
        f"{row['Wellness_Score']}/20"
    )

    print(
        f"Performance   : "
        f"{row['Performance_Score']}"
    )

    print(
        f"Status        : "
        f"{row['Athlete_Status']}"
    )

    print(
        f"Action        : "
        f"{row['Recommended_Action']}"
    )


# ------------------------------------------
# Athlete Summary
# ------------------------------------------

summary = (
    data.groupby("Athlete")
    .agg(
        Average_Load=(
            "Training_Load",
            "mean"
        ),

        Average_Readiness=(
            "Readiness_Score",
            "mean"
        ),

        Average_Wellness=(
            "Wellness_Score",
            "mean"
        ),

        Average_Performance=(
            "Performance_Score",
            "mean"
        ),

        Ready_Count=(
            "Athlete_Status",
            lambda x:
            (x == "READY").sum()
        ),

        Caution_Count=(
            "Athlete_Status",
            lambda x:
            (x == "CAUTION").sum()
        ),

        Review_Count=(
            "Athlete_Status",
            lambda x:
            (x == "REVIEW").sum()
        )
    )
    .reset_index()
)


print("\n" + "=" * 80)
print("ATHLETE SUMMARY")
print("=" * 80)

print(
    summary.to_string(
        index=False,
        formatters={
            "Average_Load":
                "{:.1f}".format,

            "Average_Readiness":
                "{:.1f}".format,

            "Average_Wellness":
                "{:.1f}".format,

            "Average_Performance":
                "{:.1f}".format
        }
    )
)


# ------------------------------------------
# Status Distribution
# ------------------------------------------

status_counts = (
    data["Athlete_Status"]
    .value_counts()
)


plt.figure(
    figsize=(8, 6)
)

status_counts.plot(
    kind="bar"
)

plt.title(
    "Athlete Status Distribution"
)

plt.xlabel(
    "Athlete Status"
)

plt.ylabel(
    "Number of Observations"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

plt.savefig(
    "athlete_status_distribution.png",
    dpi=300
)

plt.show()


# ------------------------------------------
# Export Results
# ------------------------------------------

data.to_csv(
    "athlete_decision_results.csv",
    index=False
)

summary.to_csv(
    "athlete_status_summary.csv",
    index=False
)


# ------------------------------------------
# Final Output
# ------------------------------------------

print("\n" + "=" * 80)
print("DECISION ENGINE COMPLETE")
print("=" * 80)

print("Generated files:")

print("1. athlete_decision_results.csv")
print("2. athlete_status_summary.csv")
print("3. athlete_status_distribution.png")

print("\n" + "=" * 80)
print("MONITOR • ANALYZE • CLASSIFY • DECIDE")
print("=" * 80)