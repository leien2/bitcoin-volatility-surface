import pandas as pd
from datetime import datetime
import re
import os

def analyze_option_data(csv_file_path):
    # Reading CSV Files
    df = pd.read_csv(csv_file_path)
    
    # Create a column to store the results
    df['strike_price'] = None
    df['expiry_date'] = None
    df['DTE'] = None
    
    # Current Date
    current_date = datetime.now()
    
    # Month Mapping
    month_dict = {
        'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6,
        'JUL': 7, 'AUG': 8, 'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12
    }
    
    # Process each row of data
    for index, row in df.iterrows():
        try:
            # Extract information from instrument_name (e.g., BTC-16JUN25-111000-P)
            instrument_parts = row['instrument_name'].split('-')

            # Extract strike price
            strike_price = float(instrument_parts[2])
            df.at[index, 'strike_price'] = strike_price
            
            # Extract expiration date and convert to date object
            date_str = instrument_parts[1]  # eg: 16JUN25 or 4JUN25
            
            # Extract day, month, and year using regular expressions
            import re
            match = re.match(r'(\d{1,2})([A-Z]{3})(\d{2})', date_str)
            
            if match:
                day = int(match.group(1))
                month_str = match.group(2)
                year = 2000 + int(match.group(3))
                
                month = month_dict[month_str]
                
                expiry_date = datetime(year, month, day)
                df.at[index, 'expiry_date'] = expiry_date

                # Calculate DTE (Days To Expiration)
                dte = (expiry_date - current_date).days
                df.at[index, 'DTE'] = dte
            else:
                print(f"Unable to parse date format: {date_str}")
        
        except Exception as e:
            print(f"Error processing {row['instrument_name']} : {e}")
    
    # show results
    print("\nOptions data analysis results:")
    print(df[['instrument_name', 'DTE', 'strike_price', 'mark_iv']].head(10))
    print(f"Total {len(df)} records")
    
    return df

# Usage Examples
if __name__ == "__main__":
    # Get the latest CSV file
    data_dir = "option_data"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and not f.endswith('_analyzed.csv')]
    if csv_files:
        latest_csv = sorted(csv_files)[-1]  # Get the latest file by alphabetical order
        csv_path = os.path.join(data_dir, latest_csv)
        print(f"Analyze files: {csv_path}")
        result_df = analyze_option_data(csv_path)

        # Extract specified columns and save as a new CSV file
        selected_columns = ['instrument_name', 'DTE', 'strike_price', 'mark_iv']
        output_df = result_df[selected_columns]

        # Create output file name
        output_file = csv_path.replace('.csv', '_analyzed.csv')

        # Save analysis results
        output_df.to_csv(output_file, index=False)
        print(f"\nAnalysis results saved to: {output_file}")
    else:
        print("No CSV files found")