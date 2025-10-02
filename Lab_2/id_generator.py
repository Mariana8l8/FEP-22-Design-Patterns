class IDGenerator:
    __last_id: int = 0

    def register(self, instance: object) -> int:
        self.__last_id += 1
        return self.__last_id