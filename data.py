import math


users = [
    {"name": "강순", "team": "A", "last_group": 1},
    {"name": "김국", "team": "A", "last_group": 1},
    {"name": "남우", "team": "B", "last_group": 1},
    {"name": "이혜", "team": "B", "last_group": 2},
    {"name": "마지", "team": "C", "last_group": 2},
    {"name": "김하", "team": "C", "last_group": 2},
]

# number of Members in each group
M = 2

# number of Groups
G = int(math.ceil(len(users) / M))

N = M * G
assert (N / M == N // M)

# pad dummy users
for _ in range(N - len(users)):
    users.append({"name": "(dummy)", "team": "(dummy)", "last_group": -1})


def is_teammate(u, v):
    return u["team"] == v["team"]


def was_samegroup(u, v):
    return u["last_group"] == v["last_group"]


def pooled_score(u, v):
    b = 0
    if is_teammate(u, v):
        b += 1
    # if was_samegroup(u, v):
    #     b += 1
    return b


def pooled_score_group(offset):
    return sum([pooled_score(users[i], users[j])
                for i in range(offset, offset + M)
                for j in range(i + 1, offset + M)])
