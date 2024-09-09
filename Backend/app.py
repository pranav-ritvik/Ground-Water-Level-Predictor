from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load the datasets
rainfall_df = pd.read_csv('reshaped_rainfall_levels.csv')
groundwater_df = pd.read_csv('reshaped_groundwater_levels.csv')

# Merge the datasets on 'year_month' and 'location'
merged_df = pd.merge(rainfall_df, groundwater_df, on=['year_month', 'location'])

# Convert 'year_month' to a datetime object and extract year and month
merged_df['year_month'] = pd.to_datetime(merged_df['year_month'])
merged_df['year'] = merged_df['year_month'].dt.year
merged_df['month'] = merged_df['year_month'].dt.month

# Drop the original 'year_month' column if not needed
merged_df = merged_df.drop(columns=['year_month'])

# Features and target
X = merged_df[['location', 'rainfall_level', 'year', 'month']]
y = merged_df['groundwater_level']

# Define the encoder and model pipeline
encoder = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), ['location']),
        ('num', StandardScaler(), ['rainfall_level', 'year', 'month'])
    ]
)

model = Pipeline(steps=[
    ('encoder', encoder),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Save the model to disk (optional)
joblib.dump(model, 'groundwater_model.pkl')

# Load the model (optional, if not training every time)
# model = joblib.load('groundwater_model.pkl')

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    year_month = data['year_month']
    location = data['location']
    rainfall_level = data['rainfall_level']
    
    # Convert 'year_month' to datetime and extract year and month
    date = pd.to_datetime(year_month)
    year = date.year
    month = date.month
    
    # Create a DataFrame with the input data
    input_df = pd.DataFrame({
        'location': [location],
        'rainfall_level': [rainfall_level],
        'year': [year],
        'month': [month]
    })
    
    # Make the prediction
    prediction = model.predict(input_df)
    
    return jsonify({'predicted_groundwater_level': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
