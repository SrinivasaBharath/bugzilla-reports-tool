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
from datetime import datetime, date, timedelta
import pytz

import sys

target=""

UTC = pytz.utc
IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)
start_time=datetime_ist.strftime("%d %b %Y %H:%M")

changed_to =  str(date.today())
changed_from = str(date.today() - timedelta(7))
period = changed_from+" To "+changed_to

sender = "ceph-qe-infra@redhat.com"
recipients = ["ceph-qe@redhat.com","vdas@redhat.com"]

msg = MIMEMultipart("mixed")
msg["Subject"] = "Customer Experience Report : "+period
msg["From"] = sender
msg["To"] = ", ".join(recipients)

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
template_dir=os.path.join(project_dir, "bugzilla-reports-tool/html_template")

bugs=get_customer_bug_reported(changed_from, changed_to)

items_count={"Bugs Reported":[len(bugs[0]),bugs[1]],"Customer Escalation":[len(get_customer_ex_escalation(changed_from, changed_to)[0]),get_customer_ex_escalation(changed_from, changed_to)[1]],"Hotfix Request":[len(get_hotfix_count(changed_from, changed_to)[0]),get_hotfix_count(changed_from, changed_to)[1]],
            "RFE Bugs":[len(get_customer_ex_rfe_bug(changed_from, changed_to)[0]),get_customer_ex_rfe_bug(changed_from, changed_to)[1]],"Needinfo Requested":[len(get_customer_ex_needinfo_req(changed_from, changed_to)[0]),get_customer_ex_needinfo_req(changed_from, changed_to)[1]],
            "QE_Test_Coverage +":[len(get_customer_ex_qe_test_flag_plus(changed_from, changed_to)[0]),get_customer_ex_qe_test_flag_plus(changed_from, changed_to)[1]],"QE_Test_Coverage -":[len(get_customer_ex_qe_test_flag_minus(changed_from, changed_to)[0]),get_customer_ex_qe_test_flag_minus(changed_from, changed_to)[1]],
            "Customer Opened Document Bugs":[len(get_customer_ex_document_bugs_count(changed_from, changed_to)[0]),get_customer_ex_document_bugs_count(changed_from, changed_to)[1]],"Missing Polarion TC Id":[len(missing_polarion()[0]),missing_polarion()[1]],"General Trend/Pattern":""}
jinja_env = Environment(extensions=[MarkdownExtension],
    loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
    )

template = jinja_env.get_template("customer_exp_report.html")
html1 = template.render(items_count=items_count)
table1 = MIMEText(html1, "html")
msg.attach(table1)

