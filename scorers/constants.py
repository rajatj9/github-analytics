import re
from github import Github

g = Github("<token>")

class_pattern = re.compile(r'\s*(public|private)\s+class\s+(\w+)\s+((extends\s+\w+)|(implements\s+\w+( ,\w+)*))?\s*\{')
method_pattern = re.compile(r'(public|protected|private|static|\s) +[\w\<\>\[\],\s]+\s+(\w+) *\([^\)]*\) *(\{?|[^;])')