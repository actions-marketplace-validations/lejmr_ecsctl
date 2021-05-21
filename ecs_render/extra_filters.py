import re
from slugify import slugify
import dateparser


def get_jira_id(bn, default):
    # https://community.atlassian.com/t5/Bitbucket-questions/Regex-pattern-to-match-JIRA-issue-key/qaq-p/233319
    m = re.search('(?:[A-Z]{1,10}-?)([A-Z]+-\d+)', bn)
    if m:
        return m.group(0)
    return default

def get_slug(name, max_length=20):
    return slugify(name)[:max_length]

def filter_dateparser(s):
    return dateparser.parse(s)

def filter_format(d, f='%Y-%m-%dT%H:%M:%S.000'):
    # print(d.strftime(f))
    # return "milos"
    
    return str(d.strftime(f))