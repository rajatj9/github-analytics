from dependencies.dependencies import get_top_dependencies, score_versatility
from secrets import GITHUB_API_KEY

from flask import Flask, render_template, request
from functools import lru_cache
from github import Github
from results import get_results, score_practices, score_activity
import json

app = Flask(__name__)
g = Github(GITHUB_API_KEY)


@app.route('/')
def index():
    user = request.args.get('user')
    return get(user)

@lru_cache(maxsize=10)
def get(user):
    scores = dict()

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
    scores['best_practices'] = score_practices(result)
    scores['github_activity'] = score_activity(result)

    # Return json
    result['scores'] = scores
    return json.dumps(result)


if __name__ == '__main__':
    app.run(port=5000)
