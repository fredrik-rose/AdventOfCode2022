# Day 15: Beacon Exclusion Zone
import copy
import re


def main():
    sensors, beacons = parse("15.txt")
    part_one(copy.deepcopy(sensors), copy.deepcopy(beacons))
    part_two(copy.deepcopy(sensors), copy.deepcopy(beacons))


def parse(file_path):
    sensors = []
    beacons = []
    with open(file_path) as file:
        for line in file:
            data = extract_ints(line)
            assert len(data) == 4
            sensors.append(data[0] + data[1] * 1j)
            beacons.append(data[2] + data[3] * 1j)
    return sensors, beacons


def extract_ints(text):
    return [int(x) for x in re.findall(r'-?\d+', text)]


def part_one(sensors, beacons):
    line = 2000000
    coverages = get_coverages(sensors, beacons)
    segments = get_line_segmens(sensors, coverages, line, get_single_line_segment)
    beacons_on_line = count_beacons_on_line(beacons, line)
    coverage_count = count_coverage(segments)[0]
    answer = coverage_count - beacons_on_line
    print(f"Part one: {answer}")


def part_two(sensors, beacons):
    coverages = get_coverages(sensors, beacons)
    sensors = [rotate_forward(s) for s in sensors]
    events = create_y_events(sensors, coverages)
    for line, action in events:
        line += action
        segmens = get_line_segmens(sensors, coverages, line, get_single_line_segment_for_rotated)
        holes = count_coverage(segmens)[1]
        if holes:
            position = rotate_back(holes[0] + line * 1j)
            answer = int(position.real * 4000000 + position.imag)
            break
    print(f"Part two: {answer}")


def get_coverages(sensors, beacons):
    return [manhattan_distance(s, b) for s, b in zip(sensors, beacons)]


def manhattan_distance(a, b):
    return abs(a.real - b.real) + abs(a.imag - b.imag)


def get_line_segmens(sensors, coverages, line, extractor_function):
    segments = [extractor_function(sensor, coverage, line) for sensor, coverage in zip(sensors, coverages)]
    segments = [e for e in segments if e is not None]
    return sorted(segments)


def get_single_line_segment(sensor, coverage, line):
    distance = manhattan_distance(sensor, sensor.real + line * 1j)
    if distance > coverage:
        return None
    segment = coverage - distance
    return (sensor.real - segment, sensor.real + segment)


def get_single_line_segment_for_rotated(sensor, coverage, line):
    distance = abs(sensor.imag - line)
    if distance > coverage:
        return None
    return (sensor.real - coverage, sensor.real + coverage)


def count_beacons_on_line(beacons, line):
    return len(set(b.real for b in beacons if b.imag == line))


def count_coverage(segments):
    events = create_x_events(segments)
    active = 0
    start = None
    prev = None
    coverage = 0
    single_holes = []
    for position, event in events:
        active += event
        if active == -1 and start is None:
            start = position
            if prev is not None and position - prev == 2:
                single_holes.append(position - 1)
        if active == 0:
            coverage += position - start + 1
            start = None
        prev = position
    return int(coverage), single_holes


def rotate_forward(position):
    return (position.real + position.imag) + ((position.real - position.imag) * 1j)


def rotate_back(position):
    return ((position.real + position.imag) // 2) + (((position.real - position.imag) // 2) * 1j)


def create_y_events(sensors, coverages):
    events = []
    for sensor, distance in zip(sensors, coverages):
        events.append((sensor.imag - distance, -1))
        events.append((sensor.imag + distance, 1))
    return sorted(events)


def create_x_events(segments):
    events = []
    for start, end in segments:
        events.append((start, -1))
        events.append((end, 1))
    return sorted(events)


if __name__ == "__main__":
    main()
