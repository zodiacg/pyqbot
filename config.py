from internal import const as C

import customreply

host = '127.0.0.1'
port = 9876

bot_commands = {
    # keyword: [callback_func, cooldown in secs, grp/priv, enabled groups, regex, msg, at_sender]
    r'.*有人.+[吗嘛][\?？]?': [customreply.guna, 0, C.GROUP, set(), C.REGEX, C.NO_MSG, C.NO_AT_SENDER]
}

default_proc = [
    # (callbacks, cooldown in secs, grp/priv, enabled groups)
    (customreply.nature_of_human, 0, C.GROUP, set())
]

scheduled_tasks = [
    # (callback_func, h, m, s)
]
