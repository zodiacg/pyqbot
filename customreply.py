import random
import re


async def nature_of_human(ctx, G, bot):
    try:
        _last_repeat_msg = G.last_repeat_msg
    except AttributeError:
        G.set_plugin_storage('last_repeat_msg', '')
        _last_repeat_msg = ''
    rnd = random.random()
    grp_id = ctx['group_id']

    if grp_id not in _last_repeat_msg:
        _last_repeat_msg[grp_id] = ''
    last_repeat = _last_repeat_msg[grp_id]

    last_msg = G.find_msg(grp_id, 0, 2)
    # follow repeating with 0.9 prob
    if len(last_msg) >= 2 and last_msg[0][1] == last_msg[1][1] and last_msg[0][0] != last_msg[1][0] \
            and rnd < 0.8 and last_msg[0][1] != last_repeat:
        _last_repeat_msg[grp_id] = last_msg[0][1]
        return last_msg[0][1]
    # start repeating with 0.01 prob
    if rnd < 0.01 and last_msg[0][1] != last_repeat:
        _last_repeat_msg[grp_id] = last_msg[0][1]
        return last_msg[0][1]


async def guna(ctx, G, bot):
    rnd = random.random()
    if rnd < 0.55:
        return '没有，guna'


async def stalker(ctx, G, bot):
    grp_id = ctx['group_id']
    usr_id = int(re.match(r'^(\d+)刚[刚才]说了(啥|什么)[?？]?$', ctx['message']).group(1))
    grp_usr_lst = await bot.get_group_member_list(group_id=grp_id)
    for usr in grp_usr_lst:
        if usr['user_id'] == usr_id:
            last_msg = G.find_msg(grp_id, usr_id)[::-1]
            if last_msg:
                resp_msg = '{}刚才说：\n'.format(usr['card'] or usr['nickname'])
                for idx, msg in enumerate(last_msg):
                    resp_msg += '{}.{}\n'.format(idx + 1, msg[1])
            else:
                resp_msg = '{}刚才啥也没说'.format(usr['card'] or usr['nickname'])
            return resp_msg
    return '谁啊，不认识'


async def echo_priv(ctx, G, bot):
    await bot.send_private_msg(user_id=ctx['user_id'], message='你发了：')
    return ctx['message']
