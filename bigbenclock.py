import time


async def bigben(G, bot):
    groups = []
    hour = int(time.strftime('%I'))
    msg = ''
    for _ in range(hour):
        msg += '当'
    if not groups:
        return
    try:
        for grp in groups:
            await bot.send_group_msg(group_id=grp, message=msg)
    except BaseException:
        return
    bot.logger.info('Big Ben for {} o\'clock'.format(hour))
    return
