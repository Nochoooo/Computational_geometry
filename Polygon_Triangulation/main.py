from collections import Counter

def calculation_determinant(triangle):
    determinant = (triangle[1][0] - triangle[0][0]) * (triangle[2][1] - triangle[0][1]) - (
            triangle[1][1] - triangle[0][1]) * (triangle[2][0] - triangle[0][0])
    return determinant


def is_triangle_equal(tri1, tri2):
    points1 = sorted(tri1, key=lambda p: (p[0], p[1]))
    points2 = sorted(tri2, key=lambda p: (p[0], p[1]))
    if points1 == points2:
        return True
    else:
        return False


def check_triangulation(polygon, subdivision) -> bool:
    if len(polygon) == 3 and len(subdivision) == 1 and calculation_determinant(polygon) != 0 and is_triangle_equal(
            polygon, subdivision[0]):
        return True
    if len(polygon) - 2 != len(subdivision):
        return False

    for triangle in subdivision:
        if len(triangle) != 3:
            return False
        if not set(triangle).issubset(polygon):
            return False

    subdivision_vertices = [item for sublist in subdivision for item in sublist]
    subdivision_vertices_counter = Counter(subdivision_vertices)
    subdivision_vertices_counter_list = [list(i) for i in subdivision_vertices_counter.items()]
    while len(subdivision) > 1:
        point2 = point = (0, 0)
        point_exist = False
        for i in range(len(subdivision_vertices_counter_list)):
            if subdivision_vertices_counter_list[i][1] == 1:
                point = subdivision_vertices_counter_list[i][0]
                point_exist = True
                break
        if not point_exist:
            return False

        index = subdivision_vertices.index(point)
        index_triangle = index // 3
        triangle1 = subdivision.pop(index_triangle)
        triangle1.remove(point)
        a = triangle1[0]
        b = triangle1[1]
        points_to_remove = 111
        for item in subdivision_vertices_counter_list:
            if item[0] == point or item[0] == a or item[0] == b:
                if item[0] == point and points_to_remove // 100 == 1:
                    item[1] -= 1
                    points_to_remove -= 100
                elif item[0] == a and (points_to_remove % 100) // 10 == 1:
                    item[1] -= 1
                    points_to_remove -= 10
                elif item[0] == b and points_to_remove % 10 == 1:
                    item[1] -= 1
                    points_to_remove -= 1
            if points_to_remove == 0:
                break

        subdivision_vertices.pop(index_triangle * 3 + 2)
        subdivision_vertices.pop(index_triangle * 3 + 1)
        subdivision_vertices.pop(index_triangle * 3)

        for triangle2 in subdivision:
            if a in triangle2 and b in triangle2:
                for x in triangle2:
                    if x != a and x != b:
                        point2 = x
                break
        else:
            return False

        x0 = b[0] - a[0]
        y0 = b[1] - a[1]
        x1 = point[0] - a[0]
        y1 = point[1] - a[1]
        x2 = point2[0] - a[0]
        y2 = point2[1] - a[1]
        if (x0 * y1 - x1 * y0) * (x0 * y2 - x2 * y0) >= 0:
            return False
    return True


if __name__ == '__main__':
    with open('data.txt', 'r') as file:
        polygon = eval(file.readline())
        subdivision = eval(file.readline())

    with open('result.txt', 'w') as file:
        file.write("Result - " + str(check_triangulation(polygon, subdivision)))