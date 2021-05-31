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

def updating_worksheet(data,worksheet):
    """
    Function takes new data and supplies it into the google sheet
    """
    print(f"updating the {worksheet}...\n")
    new_data = SHEET.worksheet(worksheet)
    new_data.append_row(data)
    print(f"The new data {data} has been successfully added to the {worksheet}.")

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

def get_last_5_sales_enteries():
    """
    Retrieves the last 5 sanwich sales
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns 
    




def calculate_stock_data(data):
    """
    calculate the stock data for each sandwich item and add 10%
    """

    print("Calculating the stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/len(int_column)
        new_stock = average * 1.1
        new_stock_data.append(round(new_stock))

    return new_stock_data


def get_stock_values(data):
    """
    Retrieves the first 5 headings
    """
    stock_data = SHEET.worksheet("stock")

    headings = []
    for ind in range(1,7):
        heading = stock_data.col_values(ind)
        headings.append(heading[0])
    print(headings) 

def main(): 
    """
    Run all program functions
    """
  
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    updating_worksheet(sales_data,"sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    updating_worksheet(new_surplus_data,"surplus")
    sales_columns = get_last_5_sales_enteries()
    stock_data = calculate_stock_data(sales_columns)
    print("the new stock data is: "f"{stock_data}")
    updating_worksheet(stock_data,"stock")
    print("The stock headings are:\n")
    get_stock_values(stock_data)

print("welcome to LoveSandwiches")
main()
