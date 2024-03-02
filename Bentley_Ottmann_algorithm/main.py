import bintrees
import ujson


def find_intersections(horizontal_segments, vertical_segments):
    events = []
    for x, y1, _, y2 in vertical_segments:
        events.append((x, 2, "vertical", (y1, y2)))
    for x1, y, x2, _ in horizontal_segments:
        events.append((x1, 1, "begin", y))
        events.append((x2, 3, "end", y))

    events.sort()

    status = bintrees.RBTree()
    intersections = []

    for event in events:
        x, _, event_type, y = event
        if event_type == "begin":
            status.insert(y, None)
        elif event_type == "end":
            status.discard(y)
        elif event_type == "vertical":
            if status and status.min_key() <= y[1]:
                start = status.ceiling_key(y[0])
                end = status.floor_key(y[1])
                items = status.key_slice(start, end)
                for y_value in items:
                    intersections.append((x, y_value))
                intersections.append((x, end))

    return intersections


if __name__ == '__main__':
    with open('data.txt', 'r') as file:
        horizontal_segments = ujson.loads(file.readline())
        vertical_segments = ujson.loads(file.readline())

    with open('result.txt', 'w') as file:
        file.write("Result - " + str(find_intersections(horizontal_segments, vertical_segments)))
