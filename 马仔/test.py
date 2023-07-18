import github3


def github_connect():
    with open('path') as f:
        token = f.read()
    print(type(token))
    user = 'MrSolomans'
    sess = github3.login(token=token)
    return sess.repository(user, 'LuaLu')


repo = github_connect()


def get_file_contents(dirname, module_name, repo):
    return repo.file_contents(f'{dirname}/{module_name}').content


print(get_file_contents('config', 'abc.json', repo))
