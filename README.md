Email a copy of the Boats on Order Report to staff at the dealerships

Cron job to run the first Friday of every month

`02   08 *   *  5     [ $(date +\%d) -le 07 ] && cd /home/fwarren/.venv/smartsheet_monthly_boats_on_order && direnv exec . python smartsheet_monthly_boats_on_order.py >/dev/null 2>&1`
