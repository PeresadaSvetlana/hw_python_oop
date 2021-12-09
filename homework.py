from dataclasses import dataclass
from typing import List, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = ('Тип тренировки: {}; '
                    'Длительность: {:.3f} ч.; '
                    'Дистанция: {:.3f} км; '
                    'Ср. скорость: {:.3f} км/ч; '
                    'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        """Вернуть строку с результатами тренировок"""
        return self.message.format(self.training_type,
                                   self.duration,
                                   self.distance,
                                   self.speed,
                                   self.calories)


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTS: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(type(self).__name__,
                            self.duration,
                            self.get_distance(),
                            self.get_mean_speed(),
                            self.get_spent_calories()))


@dataclass
class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.duration_H = duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
        CALORIES_SUBSTRACTER: float = 20

        return ((CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                - CALORIES_SUBSTRACTER)
                * self.weight
                / self.M_IN_KM
                * self.duration_H
                * self.MINUTS)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.duration_H = duration
        self.weight_KG = weight

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CALORIES_WEIGHT_MULTIPLIER: float = 0.035
        CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029

        return ((CALORIES_WEIGHT_MULTIPLIER * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * CALORIES_WEIGHT_MULTIPLIER_2
                * self.weight_KG)
                * (self.duration_H
                * self.MINUTS))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.duration_H = duration
        self.weight_KG = weight

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = (self.length_pool
                      * self.count_pool
                      / self.M_IN_KM
                      / self.duration_H)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        CALORIES_MEAN_SPEED_ADDER: float = 1.1
        CALORIES_WEIGHT_MULTIPLIER: float = 2
        return ((self.get_mean_speed()
                + CALORIES_MEAN_SPEED_ADDER)
                * CALORIES_WEIGHT_MULTIPLIER
                * self.weight_KG)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    package: Dict[str, type] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in package:
        raise ValueError('Тут какая-то ошибка')
    return package[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
