
from jinja2 import Environment, FileSystemLoader,select_autoescape
from jinja_markdown import MarkdownExtension
import os
import time
from helpers import *
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(project_dir)
template_dir=os.path.join(project_dir, "bugzilla-reports-tool-master/html_template")
print(template_dir)

start_time=time.strftime("%d %b %Y %H:%M")

def get_requestee_name(flag_list):
    for request in flag_list:
        if 'requestee' in request.keys():
            if request['requestee'] in all_team_members:
                return request['requestee']

now = datetime.datetime.now()
all_team_members = all_members()
g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "Need Info")
# Deleting the rows in google sheets
g.needInfo_clean_rows(2,5,50)  
bugs = get_needinfos_bugs()
items=[]
target=""
for  idx, bug in enumerate(bugs):
    
    requestee_name=get_requestee_name(bug.flags)
    print(requestee_name)
    row = 5 + idx
    column = 2
    g.update_sheet(
        row,
        column,
        (
            f'=HYPERLINK("https://bugzilla.redhat.com/show_bug'
            f'.cgi?id={bug.bug_id}", "{bug.bug_id}")'
        )
    )
    g.update_sheet(row, column+1, bug.summary)
    g.update_sheet(row, column+2, bug.status)
    g.update_sheet(row, column+3, bug.component)
    g.update_sheet(row, column+4, bug.severity)
    g.update_sheet(row, column+5, requestee_name)
    g.update_sheet(row, column+6, bug.version)

    target_list=[*bug.target_release]
    target=target.join(target_list)
    g.update_sheet(row, column+7, *bug.target_release)
    converted = datetime.datetime.strptime(
        bug.last_change_time.value, "%Y%m%dT%H:%M:%S")
    age=(now - converted).days
    g.update_sheet(row, column+8, (now - converted).days)
    time.sleep(10)
    an_item = dict(bug_id=bug.bug_id,summary=bug.summary, status=bug.status,
                   component=bug.component,severity=bug.severity,
                   requestee_name=requestee_name,version=bug.version,
                   target_release=target,age=age
                   )
    items.append(an_item)
 




jinja_env = Environment(extensions=[MarkdownExtension],
    loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
template = jinja_env.get_template("need_info.html")
html = template.render(items=items)

sender = "skanta@redhat.com"
recipients = ["skanta@redhat.com","vereddy-all@redhat.com"]

msg = MIMEMultipart("alternative")
msg["Subject"] = "Bugzilla action items on QE -Auto generated at "\
                    + start_time
msg["From"] = sender
msg["To"] = ", ".join(recipients)
part1 = MIMEText(html, "html")
msg.attach(part1)
        

try:
            s = smtplib.SMTP("localhost")
            s.sendmail(sender, recipients, msg.as_string())
            s.quit()
            print(
                "Results have been emailed to {recipients}".format(
                    recipients=recipients
                )
            )

except Exception as e:
            print("\n")
            #log.exception(e)
