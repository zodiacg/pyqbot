from collections import namedtuple, deque

__all__ = [
    'CB_FUNC', 'CD_TIME', 'F_AT', 'F_MSG', 'F_PRIV_GRP', 'F_REGEX', 'GRP_LIST',
    'Holder'
]

CB_FUNC=0
CD_TIME=1
F_PRIV_GRP=2
GRP_LIST=3
F_REGEX=4
F_MSG=5
F_AT=6


class Holder(object):
    def __init__(self):
        self.cmd_stats = {}
        self.default_stats = {}
        self.chat_history = {}

    def append_msg(self, group_id, sender_id, msg):
        if group_id not in self.chat_history:
            self.chat_history[group_id] = deque([], maxlen=200)
        # left is new
        self.chat_history[group_id].appendleft((sender_id, msg))

    def find_msg(self, group_id, sender_id, maxlen=3):
        msg = []
        if group_id not in self.chat_history:
            return
        if sender_id == 0:
            if maxlen > len(self.chat_history[group_id]):
                return list(self.chat_history[group_id])
            else:
                return list(self.chat_history[group_id])[:maxlen]
        for entry in self.chat_history[group_id]:
            if entry[0] == sender_id:
                msg.append(entry)
            if len(msg) > maxlen:
                break
        return msg


# Not __all__
constants = namedtuple('Constants', ['MSG', 'NO_MSG', 'REGEX', 'NOT_REGEX', 'AT_SENDER', 'NO_AT_SENDER',
                                     'PRIVATE', 'GROUP', 'PRIV_GRP'])
const = constants(True, False, True, False, True, False, {'private'}, {'group'}, {'private', 'group'})
