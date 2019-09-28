from dependencies.dependencies import get_top_dependencies, score_versatility
from secrets import GITHUB_API_KEY

from flask import Flask, render_template, request
from github import Github
from results import get_results
import json

app = Flask(__name__)
g = Github(GITHUB_API_KEY)


@app.route('/')
def index():
    scores = dict()

    user = request.args.get('user')
    '''
    Examples of how to get metrics and return data
    metrics.update(codequality_metrics(repos))
    metrics.update(community_metrics(repos))
    metrics.update(metrics3(repos))
    '''
    # Populate results
    result = get_results(user)
    result['top_dependencies'] = get_top_dependencies(user)

    # Compute scores
    scores['versatility'] = score_versatility(result['top_dependencies'])

    # Return json
    result['scores'] = scores
    return json.dumps(result)


if __name__ == '__main__':
    app.run(port=5000)
