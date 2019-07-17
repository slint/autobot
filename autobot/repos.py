from .issues import check_issue, fetch_issue_info
from .prs import check_pr, fetch_pr_info


def fetch_repo_info(repo):
    return {
        'url': repo.clone_url,
        'creation_date': repo.created_at,
        'description': repo.description,
        # 'collaborators': [
        #     {
        #         'name': collaborator.login,
        #         'url': collaborator.url
        #     } for collaborator in repo.collaborators()
        # ],
    }


def check_repo(repo, maintainers):
    res = []
    actions = {
        'prs': [
            {
                **{'actions': check_pr(pr, maintainers)},
                **fetch_pr_info(pr)
            }
            for pr in repo.pull_requests() if (pr.state == 'open')
        ]
    }
    res.append(actions) if actions['prs'] else None
    actions = {
        'issues': [
            {
                **{'actions': check_issue(issue, maintainers)},
                **fetch_issue_info(issue)
            }
            for issue in repo.issues() if (issue.state == 'open')
        ]
    }
    res.append(actions) if actions['issues'] else None
    return res
