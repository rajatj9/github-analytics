import numpy as np
from tqdm import tqdm


def is_bot(event):
    if hasattr(event, 'actor'):
        return 'bot' in event.actor.login
    else:
        return 'bot' in event.user.login


def get_pr_statistics(issue, username):
    issue_close_date = issue.closed_at
    issue_time_open = (issue_close_date - issue.created_at).days

    comments = list(issue.get_comments())
    events = list(issue.get_events())
    all_events = comments + events

    no_bots = filter(lambda x: not is_bot(x), all_events)

    sorted_events = sorted(no_bots, key=lambda x: x.created_at, reverse=False)

    text = [e.event if hasattr(e, 'event') else e.body for e in sorted_events]
    dates = [e.created_at if hasattr(e, 'event') else e.created_at for e in sorted_events]

    response_times = []
    last_date_idx = len(dates) - 1
    previous_date = None
    for i, date in enumerate(dates):
        if i == 0:
            previous_date = date
            continue
        if i == last_date_idx:
            break

        response_times.append((date - previous_date).days)

    num_fixes = sum(
        [1 if hasattr(event, 'event') and 'push' in text and event.actor == username else 0 for event, text in zip(sorted_events, text)])
    conflicts = sum([1 if hasattr(event, 'event') and 'conflict' in text and event.actor == username else 0 for event, text in
                     zip(sorted_events, text)])
    merges = sum(
        [1 if hasattr(event, 'event') and 'merge' in text and event.actor == username else 0 for event, text in zip(sorted_events, text)])

    return response_times, issue_time_open, num_fixes, conflicts, merges


def get_pr_score(g, username):
    prs = g.search_issues('language:Java closed:>2019-01-01', state='closed', author=username, type='pr', sort='comments')
    scores = []
    all_response_times = []
    all_additions = 0
    all_deletions = 0
    for pr in tqdm(prs, total=prs.totalCount):
        pr = pr.as_pull_request()
        additions = pr.additions
        deletions = pr.deletions

        all_additions += additions
        all_deletions += deletions

        response_times, issue_time_open, num_fixes, conflicts, merges = get_pr_statistics(pr.as_issue(), username)

        all_response_times += response_times
        if len(response_times) > 0:
            response_times = np.array(response_times, dtype='float')
            avg_response_time = response_times.mean()
        else:
            avg_response_time = 0.2 * issue_time_open

        if issue_time_open == 0:
            issue_time_open = 1
            avg_response_time = 0

        if (deletions + additions) == 0:
            score = 0
        else:
            score = ((0.6 * deletions + 0.4 * additions) / (deletions + additions)) * (
                    issue_time_open - avg_response_time) / issue_time_open
            if conflicts > 0 or merges > 0:
                score *= 0.9 * score

        scores.append(score)

    if len(all_response_times) > 0:
        mean_response_time = np.mean(all_response_times)
    else:
        mean_response_time = 0

    try:
        score = np.mean(scores)
    except Exception:  # TODO narrow down - ZeroDivisionError, ValueError
        score = 0

    return score, mean_response_time, all_additions, all_deletions
