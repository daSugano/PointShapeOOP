import abc
import math
from typing import List, Tuple


class Point(metaclass=abc.ABCMeta):
    # 基底クラスをinterfaceの代わりに用いる
    @abc.abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()


class TwoDPoint(Point):
    def __init__(self, x, y) -> None:
        self.__x = x
        self.__y = y

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y


class Shape(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def doesContain(self, coord: Point) -> bool:
        raise NotImplementedError()


class Ellipse(Shape):
    def __init__(self, center: float, focus: Tuple[TwoDPoint, TwoDPoint], long_axis: float):
        self.__center = center
        self.__focus = focus
        self.__long_axis = long_axis

    @staticmethod
    def __calculate_distance(source: TwoDPoint, target: TwoDPoint) -> float:
        return math.sqrt((source.get_x() - target.get_x())**2 + (source.get_y() - target.get_y())**2)

    def __calculate_focus_distance(self, target: TwoDPoint) -> float:
        """
        楕円には焦点が2つある。
        なお、ある楕円において、first_focus = second_focusであることと、
        その図形が円であることは同値である(多分)
        """
        first_focus = self.__focus[0]
        second_focus = self.__focus[1]
        return self.__calculate_distance(target, first_focus) + self.__calculate_distance(target, second_focus)

    def doesContain(self, target: TwoDPoint) -> bool:
        """
        ある2次元上の点targetが楕円の内部または周上にあるかどうかを判定するには、
        targetとそれぞれの焦点の間の距離の和がlong_axis以下かどうかを調べれば良い。
        ただし、不動小数点の計算には誤差がつきものであるため、許容誤差(allowable_error)
        を設定し、差の絶対値が許容誤差未満ならTrueを返すなど工夫が必要
        """
        allowable_error = 1.0 * 10 ** (-10)
        return abs(self.__calculate_focus_distance(target) - self.__long_axis) < allowable_error


class Polygon(Shape):
    def __init__(self, points: List[TwoDPoint]) -> None:
        self.__points = points

    def doesContain(self, target: TwoDPoint) -> bool:
        """
        多角形において、点の内包判定を実装できれば、Rectangle、Pentagon
        についてはPolygonのdoesContain()をそのまま用いれば良い。
        """
        pass


class Rectangle(Polygon):
    def doesContain(self, target: TwoDPoint) -> bool:
        return super().doesContain(target)


class Pentagon(Polygon):
    def doesContain(self, target: TwoDPoint) -> bool:
        return super().doesContain(target)


if __name__ == "__main__":
    e = Ellipse(0.0, (TwoDPoint(1.0, 0.0), TwoDPoint(-1.0, 0.0)), 6.0)
    p = TwoDPoint(3.000000001, 0)
    print(e.doesContain(p))
