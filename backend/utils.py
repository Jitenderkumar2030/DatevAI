from prophet import Prophet
import pandas as pd

def preprocess(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.groupby('Date')['Amount'].sum().reset_index()
    df.columns = ['ds', 'y']
    return df

def predict_sales(df):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']]