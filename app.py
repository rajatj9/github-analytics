from dependencies.dependencies import get_top_dependencies
from secrets import GITHUB_API_KEY

from flask import Flask, render_template, request
from github import Github
import json

app = Flask(__name__)
g = Github(GITHUB_API_KEY)


@app.route('/')
def index():
    metrics = dict()

    user = request.args.get('user')
    repos = g.get_user(user).get_repos()

    '''
    Examples of how to get metrics and return data
    metrics.update(codequality_metrics(repos))
    metrics.update(community_metrics(repos))
    metrics.update(metrics3(repos))
    '''

    metrics['top_dependencies'] = get_top_dependencies(user)
    return json.dumps(metrics)


if __name__ == '__main__':
    app.run(port=5000)
