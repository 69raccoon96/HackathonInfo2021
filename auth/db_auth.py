from aiohttp_security import AbstractAuthorizationPolicy


class DBAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, user_repo):
        self.user_repo = user_repo

    async def authorized_userid(self, identity):
        user = await self.user_repo.get_user_by_username(identity)
        if user is not None and user.username == identity:
            return identity
        else:
            return None

    async def permits(self, identity, permission, context=None):
        if identity is None:
            return False
        # checks)
        user = await self.user_repo.get_user_by_username(identity)
        if user is not None and user.username == identity:
            return user.status == 'admin' or user.status == permission
        return False


async def check_credentials(user_repo, username, password):
    user = await user_repo.get_user_by_username(username)
    return user is not None and user.password == password
