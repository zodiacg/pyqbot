import random


def nature_of_human(ctx, G, bot):
    rnd = random.random()
    grp_id = ctx['group_id']
    last_msg = G.find_msg(grp_id, 0, 2)
    # follow repeating with 0.9 prob
    if last_msg[0][1] == last_msg[1][1] and last_msg[0][0] != last_msg[1][0] and rnd < 0.9:
        return last_msg[0][1]
    # start repeating with 0.02 prob
    if rnd < 0.02:
        return last_msg[0][1]


def guna(ctx, G, bot):
    rnd = random.random()
    if rnd < 0.55:
        return '没有，guna'


def reply_match(ctx, G, bot):
    pass
