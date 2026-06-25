import pandas as pd
import random

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

ROLES = [
    "Python Developer",
    "Data Scientist",
    "AI Engineer"
]

LOCATIONS = [
    "Hyderabad",
    "Bangalore",
    "Pune"
]


def generate_data():

    data = []

    for _ in range(1000):

        role = random.choice(ROLES)

        exp = random.randint(0, 10)

        location = random.choice(LOCATIONS)

        base = {
            "Python Developer": 800000,
            "Data Scientist": 1200000,
            "AI Engineer": 1800000
        }[role]

        salary = base + (exp * 100000)

        data.append([
            role,
            exp,
            location,
            salary
        ])

    return pd.DataFrame(
        data,
        columns=[
            "Role",
            "Experience",
            "Location",
            "Salary"
        ]
    )


def train_model():

    df = generate_data()

    role_encoder = LabelEncoder()
    location_encoder = LabelEncoder()

    df["Role"] = role_encoder.fit_transform(df["Role"])
    df["Location"] = location_encoder.fit_transform(df["Location"])

    X = df[[
        "Role",
        "Experience",
        "Location"
    ]]

    y = df["Salary"]

    model = RandomForestRegressor()

    model.fit(X, y)

    return model