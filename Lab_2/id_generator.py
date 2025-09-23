class IDGenerator:
    __counters: dict[int, object] = {}
    __last_id: int = 0

    def register(self, instance: object) -> int:
        self.__last_id += 1
        self.__counters[self.__last_id] = instance
        return self.__last_id