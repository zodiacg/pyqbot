import time
import re
from aiocqhttp import CQHttp

from internal import *
from internal import const as C
import config as cfg

G = Holder()

bot = CQHttp(access_token='abracadabra',
             enable_http_post=False)


@bot.on_message
async def handle_msg(ctx):
    # prepare reply
    resp_json = {}

    # drop self
    if ctx['sender']['user_id'] == ctx['self_id']:
        return

    # log msg
    if ctx['message_type'] == 'group' and ctx['sub_type'] == 'normal':
        G.append_msg(ctx['group_id'], ctx['sender']['user_id'], ctx['message'])

    # check commands
    matched_cmd = None
    for cmd, func in cfg.bot_commands.items():
        # check cooldown
        if func[CD_TIME] !=0 and cmd in G.cmd_stats and time.time() - G.cmd_stats[cmd] < func[CD_TIME]:
            continue
        # filter private and group
        if ctx['message_type'] not in func[F_PRIV_GRP]:
            continue
        # check if enabled for the group
        if ctx['message_type'] == 'group' and func[GRP_LIST] and ctx['group_id'] not in func[GRP_LIST]:
            continue
        # choose proper matching method
        # regex
        if func[F_REGEX]:
            match = re.match(cmd, ctx['message'])
            if match:
                matched_cmd = cmd
                break
        # full match
        elif func[F_MSG] == C.NO_MSG:
            if ctx['message'] == cmd:
                matched_cmd = cmd
                break
        # start match
        elif ctx['message'].startswith(cmd):
            matched_cmd = cmd
            break

    if not matched_cmd:
        # default routine
        for idx, func in enumerate(cfg.default_proc):
            # check cooldown
            if func[CD_TIME] != 0 and idx in G.default_stats and time.time() - G.default_stats[idx] < func[CD_TIME]:
                continue
            # filter private and group
            if ctx['message_type'] not in func[F_PRIV_GRP]:
                continue
            # check if enabled for the group
            if ctx['message_type'] == 'group' and func[GRP_LIST] and ctx['group_id'] not in func[GRP_LIST]:
                continue
            # handle routine
            try:
                reply_msg = func[CB_FUNC](ctx, G, bot)
            except BaseException:
                reply_msg = ''
            if reply_msg != '':
                G.default_stats[idx] = time.time()
                resp_json = {'reply': reply_msg, 'at_sender': False}
                break
    else:
        # matched command
        ctx['cmd'] = matched_cmd
        try:
            reply_msg = cfg.bot_commands[matched_cmd][CB_FUNC](ctx, G, bot)
        except BaseException:
            print('catch')
            reply_msg = ''
        if reply_msg != '':
            G.cmd_stats[matched_cmd] = time.time()
            resp_json = {'reply': reply_msg, 'at_sender': cfg.bot_commands[matched_cmd][F_AT]}

    if resp_json:
        return resp_json
    else:
        return


if __name__ == '__main__':
    bot.run(host=cfg.host, port=cfg.port)
