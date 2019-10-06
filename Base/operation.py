from typing import List


class Operation:
    @staticmethod
    def move_side(array: List, element, start=True):
        position = array.index(element)
        if start:
            if position == -1:
                return [element, *array]
            else:
                return [element, *array[:position], *array[position+1:]]
        else:
            if position == -1:
                return [*array, element]
            else:
                return [*array[:position], *array[position+1:], element]

    @staticmethod
    def ip_int2dot(ip_int):
        ip_dot = []
        for _ in range(4):
            ip_dot.append(ip_int % 256)
            ip_int //= 256
        ip_dot.reverse()
        ip_dot = list(map(str, ip_dot))
        return '.'.join(ip_dot)


O = Operation
