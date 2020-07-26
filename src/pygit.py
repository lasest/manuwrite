#!/usr/bin/python3
from github import Github
import os
from pprint import pprint


def get_repos(token, user_name):
	token = os.getenv('GITHUB_TOKEN', token)
	g = Github(token)
	user = g.get_user(user_name)
	return user.get_repos()

def print_repo_info(repo):
    # repository full name
    print("Full name:", repo.full_name)
    # repository description
    print("Description:", repo.description)
    # the date of when the repo was created
    print("Date created:", repo.created_at)
    # the date of the last git push
    print("Date of last push:", repo.pushed_at)
    # home website (if available)
    print("Home Page:", repo.homepage)
    # programming language
    print("Language:", repo.language)
    # number of forks
    print("Number of forks:", repo.forks)
    # number of stars
    print("Number of stars:", repo.stargazers_count)
    print("-"*50)
    # repository content (files & directories)
    print("Contents:")
    #it also can be used like follow
    #repo.get_contents(some_file_name, ref="some_branch_name")
    for content in repo.get_contents(""):
        print(content)
    try:
        # repo license
        print("License:", base64.b64decode(repo.get_license().content.encode()).decode())
    except:
        pass


def get_issues(repo, state, page_num):
	issues = repo.get_issues(state = state)
	return issues.get_page(page_num)
	
def create_issue(repo, title, body, assignee, label):
	return repo.create_issue(
	title = title,
	body = body,
	assignee = assignee,
	labels=[repo.get_label(label)])
