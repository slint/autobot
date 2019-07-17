from .comments import fetch_comment_info, check_comment


def fetch_issue_info(issue):
    return {
        'id': issue.number,
        'url': issue.html_url,
        'title': issue.title,
        'creation_date': issue.created_at,
        'description': issue.body,
        'state': issue.state,
        'labels': [
            {
                'name': label.name,
                'color': label.color,
                'url': label.url
            } for label in issue.labels()
        ],
        'user': {
            'name': issue.user.login,
            'url': issue.user.url,
        },
    }


def check_labels(issue, maintainers):
    res = []
    if list(filter(lambda label: label.name == 'RFC', issue.labels())):
        res.append({'Skip this for now!': maintainers})
    return res


def check_comments(issue, maintainers):
    res = []
    comments = [comment for comment in issue.comments()]
    if (comments and comments[-1].user.login not in maintainers):
        res.append({'Follow up on this!': maintainers})
    return res


def check_mentions(issue, maintainers):
    res = []
    mentions = list(
        filter(
            lambda login: issue.body and (
                login in [mention[1:] for mention in issue.body]), maintainers
        )
    )
    if mentions:
        res.append({'You\'ve been mentioned in this issue!': mentions})
    return res


filters = [
    check_labels,
    check_comments,
    check_mentions,
]


def check_issue(issue, maintainers):
    res = []
    for f in filters:
        res += f(issue, maintainers)
    actions = {
        'comments': [
            {
                **{'actions': check_comment(comment, maintainers)},
                **fetch_comment_info(comment)
            }
            for comment in issue.comments()
        ]
    }
    res.append(actions) if actions['comments'] else None
    return res
