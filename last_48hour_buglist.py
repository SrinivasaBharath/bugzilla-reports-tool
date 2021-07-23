# -*- coding: utf-8 -*-

from jinja2 import Environment, FileSystemLoader,select_autoescape
from jinja_markdown import MarkdownExtension
import os
import time
from helpers import *
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from cephQeInfra import commonFunctions





items=[]
target=""

start_time=time.strftime("%d %b %Y %H:%M")

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(project_dir)
template_dir=os.path.join(project_dir, "bugzilla-reports-tool-master/html_template")

g = gapi.GoogleSpreadSheetAPI(SPREADSHEET_NAME, "New_Bugs")
bugs=get_ceph_new_arrivals(5,"-48h")
print("The number of bugs are ::::",len(bugs))
for  idx, bug in enumerate(bugs):
    print("The bug id is ::::::",bug.bug_id)
    
    target_list=[*bug.target_release]
    target=target.join(target_list)
    blocker_status=commonFunctions.get_blocker_status(bug.flags)
    an_item = dict(bug_id=bug.bug_id,summary=bug.summary, status=bug.status,
                   component=bug.component,severity=bug.severity,
                   is_Blocker=blocker_status,
                   version=bug.version,target_release=target
                   )
    items.append(an_item)

jinja_env = Environment(extensions=[MarkdownExtension],
    loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )
template = jinja_env.get_template("last_48hrs_bugs.html")
html = template.render(items=items)


sender = "skanta@redhat.com"
recipients = ["skanta@redhat.com"]

msg = MIMEMultipart("alternative")
msg["Subject"] = "Last 48 hrs Reported bugs -Auto generated at "\
                    + start_time +"[IST]"
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
print("done")