import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import psycopg2
from fastapi import APIRouter

report = APIRouter(
    prefix="/api/v1"
)


CREDENTIALS_FILE = "/api/report/creds.json"
spreadsheet_id = "1wG6HidwBQFxCUCJMbZnQdwH0OTHTj0awvpTRkMYLxB8"


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize((httplib2.Http()))

service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)



@report.post("/auth/create/otps_report")
async def otps_report():
    conn = psycopg2.connect("dbname='dbtest' user='postgres' host='172.17.0.1' password='1598'")
    cur = conn.cursor()
    gc = gspread.authorize(credentials=credentials)
    sheet = gc.open('OTP')
    cur.execute('SELECT * FROM py_otps')
    rows = cur.fetchall()
    worksheet = sheet.worksheet("OTP")
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            print(i, j, cell)
            worksheet.update_cell(i + 1, j + 1, str(cell))
