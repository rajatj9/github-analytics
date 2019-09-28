import json
import numpy as np
from functools import lru_cache
from math import sqrt, isnan

from flask import Flask, request
from github import Github

from dependencies.dependencies import get_top_dependencies, score_versatility
from results import get_results, score_practices, score_activity
from scorers.CommentsCommunityEngagemnt import get_comments_score
from scorers.PullRequestScore import get_pr_score
from secrets import GITHUB_API_KEY
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

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


@lru_cache(maxsize=100)
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
    scores['code_quality'] = result['code_quality_index']

    comments_score = get_comments_score(g, user)
    pr_score, mean_response_time, all_additions, all_deletions = get_pr_score(g, user)
    community_score = (comments_score + pr_score) / 2

    scores['community_score'] = community_score
    result['overall_score'] = int(100 * compute_overall_score(scores))
    scores = {k: int(100 * v) for k, v in scores.items() if not isnan(v)}

    # Return json
    result['scores'] = scores

    result['community_scores'] = {
        'comments_quality_score': int(comments_score * 100),
        'pr_quality_score': int(pr_score * 100)
    }

    result['avg_response_time'] = round(mean_response_time, 1)
    result['code_additions'] = all_additions
    result['code_deletions'] = all_deletions
    return result


weights = {
    'code_quality': 1,
    'versatility': 1,
    'best_practices': 1,
    'github_activity': 1,
    'community_score': 1,
}


def compute_overall_score(scores):
    weighted_scores = [weights[key] * scores[key] for key in weights]
    return sum(weighted_scores) / sum(weights.values())


def compute_similarity(resultA, resultB):
    weightedA = [weights[key] * resultA['scores'][key] for key in weights]
    weightedB = [weights[key] * resultB['scores'][key] for key in weights]
    normA = np.linalg.norm(weightedA)
    normB = np.linalg.norm(weightedB)
    dot = sum([a * b for a, b in zip(weightedA, weightedB)])
    return dot / (normA * normB)


if __name__ == '__main__':
    app.run(port=5000)