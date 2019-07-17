def fetch_comment_info(comment):
    return {
        'url': comment.html_url,
        'creation_date': comment.created_at,
        'user': {
            'name': comment.user.login,
            'url': comment.user.url,
        },
    }


def check_mentions(comment, maintainers):
    res = []
    mentions = list(
        filter(
            lambda login: comment.body and (
                login in [mention[1:] for mention in comment.body]),
            maintainers
        )
    )
    if mentions:
        res.append({'You\'ve been mentioned in this comment!': mentions})
    return res


filters = [
    check_mentions,
]


def check_comment(comment, maintainers):
    res = []
    for f in filters:
        res += f(comment, maintainers)
    return res
