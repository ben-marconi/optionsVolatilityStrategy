# The files used to get the data were too big to upload on github, 
# but they can be downloaded on https://www.optionsdx.com/product/spx-option-chain/
# 
# To replicate results, download the data for 2022, put the files from the four 
# different quarters in one folder titled spx_option_chain_2022 inside the folder
# called data and run this script to get the options_chain_spx.csv file which 
# is used in the strategy.


import pandas as pd

# Initialize an empty DataFrame to store full option chain data for 2022
option_chain = pd.DataFrame()
# Loop through the files from spy_eod_202201.txt to spy_eod_202212.txt
for month in range(1, 13):
    file_name = f'./data/spx_option_chain_2022/spx_eod_2022{month:02d}.txt'
    csv_data = pd.read_csv(file_name)
    # Append the CSV data to the DataFrame
    option_chain = pd.concat([option_chain, csv_data], ignore_index=True)
option_chain.index = pd.to_datetime(option_chain[' [QUOTE_DATE]'])
option_chain = option_chain[[' [STRIKE]', ' [UNDERLYING_LAST]', ' [C_LAST]', ' [P_LAST]', ' [EXPIRE_DATE]']]
new_column_names = {' [STRIKE]': 'Strike',
                    ' [C_LAST]': 'C_last',
                    ' [P_LAST]': 'P_last',
                    ' [UNDERLYING_LAST]': 'Close',
                    ' [EXPIRE_DATE]': 'Expiry'}
option_chain.rename(columns=new_column_names, inplace=True)
option_chain.rename_axis('Date', inplace = True)
option_chain['Expiry'] = pd.to_datetime(option_chain['Expiry'])
def is_last_day_of_month(row):
    last_trading_days = {
        1: 31,   # January
        2: 28,   # February
        3: 31,   # March
        4: 29,   # April
        5: 31,   # May
        6: 30,   # June
        7: 29,   # July
        8: 31,   # August
        9: 30,   # September
        10: 31,  # October
        11: 30,  # November
        12: 30   # December
    }
    return (
        row['Expiry'].day == last_trading_days.get(row['Expiry'].month)
        and row['Expiry'].month == row.name.month
    )
option_chain = option_chain[option_chain.apply(is_last_day_of_month, axis=1)]
option_chain.to_csv("./data/option_chain_spx.csv", index=True)