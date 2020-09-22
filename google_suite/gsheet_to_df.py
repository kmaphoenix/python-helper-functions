import pandas as pd
import logging
import google.auth
import gspread

# logging config
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

def gsheet_connect(creds_path,ss_name):
  """
  This function performs gsuite authentication, connects to GSheets,
  and returns a Spreadsheet Object.

  Make sure you have enabled API access and created an Oauth client per the 
  instructions here: https://gspread.readthedocs.io/en/latest/oauth2.html#for-end-users-using-oauth-client-id
  """
  # gc = gspread.service_account(filename=creds_path)
  gc = gspread.oauth()

  ss = gc.open(ss_name)
  logging.info("Successfully connected to spreadsheet: {}".format(ss_name))

  return ss

def get_sheet_data(ss,ws_name):
  """
  This function connects to a specific worksheet in the spreadsheet the converts
  all values into a dataframe
  """
  # Connect to a specific worksheet in the spreadsheet
  worksheet = ss.worksheet(ws_name)

  # Pull the data as dictionary, with header row as keys
  data = worksheet.get_all_records(head=1)

  # Write data to Pandas DataFrame
  df = pd.DataFrame.from_dict(data)
  logging.info("Successfully pulled worksheet \'{}\' into dataframe".format(ws_name))
  logging.info("{} records in dataframe".format(df.shape[0]))

  return df

if __name__ == "__main__":
  ss_name = 'YOUR_SPREADSHEET_HERE'
  ws_name = 'YOUR_WORKSHEET_HERE'
  creds_path = 'gsheet_creds.json'

  ss = gsheet_connect(creds_path,ss_name)
  df = get_sheet_data(ss,ws_name)