import gspread
from datetime import datetime, date, timedelta
from dateutil.rrule import rrule, MONTHLY

def write_to_sheets(google_credentials_file, spreadsheet, worksheet, column_headers, row_data):
    """
    Write data to a Google Sheets worksheet.

    Parameters:
    - google_credentials_file (str): Path to the Google Sheets credentials file.
    - spreadsheet (str): Name of the Google Sheets spreadsheet.
    - worksheet (str): Name of the worksheet within the spreadsheet.
    - column_headers (list): List of column headers.
    - row_data (list): List of lists containing data to be written.

    Returns:
    - None
    """
    # Authenticate with Google Sheets using service account credentials
    gc = gspread.service_account(filename=google_credentials_file)
    sh = gc.open(spreadsheet)
    worksheet = sh.worksheet(worksheet)
    worksheet.clear()

    # Update the first row with column headers
    for i, column_header in enumerate(column_headers):
        worksheet.update_cell(1, i + 1, column_header)
    
    # Append rows of data to the worksheet
    worksheet.append_rows(row_data)

def dates_from_delta(time_delta=30):
    """
    Get start and end dates based on a time delta from the current date.

    Parameters:
    - time_delta (int): Number of days for the time delta.

    Returns:
    - start_date, end_date (tuple): Start and end dates in ISO 8601 format.
    """
    start_date = str(date.today() - timedelta(days=time_delta)) + "T00:00:00Z"
    end_date = str(date.today()) + "T00:00:00Z"
    return start_date, end_date

def dates_formatted(start=None, end=None):
    """
    Format start and end dates in ISO 8601 format.

    Parameters:
    - start (str): Start date.
    - end (str): End date.

    Returns:
    - start_date, end_date (tuple): Formatted start and end dates in ISO 8601 format.
    """
    # Use default start date if not provided
    start_date = str(start) + "T00:00:00Z" if start else str(date.today() - timedelta(days=30)) + "T00:00:00Z"
    
    # Use default end date if not provided
    end_date = str(end) + "T23:59:59Z" if end else str(date.today()) + "T23:59:59Z"

    return start_date, end_date

def month_map(year=None):
    """
    Generate a mapping of start and end dates for each month in a given year.

    Parameters:
    - year (str): Year for which to generate the mapping.

    Returns:
    - months (dict): Dictionary mapping start dates to end dates for each month.
    """
    if year:
        start_year = year
        end_year = str(int(year) + 1)
    else:
        start_year = str(date.today().year)
        end_year = str(int(start_year) + 1)

    start = "%s-2-1" % (start_year)
    end = "%s-1-31" % (end_year)
    start_date = datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.strptime(end, '%Y-%m-%d').date()

    months = {}

    start_dates = [date for date in rrule(MONTHLY, bymonthday=1, dtstart=start_date, until=end_date)]
    end_dates = [date for date in rrule(MONTHLY, bymonthday=-1, dtstart=start_date, until=end_date)]

    for n in range(len(start_dates)):
        date_format = "%Y-%m-%d %H:%M:%S"
        start_date = str(datetime.date(datetime.strptime(str(start_dates[n]), date_format))) + "T00:00:00Z"
        end_date = str(datetime.date(datetime.strptime(str(end_dates[n]), date_format))) + "T23:59:59Z"

        months[start_date] = end_date

    return months

def filter_by_slug(invites, demo_list, start=None, end=None):
    """
    Filter invites based on track slugs and date range.

    Parameters:
    - invites (dict): Dictionary containing invitation data.
    - demo_list (list): List of demo track slugs.
    - start (str): Start date for filtering.
    - end (str): End date for filtering.

    Returns:
    - invite_data (list): List of lists containing filtered invitation data.
    """
    start_date = start if start else "2000-01-01"
    end_date = end if end else str(date.today())
    
    filtered_invites = []
    for invite in invites["trackInvites"]:
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        created_date = datetime.date(datetime.strptime(invite["created"], date_format))
        check_start = datetime.strptime(start_date, '%Y-%m-%d').date()
        check_end = datetime.strptime(end_date, '%Y-%m-%d').date()
        if created_date >= check_start and created_date <= check_end:
            slugs = []
            for slug in invite["tracks"]:
                slugs.append(slug["slug"])
            if any(slug in demo_list for slug in slugs):
                filtered_invites.append(invite)

    invite_data = []
    for invite in filtered_invites:
        track_id = invite["id"]
        title = invite["title"] if invite["title"] != "" else invite["publicTitle"]
        invite_count = invite["inviteCount"]
        created_date = invite["created"]
        tracks = ", ".join([track["slug"] for track in invite["tracks"]])
        row = [track_id, title, invite_count, created_date, tracks]
        invite_data.append(row)
    return invite_data
