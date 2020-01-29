import bigbenclock
import customreply
from internal import const as C

host = '127.0.0.1'
port = 9876

scheduler_opt = {
    'apscheduler.timezone': 'Asia/Shanghai'
}

bot_commands = {
    # keyword: [callback_func, cooldown in secs, grp/priv, enabled groups, regex, msg, at_sender]
    r'.*有人.+[吗嘛][\?？]?': [customreply.guna, 0, C.GROUP, set(), C.REGEX, C.NO_MSG, C.NO_AT_SENDER],
    r'^(\d+)刚[刚才]说了(啥|什么)[?？]?$': [customreply.stalker, 0, C.GROUP, set(), C.REGEX, C.NO_MSG, C.AT_SENDER]
}

default_proc = [
    # (callbacks, cooldown in secs, grp/priv, enabled groups)
    (customreply.nature_of_human, 0, C.GROUP, set())
]

scheduled_tasks = [
    # (callback_func, {cron typed time dict})
    (bigbenclock.bigben, {'hour': '*'})
]
