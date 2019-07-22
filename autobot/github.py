# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Github Client."""

from autobot.config import Config
from github3 import login, repository
from datetime import datetime
import pytz


class GitHubAPI:

    def __init__(self, config: Config):
        self.owner = config.owner
        self.GH_CLIENT = login(token=config.GITHUB_TOKEN)


    def fetch_comment_info(self, comment):
        return {
            'url': comment.html_url,
            'creation_date': comment.created_at,
            'user': {
                'name': comment.user.login,
                'url': comment.user.url,
            },
        }


    def fetch_pr_info(self, pr):
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


    def fetch_issue_info(self, issue):
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


    def fetch_repo_info(self, repo):
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


    def check_mentions(self, m, maintainers):
        res = []
        mentions = list(
            filter(
                lambda login: m.body and (
                    login in [mention[1:] for mention in m.body]),
                maintainers
            )
        )
        if mentions:
            res.append({'You\'ve been mentioned here!': mentions})
        return res


    def check_mergeable(self, pr, maintainers):
        res = []
        if pr.refresh().mergeable:
            res.append({'Merge this!': maintainers})
        return res


    def check_review(self, pr, maintainers):
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


    def check_if_connected_with_issue(self, pr, maintainers):
        res = []
        if pr.issue() is None:
            res.append({'Resolve not connected with issue!': maintainers})
        return res


    def check_close(self, pr, maintainers):
        res = []
        if ((datetime.utcnow().replace(tzinfo=pytz.utc)-pr.updated_at).days >=
                3*30):
            res.append({'Close this!': maintainers})
        return res


    def check_follow_up(self, pr, maintainers):
        res = []
        if (('WIP' in pr.title) and
            ((datetime.utcnow().replace(tzinfo=pytz.utc)-pr.updated_at).days >=
            1*30)):
            res.append({'Follow up on this!': maintainers})
        return res


    def check_labels(self, issue, maintainers):
        res = []
        if list(filter(lambda label: label.name == 'RFC', issue.labels())):
            res.append({'Skip this for now!': maintainers})
        return res


    def check_comments(self, issue, maintainers):
        res = []
        comments = [comment for comment in issue.comments()]
        if (comments and comments[-1].user.login not in maintainers):
            res.append({'Follow up on this!': maintainers})
        return res


    comment_filters = [
        check_mentions,
    ]

    pr_filters = [
            check_mergeable,
            check_review,
            check_if_connected_with_issue,
            check_mentions,
            check_close,
            check_follow_up,
    ]

    issue_filters = [
        check_labels,
        check_comments,
        check_mentions,
    ]


    def _comment_report(self, comment, maintainers):
        """Check a comment for possible actions."""

        res = []
        for f in self.comment_filters:
            res += f(self, comment, maintainers)
        return res


    def _pr_report(self, pr, maintainers):
        """Check a pull request for possible actions."""

        res = []
        for f in self.pr_filters:
            res += f(self, pr, maintainers)
        actions = {
            'issue_comments': [
                {
                    **{'actions': self._comment_report(comment, maintainers)},
                    **self.fetch_comment_info(comment)
                }
                for comment in pr.issue_comments()
            ]
        }
        res.append(actions) if actions['issue_comments'] else None
        actions = {
            'review_comments': [
                {
                    **{'actions': self._comment_report(comment, maintainers)},
                    **self.fetch_comment_info(comment)
                }
                for comment in pr.review_comments()
            ]
        }
        res.append(actions) if actions['review_comments'] else None
        return res


    def _issue_report(self, issue, maintainers):
        """Check an issue for possible actions."""

        res = []
        for f in self.issue_filters:
            res += f(self, issue, maintainers)
        actions = {
            'comments': [
                {
                    **{'actions': self._comment_report(comment, maintainers)},
                    **self.fetch_comment_info(comment)
                }
                for comment in issue.comments()
            ]
        }
        res.append(actions) if actions['comments'] else None
        return res


    def _repo_report(self, repo, maintainers):
        """Check a repository for possible actions."""

        res = []
        actions = {
            'prs': [
                {
                    **{'actions': self._pr_report(pr, maintainers)},
                    **self.fetch_pr_info(pr)
                }
                for pr in repo.pull_requests() if (pr.state == 'open')
            ]
        }
        res.append(actions) if actions['prs'] else None
        actions = {
            'issues': [
                {
                    **{'actions': self._issue_report(issue, maintainers)},
                    **self.fetch_issue_info(issue)
                }
                for issue in repo.issues() if (issue.state == 'open')
            ]
        }
        res.append(actions) if actions['issues'] else None
        return res


    def _report(self, repos, maintainers):
        """Check a repository for possible actions."""

        res = []
        actions = {'repos': []}
        for repo in repos:
            repo_obj = self.GH_CLIENT.repository(self.owner, repo)
            actions['repos'].append(
                {
                    **{'actions': self._repo_report(repo_obj, maintainers)},
                    **self.fetch_repo_info(repo_obj)
                }
            )
        res.append(actions) if actions['repos'] else None
        return res
