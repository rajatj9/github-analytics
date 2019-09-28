from dependencies.dependencies import get_top_dependencies, score_versatility
from secrets import GITHUB_API_KEY

from flask import Flask, render_template, request
from functools import lru_cache
from github import Github
from math import sqrt
from results import get_results, score_practices, score_activity
import json

app = Flask(__name__)
g = Github(GITHUB_API_KEY)


@app.route('/')
def index():
    user = request.args.get('user')
    return json.dumps(get(user))


@app.route('/compare')
def compare():
    userA = request.args.get('userA')
    userB = request.args.get('userB')
    resultA = get(userA)
    resultB = get(userB)
    similarity = compute_similarity(resultA, resultB)
    return json.dumps({
        'userA': resultA,
        'userB': resultB,
        'similarity': int(100 * similarity)
    })


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
    result['overall_score'] = int(100 * compute_overall_score(scores))
    scores = {k: int(100 * v) for k, v in scores.items()}

    # Return json
    result['scores'] = scores
    return result


weights = {
    'versatility': 1,
    'best_practices': 1,
    'github_activity': 1,
}


def compute_overall_score(scores):
    weighted_scores = [weights[key] * scores[key] for key in weights]
    return sum(weighted_scores) / sum(weights.values())


def compute_similarity(resultA, resultB):
    weightedA = [weights[key] * resultA['scores'][key] for key in weights]
    weightedB = [weights[key] * resultB['scores'][key] for key in weights]
    normA = sqrt(sum([s * s for s in weightedA]))
    normB = sqrt(sum([s * s for s in weightedB]))
    dot = sum([a * b for a, b in zip(weightedA, weightedB)])
    return dot / (normA * normB)


if __name__ == '__main__':
    app.run(port=5000)
