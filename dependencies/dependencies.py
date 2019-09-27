from secrets import GITHUB_API_KEY

from collections import Counter
import requests

headers = {
    'Accept': 'application/vnd.github.hawkgirl-preview+json',
    'Authorization': f'bearer {GITHUB_API_KEY}',
}

# https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
def run_query(query, variables): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

# The GraphQL query (with a few aditional bits included) itself defined as a
# multi-line string.
query = '''
    query ($login: String!) {
        user (login: $login) {
            repositories (
                first: 100
                orderBy: {
                    direction: DESC
                    field: STARGAZERS
                }
            ) {
                edges {
                    node {
                        primaryLanguage {
                            name
                        }
                        dependencyGraphManifests {
                            edges {
                                node {
                                    dependencies {
                                        edges {
                                            node {
                                                packageName
                                                requirements
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
'''

# https://blogs.oracle.com/java/top-java-libraries-on-github
def load_top_java_libraries():
    with open('top_java_libraries.txt', 'r') as f:
        return f.read().splitlines()

def get_top_dependencies(user):
    variables = {
        'login': user,
    }
    result = run_query(query, variables)
    dependencies = list()
    repos = result['data']['user']['repositories']
    for repoEdge in repos['edges']:
        lang = repoEdge['node']['primaryLanguage']
        if lang and lang['name'] == 'Java':
            for dependencyGraphEdge in repoEdge['node']['dependencyGraphManifests']['edges']:
                for dependencyEdge in dependencyGraphEdge['node']['dependencies']['edges']:
                    dependencies.append(dependencyEdge['node']['packageName'])
                    # use this for matching with the top libraries
                    # dependencies.append(dependencyEdge['node']['packageName'].split(':')[0])

    counter = Counter(dependencies)

    '''
    # use this for matching with the top libraries
    top_counter = Counter({lib: counter[lib] for lib in load_top_java_libraries()})
    top_counter = +top_counter # remove 0's
    return top_counter.most_common(10)
    '''

    return counter.most_common(10)
