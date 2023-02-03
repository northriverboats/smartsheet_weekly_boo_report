#!/usr/bin/env python3

# email PDF version of the Boats on order report to each dealer

import datetime
import logging
import os
import shutil
import sys
import time
import click
from dotenv import load_dotenv
from emailer import mail_results


# Setup Logging
class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record):
        result = super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        return result



# load environmental variables
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

env_path = resource_path('.env')
load_dotenv(dotenv_path=env_path)

# GLOBALS start here
all_dealers = os.getenv('DEALERS').split('|')
users = {key: os.getenv(
              key.upper().replace(' ', '_').replace('.','')).split('|')
         for key in all_dealers+['Factory']}
debug = False
verbose = False
log_text = ""

plain_text_template = \
"""%s,\nPlease review the %s Boats on Order.\n\nThank you,\n\n
Joe Depweg\n
North River Boats\n
541-673-2438\n
joed@northriverboats.com\n
www.northriverboats.com\n"""

html_text_template = \
"""<div style="font-size: 11.0pt; font-family:'Calibri',sans-serif"><p>%s,</p>
<p>Please review the %s Boats on Order.</p><p>Thank you,</p></div>
<p style="line-height: 95%%; font-size:11.0pt; font-family:'Calibri',sans-serif; color: #1F497D">
Joe Depweg<br />
North River Boats<br />
541-673-2438<br />
<a href="mailto:joed@northriverboats.com" style="color:#0563C1; text-decoration:underline;">joed@northriverboats.com</a><br />
www.northriverboats.com<br />
</p>"""
# GLOBALS end here


# HELPER functions
def set_debug(flag):
    global debug
    debug = flag

def set_dry(flag):
    global dry
    dry = flag

def set_verbose(flag):
    global verbose
    verbose = flag

def log(text):
    global log_text
    if debug or verbose:
        click.echo(text)
    log_text += text + "\n"


# CODE starts here
def send_email(recipient, subject, plain_text, html_text, attachment=None):
    if debug: return  # do not send email if debug
    if not recipient: return  # do not send if no adressee
    mail_results(subject, html_text, text=plain_text,
                 recipient=recipient,attachment=attachment)


def email_dealership(dealership, email_list, plain_text, html_text, attachment):
    subject = 'Automated %s Boats on Order Report for %s' % (dealership, datetime.date.today().strftime('%B %d, %Y'))
    for recipient in email_list[:]:
        status = 'sent' if not debug else 'skipped on debug'
        try:
            send_email(recipient, subject, plain_text, html_text, attachment)
        except:
            status = 'failed'
        log('    Emailing:   {:.<36}'.format(recipient) + ' ' + status)

def email_dealerships(dealership):
    logging.info(dealership)
    # add factory empoloyees to store employees to email
    email_list = users[dealership][:] + users['Factory']
    # generate txt and html versions of message
    plain_text = plain_text_template % (dealership, datetime.date.today().strftime('%B %d, %Y'))
    html_text = html_text_template % (dealership, datetime.date.today().strftime('%B %d, %Y'))
    # find attachement file
    source = os.getenv('SHEET_FOLDER') + dealership.replace('.', '') + ' - Boats on Order.pdf'
    # print list of dealership employees to email
    if debug or verbose:
        click.echo('    Send To:    ', nl=False)
        click.echo(users[dealership])
    # if file cant be found skip 
    if os.path.isfile(source):
        logging.info(f'    Found:      {source}')
    else:
        logging.warning(f'    Not found:   {source}')
        return
    try:
        # copy sheet to /tmp - if copy fails then error out on whole store with no attachment
        attachment = '/tmp/' + dealership.replace('.', '') + ' - Boats on Order.pdf'
        shutil.copy(source, attachment)
        logging.info(f'    Copying:     {attachment}')
        email_dealership(dealership, email_list, plain_text, html_text, attachment)
        logging.info(f'    Deleting:    {attachment}')
        os.remove(attachment)
    except IOError:
        logging.error('Can\'t copy:  {source}')
    except Exception as e:
        logging.error(str(e))

def process_boo(dealers):
    logging.info('Processing Dealerships')
    for dealer in dealers:
        try:
            email_dealerships(dealer)
        except Exception as e:
            logging.error(str(e))
    # Send status report
    for recepient in os.getenv('STATUS_REPORT').split('|'):
        logging.info(f"{('Sending', 'Not Sending')[debug]} Status Report to: {recepient}")
        if debug:
            continue
        send_email(recepient, 'Smartsheet Weekly Boats On Order Report Status', log_text, f"<pre>\n{log_text}</pre>\n")


@click.command()
@click.option('--debug', '-d', is_flag=True, help='dont send email')
@click.option('--exclude', '-e', multiple=True, help='exclude dealer')
@click.option('--include', '-i', multiple=True, help='include only these dealers')
@click.option('--list', '-l', is_flag=True, help='list all dealers')
@click.option('--verbose', '-v', is_flag=True, help='show more details')
def cli(debug, exclude, include, list, verbose):
    set_debug(debug)
    set_verbose(verbose)
    dealers = all_dealers[:]
    if (include):
        dealers = [ dealer for dealer in all_dealers if dealer in include]
    dealers = [dealer for dealer in dealers  if dealer not in exclude]
    if (list):
        for dealer in dealers:
            click.echo(dealer)
        return
    process_boo(dealers)

# Start Logging
handler = logging.StreamHandler()
formatter = OneLineExceptionFormatter(logging.BASIC_FORMAT)
handler.setFormatter(formatter)
root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)

if __name__ == '__main__':
    try:
        exit(cli())
    except Exception:
        logging.exception("Exception in cli()/main(): ")
        exit(1)

