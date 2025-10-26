from constants.constants import ROLE_AVATARS


def get_role_emoji(role_with_desc: str) -> str:
    base = role_with_desc.split(" - ")[0] if role_with_desc else ""
    return ROLE_AVATARS.get(base, ":robot:")
