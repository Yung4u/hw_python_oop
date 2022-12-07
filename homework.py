class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    # константа расстояния за один шаг (метр)
    LEN_STEP: float = 0.65
    # константа расстояния за один гребок (метр)
    LEN_SWIM: float = 1.38
    # константа для перевода значений из метров в километры
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed: float = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    # константы для расчета калорий после бега
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                                 * self.get_mean_speed()
                                 + self.CALORIES_MEAN_SPEED_SHIFT)
                                 * self.weight / self.M_IN_KM
                                 * self.duration * self.MIN_IN_H)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # константы для расчета калорий после спортивой ходьбы
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self, action: int, duration: float, weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        spent_calories: float = ((self.CALORIES_WEIGHT_MULTIPLIER
                                 * self.weight
                                 + ((self.get_mean_speed()
                                  * self.KMH_IN_MSEC) ** 2
                                  / (self.height / self.CM_IN_M))
                                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                                 * self.weight) * self.duration
                                 * self.MIN_IN_H)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    # константы для расчета калорий после плавания
    SWIMMING_CALORIES_WEIGHT_MULTIPLIER: int = 2
    SWIMMING_CALORIES_MEAN_SPEED_MULTIPLIER: float = 1.1
    LEN_STEP: float = 1.38

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return super().get_distance()

    def get_mean_speed(self) -> float:
        mean_speed: float = (self.length_pool * self.count_pool
                             / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories: float = (
            (self.get_mean_speed()
             + self.SWIMMING_CALORIES_MEAN_SPEED_MULTIPLIER)
            * self.weight
            * self.SWIMMING_CALORIES_WEIGHT_MULTIPLIER
            * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types: dict[str, type[Training]] = {'RUN': Running, 'WLK': SportsWalking,
                                        'SWM': Swimming}
    sport: Training = types[workout_type](*data)
    return sport


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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
