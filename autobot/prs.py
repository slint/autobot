from .comments import fetch_comment_info, check_comment
from datetime import datetime
import pytz


def fetch_pr_info(pr):
    return {
        'id': pr.number,
        'url': pr.html_url,
        'title': pr.title,
        'creation_date': pr.created_at,
        'description': pr.body,
        'state': pr.state,
        # 'labels': [
        #    {
        #          'name': label.name,
        #          'color': label.color,
        #          'url': label.url
        #    } for label in pr.labels()
        #    ],
        'user': {
            'name': pr.user.login,
            'url': pr.user.url,
        },
        'related_issue': pr.issue_url,
    }


def check_mergeable(pr, maintainers):
    res = []
    if pr.refresh().mergeable:
        res.append({'Merge this!': maintainers})
    return res


def check_review(pr, maintainers):
    res = []
    requested_reviewers = list(
        filter(
            lambda login: login in [
                reviewer.login for reviewer in pr.requested_reviewers],
            maintainers
        )
    )
    if requested_reviewers:
        res.append({'Review this!': requested_reviewers})
    return res


def check_if_connected_with_issue(pr, maintainers):
    res = []
    if pr.issue() is None:
        res.append({'Resolve not connected with issue!': maintainers})
    return res


def check_mentions(pr, maintainers):
    res = []
    mentions = list(
        filter(
            lambda login: pr.body and (
                login in [mention[1:] for mention in pr.body]), maintainers
        )
    )
    if mentions:
        res.append(
            {'You\'ve been mentioned in this pull request!': mentions})
    return res


def check_close(pr, maintainers):
    res = []
    if ((datetime.utcnow().replace(tzinfo=pytz.utc)-pr.updated_at).days >=
            3*30):
        res.append({'Close this!': maintainers})
    return res


def check_follow_up(pr, maintainers):
    res = []
    if (('WIP' in pr.title) and
        ((datetime.utcnow().replace(tzinfo=pytz.utc)-pr.updated_at).days >=
         1*30)):
        res.append({'Follow up on this!': maintainers})
    return res


filters = [
    check_mergeable,
    check_review,
    check_if_connected_with_issue,
    check_mentions,
    check_close,
    check_follow_up,
]


def check_pr(pr, maintainers):
    res = []
    for f in filters:
        res += f(pr, maintainers)
    actions = {
        'issue_comments': [
            {
                **{'actions': check_comment(comment, maintainers)},
                **fetch_comment_info(comment)
            }
            for comment in pr.issue_comments()
        ]
    }
    res.append(actions) if actions['issue_comments'] else None
    actions = {
        'review_comments': [
            {
                **{'actions': check_comment(comment, maintainers)},
                **fetch_comment_info(comment)
            }
            for comment in pr.review_comments()
        ]
    }
    res.append(actions) if actions['review_comments'] else None
    return res
