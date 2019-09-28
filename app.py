import json

from flask import Flask, request
from github import Github

from dependencies.dependencies import get_top_dependencies, score_versatility
from results import get_results, score_practices, score_activity
from scorers.CommentsCommunityEngagemnt import get_comments_score
from scorers.PullRequestScore import get_pr_score
from secrets import GITHUB_API_KEY

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
    scores['best_practices'] = score_practices(result)
    scores['github_activity'] = score_activity(result)

    comments_score = get_comments_score(g, user)
    pr_score, mean_response_time, all_additions, all_deletions = get_pr_score(g, user)

    community_score = (comments_score + pr_score) / 2

    scores['community_score'] = community_score

    # Return json
    result['scores'] = scores

    result['community_scores'] = {
        'comments_quality_score': comments_score,
        'pr_quality_score': pr_score
    }

    result['avg_response_time'] = mean_response_time
    result['code_additions'] = all_additions
    result['code_deletions'] = all_deletions
    return json.dumps(result)


if __name__ == '__main__':
    app.run(port=5000)