if items_count["Bugs Reported"][0]>0:
    items=[]
    for  idx, bug in enumerate(bugs[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items.append(an_item)
    # jinja_env = Environment(extensions=[MarkdownExtension],
    #     loader=FileSystemLoader(template_dir),
    #         autoescape=select_autoescape(["html", "xml"]),
    #     )
    # template = jinja_env.get_template("customer_ex_bug_reported.html")
    # html2 = template.render(items=items)
    # table2 = MIMEText(html2, "html")
    # msg.attach(table2)

if items_count["Customer Escalation"][0]>0:
    bugs_esc=get_customer_ex_escalation(changed_from, changed_to)
    items1=[]
    for  idx, bug in enumerate(bugs_esc[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item1 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items1.append(an_item1)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_esc.html")
    html3 = template.render(items1=items1)
    table3 = MIMEText(html3, "html")
    msg.attach(table3)

if items_count["Hotfix Request"][0]>0:
    bugs_hotfix=get_hotfix_count(changed_from, changed_to)
    items2=[]
    for  idx, bug in enumerate(bugs_hotfix[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item2 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items2.append(an_item1)
    # jinja_env = Environment(extensions=[MarkdownExtension],
    #     loader=FileSystemLoader(template_dir),
    #         autoescape=select_autoescape(["html", "xml"]),
    #     )
    # template = jinja_env.get_template("customer_ex_cus_hotfix.html")
    # html4 = template.render(items2=items2)
    # table4 = MIMEText(html4, "html")
    # msg.attach(table4)

if items_count["RFE Bugs"][0]>0:
    bugs_rfe = get_customer_ex_rfe_bug(changed_from, changed_to)
    items3=[]
    for  idx, bug in enumerate(bugs_rfe[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        an_item3 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items3.append(an_item3)
    # jinja_env = Environment(extensions=[MarkdownExtension],
    #     loader=FileSystemLoader(template_dir),
    #         autoescape=select_autoescape(["html", "xml"]),
    #     )
    # template = jinja_env.get_template("customer_ex_cus_rfe.html")
    # html5 = template.render(items3=items3)
    # table5 = MIMEText(html5, "html")
    # msg.attach(table5)

if items_count["Needinfo Requested"][0]>0:
    bugs_needinfo = get_customer_ex_needinfo_req(changed_from, changed_to)
    items4=[]
    for  idx, bug in enumerate(bugs_needinfo[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item4 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items4.append(an_item4)
    # jinja_env = Environment(extensions=[MarkdownExtension],
    #     loader=FileSystemLoader(template_dir),
    #         autoescape=select_autoescape(["html", "xml"]),
    #     )
    # template = jinja_env.get_template("customer_ex_cus_needinfo.html")
    # html6 = template.render(items4=items4)
    # table6 = MIMEText(html6, "html")
    # msg.attach(table6)

if items_count["QE_Test_Coverage +"][0]>0:
    bugs_qe_plus = get_customer_ex_qe_test_flag_plus(changed_from, changed_to)
    items5=[]
    for  idx, bug in enumerate(bugs_qe_plus[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item5 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items5.append(an_item5)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_qe_plus.html")
    html7 = template.render(items5=items5)
    table7 = MIMEText(html7, "html")
    msg.attach(table7)

if items_count["QE_Test_Coverage -"][0]>0:
    bugs_qe_minus = get_customer_ex_qe_test_flag_minus(changed_from, changed_to)
    items6=[]
    for  idx, bug in enumerate(bugs_qe_minus[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item6 = dict(qa_contact=bug.qa_contact,bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items6.append(an_item6)
    jinja_env = Environment(extensions=[MarkdownExtension],
        loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(["html", "xml"]),
        )
    template = jinja_env.get_template("customer_ex_cus_qe_minus.html")
    html8 = template.render(items6=items6)
    table8 = MIMEText(html8, "html")
    msg.attach(table8)

if items_count["Customer Opened Document Bugs"][0]>0:
    bugs_doc = get_customer_ex_document_bugs_count(changed_from, changed_to)
    items7=[]
    for  idx, bug in enumerate(bugs_doc[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item7 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items7.append(an_item7)
    # jinja_env = Environment(extensions=[MarkdownExtension],
    #     loader=FileSystemLoader(template_dir),
    #         autoescape=select_autoescape(["html", "xml"]),
    #     )
    # template = jinja_env.get_template("customer_ex_cus_doc.html")
    # html9 = template.render(items7=items7)
    # table9 = MIMEText(html9, "html")
    # msg.attach(table9)


if items_count["Missing Polarion TC Id"][0]>0:
    miss_polarion = missing_polarion()
    items8=[]
    for  idx, bug in enumerate(miss_polarion[0]):
        target_list=[*bug.target_release]
        target=target.join(target_list)
        blocker_status=commonFunctions.get_blocker_status(bug.flags)
        hotfix_request=commonFunctions.get_hotfix_status(bug.flags)
        an_item8 = dict(bug_id=bug.bug_id,summary=bug.summary,reporter=bug.creator, status=bug.status,
                    component=bug.component,severity=bug.severity,
                    is_Blocker=blocker_status,
                    version=bug.version,target_release=target,)
        items8.append(an_item8)
    # jinja_env = Environment(extensions=[MarkdownExtension],
    #     loader=FileSystemLoader(template_dir),
    #         autoescape=select_autoescape(["html", "xml"]),
    #     )
    # template = jinja_env.get_template("customer_ex_missing_polarion.html")
    # html10 = template.render(items8=items8)
    # table10 = MIMEText(html10, "html")
    # msg.attach(table10)

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
            log.exception(e)
            print(e)
print("done")
