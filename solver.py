import z3
from data import users, N, M, G, pooled_score, pooled_score_group
from collections import defaultdict
from random import shuffle

# declare variables
groups = [z3.Int('group_of_' + str(i)) for i in range(N)]
total_pooled = z3.Int('total_pooled')


def build_solver():
    o = z3.Optimize()

    for g in range(G):
        o.add(z3.Sum([z3.If(groups[i] == g, 1, 0) for i in range(N)]) == M)

    o.add(total_pooled == z3.Sum([z3.If(groups[i] == groups[j],
                                        pooled_score(users[i], users[j]),
                                        0)
                                  for i in range(N)
                                  for j in range(i + 1, N)]))

    o.minimize(total_pooled)

    return o


def pull_result(m):
    by_group = defaultdict(list)
    for i in range(N):
        by_group[m[groups[i]].as_long()].append(i)

    serialized = [{"name": users[u]["name"],
                   "team": users[u]["team"],
                   "last_group": users[u]["last_group"]}
                  for g in range(G)
                  for u in by_group[g]]

    return serialized


def dump_edn(score, ordered_users):
    import edn_format

    open("demo/src/shuffle_lunch/data.cljc", "w") \
        .write("""(ns shuffle-lunch.data)
    
(def total-pooled %d)

(def users %s)

(def cardinality %d)""" % (score, edn_format.dumps(ordered_users, keyword_keys=True), M))


mode = 2
if mode == 0:
    # dump original
    dump_edn(sum([pooled_score_group(g) for g in range(0, N, M)]), users)
elif mode == 1:
    # simple shuffle
    shuffle(users)
    dump_edn(sum([pooled_score_group(g) for g in range(0, N, M)]), users)
elif mode == 2:
    # dump shuffled
    z3.set_param("smt.random_seed", 10)
    s = build_solver()
    s.set("timeout", 3000)
    s.check()

    m = s.model()
    dump_edn(m[total_pooled].as_long(), pull_result(m))
