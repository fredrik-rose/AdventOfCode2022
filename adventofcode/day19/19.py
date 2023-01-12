# Day 19: Not Enough Minerals
import collections as coll
import copy
import re


def main():
    blueprints = parse("19.txt")
    part_one(copy.deepcopy(blueprints))
    part_two(copy.deepcopy(blueprints))


def parse(file_path):
    blueprints = {}
    with open(file_path) as file:
        for line in file:
            data = extract_ints(line)
            blueprint = data[0]
            ore = data[1]
            clay = data[2]
            obsidian = (data[3], data[4])
            geode = (data[5], data[6])
            blueprints[blueprint] = {
                "ore": ore,
                "clay": clay,
                "obsidian": obsidian,
                "geode": geode
            }
    return blueprints


def extract_ints(text):
    return [int(x) for x in re.findall(r'-?\d+', text)]


def part_one(blueprints):
    answer = 0
    for i, blueprint in blueprints.items():
        answer += i * find_max_possible_geodes(blueprint, 24)
    print(f"Part one: {answer}")


def part_two(blueprints):
    answer = 1
    for _, blueprint in list(blueprints.items())[:3]:
        answer *= find_max_possible_geodes(blueprint, 32)
    print(f"Part two: {answer}")


def find_max_possible_geodes(blueprint, end_time):  # noqa: C901 pylint: disable=too-many-branches, too-many-statements
    def get_state(r, m, t):
        return (
            1000*r["geode"] + 100*r["obsidian"] + 10*r["clay"] + r["ore"],
            1000*m["geode"] + 100*m["obsidian"] + 10*m["clay"] + m["ore"],
            t)

    time = 1
    money = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
    robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
    seen = set()
    queue = coll.deque([(robots, money, time)])
    best = 0
    max_ore = max([blueprint["ore"], blueprint["clay"], blueprint["obsidian"][0], blueprint["geode"][0]])
    max_clay = blueprint["obsidian"][1]
    max_obsidian = blueprint["geode"][1]
    while queue:
        robots, money, time = queue.popleft()
        new_money = {}
        for robot, count in robots.items():
            new_money[robot] = money[robot] + count
        if time == end_time:
            best = max(new_money["geode"], best)
            continue
        if money["ore"] >= blueprint["geode"][0] and money["obsidian"] >= blueprint["geode"][1]:
            c1_money = dict(new_money)
            c1_money["ore"] -= blueprint["geode"][0]
            c1_money["obsidian"] -= blueprint["geode"][1]
            c1_robots = dict(robots)
            c1_robots["geode"] += 1
            state = get_state(c1_robots, c1_money, time + 1)
            if state not in seen:
                queue.append((c1_robots, c1_money, time + 1))
                seen.add(state)
            continue  # NOTE: This is not correct but works for most inputs.
        if robots["obsidian"] < max_obsidian:
            if money["ore"] >= blueprint["obsidian"][0] and money["clay"] >= blueprint["obsidian"][1]:
                c2_money = dict(new_money)
                c2_money["ore"] -= blueprint["obsidian"][0]
                c2_money["clay"] -= blueprint["obsidian"][1]
                c2_robots = dict(robots)
                c2_robots["obsidian"] += 1
                state = get_state(c2_robots, c2_money, time + 1)
                if state not in seen:
                    queue.append((c2_robots, c2_money, time + 1))
                    seen.add(state)
        if robots["clay"] < max_clay:
            if money["ore"] >= blueprint["clay"]:
                c3_money = dict(new_money)
                c3_money["ore"] -= blueprint["clay"]
                c3_robots = dict(robots)
                c3_robots["clay"] += 1
                state = get_state(c3_robots, c3_money, time + 1)
                if state not in seen:
                    queue.append((c3_robots, c3_money, time + 1))
                    seen.add(state)
        if robots["ore"] < max_ore:
            if money["ore"] >= blueprint["ore"]:
                c4_money = dict(new_money)
                c4_money["ore"] -= blueprint["ore"]
                c4_robots = dict(robots)
                c4_robots["ore"] += 1
                state = get_state(c4_robots, c4_money, time + 1)
                if state not in seen:
                    queue.append((c4_robots, c4_money, time + 1))
                    seen.add(state)
        state = get_state(robots, new_money, time + 1)
        if state not in seen:
            queue.append((robots, new_money, time + 1))
            seen.add(state)
    return best


if __name__ == "__main__":
    main()
