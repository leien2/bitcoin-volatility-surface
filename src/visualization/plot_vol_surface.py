import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from scipy.interpolate import griddata

def plot_volatility_surface(input_file, output_file):
    """
    Plot a smoothed 3D surface of volatility
    """
    try:
        # Get the current date
        today = pd.Timestamp.now()

        # Read data
        df = pd.read_csv(input_file)

        # Data preprocessing: Keep DTE >= 0
        df = df[df['DTE'] >= 0]

        # Ensure correct types to avoid string types
        df['strike_price'] = pd.to_numeric(df['strike_price'])
        df['mark_iv'] = pd.to_numeric(df['mark_iv'])
        df['DTE'] = pd.to_numeric(df['DTE'])
        # Prepare 3D data
        X = df['strike_price'].values
        Y = df['DTE'].values
        Z = df['mark_iv'].values

        # Create grid points
        xi = np.linspace(X.min(), X.max(), 50)
        yi = np.linspace(Y.min(), Y.max(), 20)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolation
        zi = griddata(
            points=(X, Y),
            values=Z,
            xi=(xi, yi),
            method='cubic',  # Use cubic interpolation
            fill_value=np.nan
        )

        # Create 3D plot
        fig = go.Figure(data=[
            # Main surface - directly connect data points
            go.Mesh3d(
                x=X,
                y=Y,
                z=Z,
                colorscale='Viridis',
                opacity=0.8,
                name='Volatility Surface'
            ),

            # Data point markers
            go.Scatter3d(
                x=X,
                y=Y,
                z=Z,
                mode='markers',
                marker=dict(size=4, color='red', opacity=0.8),
                name='Actual Data Points'
            )
        ])

        # Update layout
        fig.update_layout(
            title='Bitcoin Options Volatility Surface',
            scene=dict(
                xaxis_title='Strike Price (USD)',
                yaxis_title='Days to Expiration',
                zaxis_title='Implied Volatility (%)',
                camera=dict(
                    up=dict(x=0, y=0, z=1),
                    center=dict(x=0, y=0, z=0),
                    eye=dict(x=2, y=2, z=1.5)
                )
            ),
            width=1200,
            height=900
        )

        # Save and display the plot
        fig.write_html(output_file)
        fig.show()

        print(f"Volatility surface plot saved to: {output_file}")
        return True

    except Exception as e:
        print(f"Error plotting volatility surface: {e}")
        return False

if __name__ == "__main__":
    # Set input and output file paths
    input_file = '../data/option_data/BTC_option_instruments_20250615_055819_analyzed.csv'
    output_file = 'volatility_surface.html'

    # Plot volatility surface
    plot_volatility_surface(input_file, output_file)