Email a copy of the Boats on Order Report to staff at the dealerships

information is pulled from the .env file.
email addresses are separated by the vertical bar |

STATUS_REPORT is the list of factory employees that are emailed the outcome of this report being run

FACTORY is the list of factory employees who recevie a copy of the report along with the staff of each dealership

DEALERS is the list of dealer names separated by the vertical bar |

each dealer is all caps and space replaced with the underscore character

A sample of the .env file layout
```
SHEET_FOLDER="/dir-to-folder/"
STATUS_REPORT='supervisor1@company.com|supervisor2@company.com'
FACTORY='employee1@company.com|employee2@company.com'
DEALERS='Bills Carpet|Taft Plumbing'

BILLS_CARPT='supervisor@billscarpt.com|employye@billscarpt.com'
TAFT_PLUMBING='taft@taftplumbing.com
```

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

