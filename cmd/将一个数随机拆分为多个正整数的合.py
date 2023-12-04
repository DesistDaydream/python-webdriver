import random


def get_track2(distanceTotal, parts):
    amount_list = []
    remaining_amount = distanceTotal
    remaining_parts = parts

    for _ in range(parts - 1):
        # 随机生成一个整数，范围为0到当前剩余金额除以剩余份数的两倍
        amount = random.randint(0, remaining_amount // remaining_parts * 2)
        # 每次减去当前随机金额，用剩余金额进行下次随机获取
        remaining_amount -= amount
        remaining_parts -= 1
        amount_list.append(amount)

    # 最后一个整数为剩余的金额
    amount_list.append(remaining_amount)
    print(amount_list)

    return amount_list


get_track2(200, random.randint(20, 50))
