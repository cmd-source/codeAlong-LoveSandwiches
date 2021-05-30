import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Function should get the sales data from the user
    """
    while True:
        print("Please enter the sales data from the last market.")
        print("The data should be six numbers seperasted by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Yay data is valid!")
            break

    return sales_data

def validate_data(values):
    """
    Function should convert all strings to integers
    Raises a ValueError if strings cannot be converted into integers or if there is not six integers
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(f"Expected 6 values, you provided {len(values)}")
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True

def update_sales_worksheet(data):
    """
    Function updates a new line of data into the Googlesheets
    """
    print("Updating sales worksheet...")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Function used with sales and stock data to calculate the surplus data
    """
    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock,sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def insert_surplus_data(insert_surplus):
    """
    Function takes the new surplus data and appends it into the google worksheet
    """
    print("Updating the Surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(insert_surplus)
    print("The new surplus data has been added in.\n")


def main(): 
    """
    Run all program functions
    """
  
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    insert_surplus_data(new_surplus_data)

print("welcome to LoveSandwiches")
main()