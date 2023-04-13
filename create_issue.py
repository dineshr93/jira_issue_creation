from atlassian import Jira
import json
import requests
import sys
import os
# https://atlassian-python-api.readthedocs.io/jira.html#manage-issues
# pip install atlassian-python-api

user = os.environ.get("JUSER")
pwd = os.environ.get("JPWD")

if len(user) is 0 and len(pwd) is 0:
    sys.exit('export environment variable JUSER= & JPWD=')
if len(user) is 0 or len(pwd) is 0:
    sys.exit('export either of environment variable JUSER & JPWD')

jira = Jira(
    url='https://jira.elektrobit.com/',
    username=user,
    password=pwd)
	

# Create issue
def create_issue(snapshot: str, variantBrand: str):
    component = component_for(variantBrand)
    template_ticket = template_ticket_for(variantBrand)

    fields = {'summary': f'AED Gen2 {variantBrand} {snapshot}_{variantBrand} release scan',
            'project': {"key": "your_pj_key"},
            "assignee": {"name": "jira_user_name"},
            "description": f"*Description:*\r\n # Perform an open source scan for {variantBrand} release *{snapshot}_{variantBrand}* \r\n\r\n*Link to scan:*\r\n # {variantBrand}: \r\n\r\n*Security Risk Findings:*\r\n\r\n\u00a0\r\n",
            "components": [{"name": "your_component1"},{"name": component}],
            "issuetype": {"name": "Task"}
            }
    try:
        data=jira.issue_create(fields)
        # print(json.dumps(data, indent = 4))
        new_issue_id=data.get('key')
        new_issue_link=f'https://jira.company.com/browse/{new_issue_id}'
        issue_links.append(new_issue_link)
        # Create Issue Link
        data_link = {"type": {"name": "Cloners" },"inwardIssue": { "key": f'{new_issue_id}'},"outwardIssue": {"key": f"{template_ticket}"}}
        data=jira.create_issue_link(data_link)
        # print(json.dumps(data, indent = 4))
        print()
        print(f'Add epic "{epic_text_for(vab)}" to link {new_issue_link}')
        print('-'*50)
        
    except requests.exceptions.HTTPError as e:
        print(e.response.json())
