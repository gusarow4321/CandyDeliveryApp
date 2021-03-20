def str_hours_to_int(hours):
    res = []
    for h in hours:
        split_times = h.split('-')
        h1 = int(split_times[0].split(':')[0]) * 60 + int(split_times[0].split(':')[1])
        h2 = int(split_times[1].split(':')[0]) * 60 + int(split_times[1].split(':')[1])
        res.append([h1, h2])
    return res


def is_ranges_crossing(hours1, hours2):
    range1 = str_hours_to_int(hours1)
    range2 = str_hours_to_int(hours2)
    for t1 in range1:
        for t2 in range2:
            if (t1[0] <= t2[0] <= t1[1]) or (t2[0] <= t1[0] <= t2[1]):
                return True
    return False


def get_max_weight(courier_type):
    return {'foot': 10, 'bike': 15, 'car': 50}[courier_type]


def get_earning_coef(courier_type):
    return {'foot': 2, 'bike': 5, 'car': 9}[courier_type]
