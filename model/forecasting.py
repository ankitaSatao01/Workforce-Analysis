import mysql.connector
import pandas as pd
from sklearn.linear_model import LinearRegression
from dateutil.relativedelta import relativedelta


# ============================================================
# 1. CONNECT TO MYSQL
# ============================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="workforce_planning"
)


# ============================================================
# 2. READ HISTORICAL WORKFORCE DEMAND
# ============================================================

query = """
    SELECT
        demand_month,
        skill_id,
        required_employees
    FROM workforce_demand
    ORDER BY skill_id, demand_month
"""

df = pd.read_sql(query, db)


print("\n========================================")
print("HISTORICAL WORKFORCE DEMAND")
print("========================================")

print(df)


# ============================================================
# 3. CONVERT DATE TO DATETIME
# ============================================================

df["demand_month"] = pd.to_datetime(df["demand_month"])


# ============================================================
# 4. CREATE MONTH NUMBER
# ============================================================

first_date = df["demand_month"].min()

df["month_number"] = (
    (df["demand_month"].dt.year - first_date.year) * 12
    + (df["demand_month"].dt.month - first_date.month)
)


print("\n========================================")
print("PREPARED DATA")
print("========================================")

print(df)


# ============================================================
# 5. DELETE OLD FORECASTS
# ============================================================

cursor = db.cursor()

cursor.execute("""
    DELETE FROM forecasts
""")

db.commit()

print("\nOld forecasts deleted.")


# ============================================================
# 6. TRAIN MODEL FOR EACH SKILL
# ============================================================

print("\n========================================")
print("AI WORKFORCE FORECASTING")
print("========================================")


for skill_id in df["skill_id"].unique():

    # Get data for current skill
    skill_data = df[df["skill_id"] == skill_id].copy()

    # Input
    X = skill_data[["month_number"]]

    # Output
    y = skill_data["required_employees"]

    # Create model
    model = LinearRegression()

    # Train model
    model.fit(X, y)

    # Last historical month
    last_month_number = skill_data["month_number"].max()

    # Next month number
    next_month_number = last_month_number + 1

    # Predict
    prediction = model.predict(
        [[next_month_number]]
    )[0]

    # Prevent negative prediction
    if prediction < 0:
        prediction = 0

    prediction = round(prediction, 2)


    # ========================================================
    # 7. CALCULATE FORECAST MONTH
    # ========================================================

    last_date = skill_data["demand_month"].max()

    forecast_month = (
        last_date + relativedelta(months=1)
    ).date()


    # ========================================================
    # 8. SAVE FORECAST TO MYSQL
    # ========================================================

    cursor.execute("""
        INSERT INTO forecasts
        (
            forecast_month,
            skill_id,
            predicted_demand,
            model_name
        )
        VALUES (%s, %s, %s, %s)
    """, (
        forecast_month,
        int(skill_id),
        prediction,
        "Linear Regression"
    ))


    print(
        f"Skill ID {skill_id} -> "
        f"Forecast Month: {forecast_month} -> "
        f"Predicted Demand: {prediction}"
    )


# ============================================================
# 9. SAVE ALL CHANGES
# ============================================================

db.commit()


# ============================================================
# 10. CLOSE CONNECTION
# ============================================================

cursor.close()
db.close()


print("\n========================================")
print("FORECASTS SAVED SUCCESSFULLY")
print("========================================")