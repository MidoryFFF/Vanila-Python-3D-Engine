import turtle as tu
import math

class vector3:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def normalize(self):
        vector_magnitude = self.magnitude()
        self.x /= vector_magnitude
        self.y /= vector_magnitude
        self.z /= vector_magnitude

    def normalized_vetor(self):
        vector_magnitude = self.magnitude()
        new_vector = self / vector_magnitude
        return new_vector

    def magnitude(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def to_2D(self):
        if (self.z != 0):
            return (self.x/abs(self.z), self.y/abs(self.z))
        else:
            return (self.x, self.y)

    def ScreenPoints(self, WIDTH, HEIGHT):
        x, y = self.to_2D()
        x = x*WIDTH
        y = y*HEIGHT
        return x, y

    def to_list(self):
        return self.x, self.y, self.z

    def __truediv__(self, other):
        if (not isinstance(other, (int, float)) or other == 0):
            raise ValueError("Деление возможно только на ненулевое число")
        else:
            return vector3(self.x / other, self.y / other, self.z / other)

    def __mul__(self, other):
        if (not isinstance(other, (int, float))):
            raise ValueError("Умножение возможно только на число")
        else:
            return vector3(self.x * other, self.y * other, self.z * other)

    def __add__(self, other):
        if (not isinstance(other, (vector3))):
            raise ValueError("Сложение возможно только между векторами")
        else:
            return vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        if (not isinstance(other, (vector3))):
            raise ValueError("Вычетание возможно только между векторами")
        else:
            return self + (other * (-1))

    def __str__(self):
        return str([self.x, self.y, self.z])

class Matrix3x3:
    def __init__(self, matrixVolues: list[list[float]] = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]):
        self.volues = matrixVolues

    def __add__(self, other):
        if (isinstance(other, Matrix3x3)):
            result_matrix = [[0, 0, 0] for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    result_matrix[i][j] = self.volues[i][j] + other.volues[i][j]
            return Matrix3x3(result_matrix)
        else:
            raise ValueError("Поддерживаеться только сложение матриц 3 на 3")
        # if (isinstance(other, (int, float))):

    def __mul__(self, other):
        if (isinstance(other, (int, float))):
            result_matrix = [[0, 0, 0] for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    result_matrix[i][j] = self.volues[i][j] * other
            return Matrix3x3(result_matrix)
        if (isinstance(other, Matrix3x3)):
            result_matrix = [[0, 0, 0] for _ in range(3)]
            for i in range(3):
                for j in range(3):
                    for k in range(3):
                        result_matrix[i][j] += self.volues[i][k] * other.volues[k][j]
            return Matrix3x3(result_matrix)
        if (isinstance(other, vector3)):
            result_vector = [0, 0 ,0]
            for i in range(3):
                for j in range(3):
                    result_vector[i] += self.volues[i][j] * other.to_list()[j]
            return vector3(result_vector[0], result_vector[1], result_vector[2])
        else:
            raise ValueError("Ошибка выбора умножаемого типа типа")


class Shape3D:
    MAX_PENSIZE = 50
    WIDTH = 800
    HEIGHT = 800

    def __init__(self, pointsList: list[vector3], connectionsList: list[list[int]], centerOfMass: vector3, globalPosition: vector3):
        self.mass_center: vector3 = centerOfMass
        self.global_position: vector3 = globalPosition
        self.scale = 1
        self.rotation_points_list: dict[vector3, list[int]] = [[i + self.mass_center, []] for i in pointsList]
        for i in connectionsList:
            if (i[0] < len(self.rotation_points_list) and i[1] < len(self.rotation_points_list)):
                self.rotation_points_list[i[0]][1].append(i[1])

    def shift_shape(self, newGlobalPosition: vector3):
        self.global_position = newGlobalPosition

    def rotate(self, angle: float, axis: vector3):
        axis.normalize()
        #angle %= 360
        R = Matrix3x3()
        K = Matrix3x3([[0, axis.z * (-1), axis.y], 
                       [axis.z, 0, axis.x * (-1)],
                       [axis.y * (-1), axis.x, 0]])
        R += K * math.sin(angle)
        R += K * K * (1 - math.cos(angle))
        for point in range(len(self.rotation_points_list)):
            self.rotation_points_list[point][0] = R * self.rotation_points_list[point][0]

    def change_scale(self, scale: float):
        self.scale = max(0, scale)

    def to_2D(self):
        poitns_list_2D = [vector3(i.x/(abs(i.z) if i.z != 0 else 1) * Shape3D.WIDTH, ((i.y/abs(i.z)) if i.z != 0 else 0) * Shape3D.HEIGHT, i.z) for i in self.rotation_points_list]
        return poitns_list_2D

    def DrawShape(self):
        for point_index in range(len(self.rotation_points_list)):
            for t_point_index in range(len(self.rotation_points_list[point_index][1])):
                from_point = (self.rotation_points_list[point_index][0] * self.scale) + self.global_position
                to_point = (self.rotation_points_list[self.rotation_points_list[point_index][1][t_point_index]][0] * self.scale) + self.global_position
                Shape3D.DrawLine(from_point, to_point, "green")

    def UpdateShape(self, DeltaTime: float):
        pass

    def __str__(self):
        string = ""
        for i in self.rotation_points_list:
            string += str(i) + "\n" + str([str(i) for i in self.rotation_points_list[i]]) + "\n"
        return string

    def DrawLine(from_point: vector3, to_point: vector3, color: str, is_debug = False):
        thikness = 0
        if ((from_point.z + to_point.z)/2 > 0):
            thikness = Shape3D.MAX_PENSIZE/abs((from_point.z + to_point.z)/2)
        if (from_point.z <= 0 and to_point.z <= 0):
            tu.color("black")
        else:
            tu.color(color)
        tu.pensize(thikness)
        tu.penup()
        tu.goto(from_point.ScreenPoints(WIDTH=Shape3D.WIDTH, HEIGHT=Shape3D.HEIGHT))
        tu.pendown()
        if (is_debug):
            tu.dot(thikness*2)
        tu.goto(to_point.ScreenPoints(WIDTH=Shape3D.WIDTH, HEIGHT=Shape3D.HEIGHT))
        tu.update()

class Space3D:
    defaul_shapes = {
        "cube": Shape3D([vector3(list(map(float, i.split(",")))[0], list(map(float, i.split(",")))[1], list(map(float, i.split(",")))[2]) for i in "1,1,-1;-1,1,-1;-1,-1,-1;1,-1,-1;1,1,1;-1,1,1;-1,-1,1;1,-1,1".split(";")], 
                       [[0, 1], [1, 2], [2, 3], [3, 0],
                        [4, 5], [5, 6], [6, 7], [7, 4],
                        [0, 4], [1, 5], [2, 6], [3, 7]], 
                        vector3(0, 0, 0), vector3(0, 0, 0)),
        "tetraider": Shape3D([vector3(list(map(float, i.split(",")))[0], list(map(float, i.split(",")))[1], list(map(float, i.split(",")))[2]) for i in "-1,-1,-1;1,-1,-1;0,-1,1;0,1,-0.25".split(";")],
                       [[0, 1], [1, 2], [2, 3], [3, 0],
                        [3, 1], [2, 0]],
                        vector3(0, 0, 0), vector3(0, 0, 0))
    }

    def __init__(self):
        self.shapes: list[Shape3D] = []
        tu.bgcolor("black")
        tu.tracer(0, 0)
        tu.hideturtle()

    def __add__(self, other):
        if (not isinstance(other, Shape3D)):
            raise ValueError("Отрисовка поддерживается только для фигур")
        else:
            self.shapes.append(other)

    def __sub__(self, other):
        if (not isinstance(other, Shape3D)):
            raise ValueError("Отрисовка поддерживается только для фигур")
        else:
            self.shapes.remove(other)

    def Update(self, deltaTime):
        tu.clear()
        for shape in self.shapes:
            shape.DrawShape()
        tu.update()

if (__name__ == "__main__"):
    import time
    space = Space3D()
    space + Space3D.defaul_shapes["tetraider"]
    TIME = 0
    DELTA_TIME = 1/60

    distanse = 2
    while TIME <= 1000:
        TIME_SECNCE_START = TIME * DELTA_TIME
        space.Update(TIME_SECNCE_START)
        ratationg_vector: vector3 = vector3(math.sin(TIME_SECNCE_START + 5) * distanse, math.cos(TIME_SECNCE_START + 5) * distanse, 0)
        space.shapes[0].shift_shape(vector3(math.sin(TIME_SECNCE_START + 5) * distanse, math.cos(TIME_SECNCE_START + 5) * distanse, 10))
        space.shapes[0].rotate(DELTA_TIME * distanse/2, ratationg_vector)
        #space.shapes[0].change_scale(math.sin(TIME_SECNCE_START)/2 + 1)
        TIME += 1
        time.sleep(DELTA_TIME)
    tu.done()

