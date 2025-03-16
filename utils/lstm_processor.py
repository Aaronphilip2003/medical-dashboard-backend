import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from database.connection import client
from typing import List, Tuple
from datetime import datetime

class LSTMPredictor:
    def __init__(self):
        self.model = None
        self.scaler = MinMaxScaler()
        self.n_steps = 7
        self.n_features = None
        
    def prepare_data(self, city: str, disease: str):
        # Query data from database
        query = """
        SELECT 
            date,
            sum(daily_cases) as total_cases,
            avg(temperature) as avg_temp,
            avg(humidity) as avg_humidity,
            avg(rainfall) as avg_rainfall,
            avg(mobility_index) as avg_mobility,
            avg(vaccination_rate) as avg_vaccination,
            avg(social_distancing_index) as avg_social_distancing,
            avg(mask_compliance_rate) as avg_mask_compliance
        FROM disease_timeseries
        WHERE disease_name = '{disease}' 
            AND city = '{city}'
        GROUP BY date
        ORDER BY date
        """.format(disease=disease, city=city)
        
        result = client.query(query)
        
        # Convert to DataFrame
        df = pd.DataFrame(
            result.result_rows,
            columns=['date', 'total_cases', 'avg_temp', 'avg_humidity', 
                    'avg_rainfall', 'avg_mobility', 'avg_vaccination',
                    'avg_social_distancing', 'avg_mask_compliance']
        )
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        
        return df
        
    def train_model(self, df):
        # Scale the data
        scaled_data = self.scaler.fit_transform(df)
        self.n_features = df.shape[1]
        
        # Prepare sequences
        X, y = [], []
        for i in range(len(scaled_data) - self.n_steps):
            X.append(scaled_data[i:(i + self.n_steps)])
            y.append(scaled_data[i + self.n_steps, 0])  # Predict total_cases
            
        X = np.array(X)
        y = np.array(y)
        
        # Create and train model
        self.model = Sequential([
            LSTM(50, activation='relu', input_shape=(self.n_steps, self.n_features), return_sequences=True),
            Dropout(0.2),
            LSTM(50, activation='relu'),
            Dropout(0.2),
            Dense(1)
        ])
        
        self.model.compile(optimizer='adam', loss='mse')
        self.model.fit(X, y, epochs=100, batch_size=32, verbose=0)
        
    def predict_future(self, df: pd.DataFrame, days: int = 30) -> List[Tuple[datetime, float, float, float]]:
        """
        Make future predictions with confidence intervals
        
        Returns:
        List of tuples (date, prediction, lower_bound, upper_bound)
        """
        try:
            # Get the last sequence
            last_sequence = self.scaler.transform(df.iloc[-self.n_steps:])
            
            # Make predictions
            future_predictions = []
            current_sequence = last_sequence.copy()
            
            for _ in range(days):
                # Predict next value
                next_pred = self.model.predict(current_sequence.reshape(1, self.n_steps, self.n_features), verbose=0)
                future_predictions.append(next_pred[0, 0])
                
                # Update sequence
                current_sequence = np.roll(current_sequence, -1, axis=0)
                current_sequence[-1] = np.append(next_pred, current_sequence[-2, 1:])
            
            # Convert predictions back to original scale
            future_scaled = np.concatenate((
                np.array(future_predictions).reshape(-1, 1),
                np.zeros((len(future_predictions), self.n_features-1))
            ), axis=1)
            future_predictions = self.scaler.inverse_transform(future_scaled)[:, 0]
            
            # Calculate confidence intervals (95% confidence)
            std_dev = np.std(future_predictions) * 1.96  # 95% confidence interval
            lower_bound = future_predictions - std_dev
            upper_bound = future_predictions + std_dev
            
            # Ensure lower bound is not negative
            lower_bound = np.maximum(lower_bound, 0)
            
            # Generate future dates
            last_date = df.index[-1]
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1), 
                periods=days, 
                freq='D'
            )
            
            # Return list of tuples with all four values
            return list(zip(
                future_dates,
                future_predictions,
                lower_bound,
                upper_bound
            ))
            
        except Exception as e:
            raise Exception(f"Error making predictions: {str(e)}") 