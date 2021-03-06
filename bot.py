import re
import time

from aiocqhttp import CQHttp

import config as cfg
from internal import *
from internal import const as C

G = Holder()

bot = CQHttp(access_token='abracadabra',
             enable_http_post=False)


def general_check(ctx, cmd, func):
    # check cooldown
    if func[CD_TIME] != 0 and cmd in G.cmd_stats and time.time() - G.cmd_stats[cmd] < func[CD_TIME]:
        return False
    # filter private and group
    if ctx['message_type'] not in func[F_PRIV_GRP]:
        return False
    # check if enabled for the group
    if ctx['message_type'] == 'group' and func[WHITELIST] and ctx['group_id'] not in func[WHITELIST]:
        return False
    # check if enabled for the friend, but allow everything for superuser
    if func[F_PRIV_GRP] == {'private'} and func[WHITELIST] and ctx['user_id'] not in func[WHITELIST] \
            and ctx['user_id'] != cfg.super_user:
        return False
    return True


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
        # general check
        if not general_check(ctx, cmd, func):
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
            cmd = f'_default_routine_{idx}'
            if not general_check(ctx, cmd, func):
                continue
            # handle routine
            try:
                reply_msg = await func[CB_FUNC](ctx, G, bot)
            except BaseException as e:
                print('default', e)
                reply_msg = ''
            if reply_msg:
                G.cmd_stats[cmd] = time.time()
                bot.logger.info('Msg processed by default routine {}: {}'.format(idx, func[CB_FUNC].__name__))
                resp_json = {'reply': reply_msg, 'at_sender': False}
                break
    else:
        # matched command
        ctx['cmd'] = matched_cmd
        try:
            reply_msg = await cfg.bot_commands[matched_cmd][CB_FUNC](ctx, G, bot)
        except BaseException as e:
            print('cmd', e)
            reply_msg = ''
        if reply_msg:
            G.cmd_stats[matched_cmd] = time.time()
            bot.logger.info('Msg processed by matched cmd: {}'.format(cfg.bot_commands[matched_cmd][CB_FUNC].__name__))
            resp_json = {'reply': reply_msg, 'at_sender': cfg.bot_commands[matched_cmd][F_AT]}

    if resp_json:
        return resp_json
    else:
        return


if __name__ == '__main__':
    # add tasks
    for func, job_time in cfg.scheduled_tasks:
        G.scheduler.add_job(func, trigger='cron', args=(G, bot), **job_time)


    def _start_scheduler():
        # use configure to make sure scheduler get the correct event loop
        G.scheduler.configure(cfg.scheduler_opt)
        G.scheduler.start()


    bot.server_app.before_serving(_start_scheduler)
    bot.run(host=cfg.host, port=cfg.port, debug=True)
