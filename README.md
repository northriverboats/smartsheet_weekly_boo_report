# Email a copy of the Boats on Order Report to staff at the dealerships

A copy of the pdf of the latest Boats on Order Report for a particular dealership is sent to selected employees at each Dealership as well as selected employees at the factory.

After all these emails are sent a report of what emails were sent and which ones failed or succeeded is sent to selected employees at the factory.

# The .env file
Information is pulled from the `.env` file.

Email addresses are separated by the vertical bar **`|`**

Each dealer is all caps and space replaced with the underscore character **`_`**

| Variable | Description |
| -------- | ----------- |
|`STATUS_REPORT` | is the list of factory employees that are emailed the outcome of this report being run|
|`FACTORY` | is the list of factory employees who recevied a copy of the report along with the staff of each dealership|
|`DEALERS` | is the list of dealer names separated by the vertical bar `|` | 

A sample of the `.env` file layout:
```
SHEET_FOLDER="/dir/to/folder/with/PDF/files/"
STATUS_REPORT='supervisor1@company.com|supervisor2@company.com'
FACTORY='employee1@company.com|employee2@company.com'
DEALERS='Bills Carpet|Taft Plumbing'

BILLS_CARPT='supervisor@billscarpt.com|employye@billscarpt.com'
TAFT_PLUMBING='taft@taftplumbing.com
```

# Command line options
`smartsheet_weekly_boo_report --help`

```
Usage: smartsheet_weekly_boats_on_order.py [OPTIONS]

Options:
  -d, --debug         dont send email
  -e, --exclude TEXT  exclude dealer
  -i, --include TEXT  include only these dealers
  -l, --list          list all dealers
  -v, --verbose       show more details
  --help              Show this message and exit.
```
# Installation
```
pip install -r requirements.txt
pip install git+https://github.com/northriverboats/emailer.git
# remove emailer=1.0.0
# from pip freeze > reqirements.txt
```
# TODO
1. move load_env into function
2. move loadng of gloabals into function 
