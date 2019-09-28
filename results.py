from github import Github

credentials = open("credentials.json").read().split(',')

def get_results(username: str):
    g = Github(credentials[0], credentials[1])
    user = g.get_user(username)
    repos = user.get_repos()
    result = {}
    star_count = 0
    open_issues = 0
    repo_count = 0
    fork_count = 0
    has_readme = False
    has_maven_gradle = False
    uses_branches = False
    for repo in repos:
        if "Java" == repo._language.value:
            star_count += repo.stargazers_count
            open_issues += len(list(repo.get_issues(state='open')))
            repo_count += 1
            fork_count += repo._forks_count.value
            if len(list(repo.get_branches())) > 1:
                uses_branches = True
            for file in repo.get_dir_contents(""):
                if file.name == "gradle" or file.name == "pom.xml":
                    has_maven_gradle = True
                if file.name.lower() == "readme.md":
                    has_readme = True

    result = { 'name': user._name.value, 'username': username, 'avatar': user._avatar_url.value, 'bio': user._bio.value, 'email': user._email.value,
              'location': user._location.value, 'company': user._company.value, 'num_of_java_repos': repo_count,
              'avg_stars_count_per_repo': star_count / repo_count, 'avg_open_issues_per_repo': open_issues / repo_count,
              'avg_fork_count': fork_count / repo_count,
              'has_maven_gradle': has_maven_gradle, 'has_readme': has_readme, 'uses_branches': uses_branches}

    return result
