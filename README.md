# Athlete Risk & Decision Engine

A Python-based athlete monitoring decision-support system that combines training load, readiness, wellness and performance data to classify athlete status and generate monitoring actions.

## Objective

The system transforms athlete monitoring data into an automated decision-support workflow.

It evaluates:

- Training load
- Training-load change
- Readiness
- Wellness
- Performance

and produces:

- Athlete status
- Decision score
- Load status
- Recommended monitoring action

## Data Flow

```text
Athlete Monitoring
       ↓
Data Validation
       ↓
Feature Engineering
       ↓
Decision Rules
       ↓
Decision Score
       ↓
Athlete Status
       ↓
Recommended Action
```

## Dataset

The sample dataset contains longitudinal observations from four athletes.

### Variables

| Variable | Description |
|---|---|
| Athlete | Athlete identifier |
| Date | Observation date |
| Training_Load | Training load in arbitrary units |
| Sleep_Quality | Subjective sleep-quality score |
| Wellness_Score | Wellness score |
| Readiness_Score | Readiness percentage |
| Performance_Score | Performance score |

## Decision Framework

The system combines three primary athlete-state domains:

```text
Readiness
   +
Wellness
   +
Performance
   -
Excessive Load Increase
   ↓
Decision Score
```

### Readiness

```text
85 or higher → 2 points
70–84        → 1 point
Below 70     → 0 points
```

### Wellness

```text
17 or higher → 2 points
13–16        → 1 point
Below 13     → 0 points
```

### Performance

```text
88 or higher → 2 points
80–87        → 1 point
Below 80     → 0 points
```

### Training Load

A training-load increase above 25% creates a penalty.

An increase above 40% creates an additional penalty.

## Athlete Status

```text
Score ≥ 5  → READY

Score 2–4  → CAUTION

Score < 2   → REVIEW
```

## Recommended Actions

### READY

Proceed with planned training while continuing normal monitoring.

### CAUTION

Review training load, recovery and athlete response before progressing.

### REVIEW

Review athlete status before progressing the planned training load.

## Important Limitation

This decision framework is an educational rule-based example.

It is not a validated injury-risk model, medical assessment, or universal training prescription.

Real-world athlete decisions should incorporate:

- Individual baselines
- Measurement reliability
- Training phase
- Competition schedule
- Athlete history
- Injury status
- Recovery
- Coaching context
- Performance trends

## Technologies

- Python
- Pandas
- Matplotlib
- CSV
- Conditional logic
- Feature engineering
- Rule-based decision systems
- Automated reporting

## Installation

```bash
pip install pandas matplotlib
```

## Running the Project

Place the Python script and CSV dataset in the same directory.

Run:

```bash
python athlete_decision_engine.py
```

## Generated Outputs

```text
athlete_decision_results.csv
athlete_status_summary.csv
athlete_status_distribution.png
```

## Sports Science Applications

Potential applications include:

- Athlete monitoring
- Strength and conditioning
- Training-load monitoring
- Readiness monitoring
- Performance support
- Coaching decision support
- Sports analytics

## Future Development

The rule-based system can later be extended with:

- Individual baselines
- Z-scores
- Acute and chronic load
- Rolling averages
- GPS metrics
- Heart-rate metrics
- Force-plate metrics
- Jump testing
- Velocity-based training
- Machine-learning predictions
- Explainable AI
- Automated alerts
- Athlete dashboards
- Agentic decision-support systems

## Skills Demonstrated

```text
Python
   ↓
Pandas
   ↓
Data Validation
   ↓
Feature Engineering
   ↓
Decision Rules
   ↓
Classification
   ↓
Automated Reporting
   ↓
Sports Performance Decision Support
```

## Author

**Abhishek Tomar**

Strength & Conditioning | Sports Performance | Sports Analytics | Python

## License

MIT License