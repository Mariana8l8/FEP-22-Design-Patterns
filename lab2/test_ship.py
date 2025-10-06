import unittest
from containers import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from ship import Ship
from port import Port

class TestShip(unittest.TestCase):

    def setUp(self):
        # Створюємо порт та корабель для всіх тестів
        self.port1 = Port(1, 0.0, 0.0)
        self.port2 = Port(2, 3.0, 4.0)  # Відстань ~5
        self.ship = Ship(
            ID=1,
            fuel=1000.0,
            totalWeightCapacity=5000,
            maxNumberOfAllContainers=10,
            maxNumberOfHeavyContainers=5,
            maxNumberOfRefrigeratedContainers=2,
            maxNumberOfLiquidContainers=2,
            fuelConsumptionPerKM=1.0,
            currentPort=self.port1
        )

    def test_load_basic_container(self):
        container = BasicContainer(1, 2000)
        result = self.ship.load(container)
        self.assertTrue(result)
        self.assertIn(container, self.ship.containers)

    def test_load_overweight_container(self):
        container = BasicContainer(2, 6000)  # Більше за totalWeightCapacity
        result = self.ship.load(container)
        self.assertFalse(result)

    def test_load_too_many_containers(self):
        for i in range(10):
            self.ship.load(BasicContainer(i, 100))
        extra_container = BasicContainer(99, 50)
        result = self.ship.load(extra_container)
        self.assertFalse(result)

    def test_load_heavy_limit(self):
        for i in range(5):
            self.ship.load(HeavyContainer(i, 300))
        extra_heavy = HeavyContainer(99, 100)
        result = self.ship.load(extra_heavy)
        self.assertFalse(result)

    def test_load_refrigerated_limit(self):
        for i in range(2):
            self.ship.load(RefrigeratedContainer(i, 200))
        extra_r = RefrigeratedContainer(99, 100)
        result = self.ship.load(extra_r)
        self.assertFalse(result)

    def test_load_liquid_limit(self):
        for i in range(2):
            self.ship.load(LiquidContainer(i, 200))
        extra_l = LiquidContainer(99, 100)
        result = self.ship.load(extra_l)
        self.assertFalse(result)

    def test_unload_container(self):
        c = BasicContainer(1, 100)
        self.ship.load(c)
        result = self.ship.unLoad(c)
        self.assertTrue(result)
        self.assertNotIn(c, self.ship.containers)

    def test_unload_nonexistent_container(self):
        c = BasicContainer(2, 100)
        result = self.ship.unLoad(c)
        self.assertFalse(result)

    def test_sailTo_enough_fuel(self):
        c = BasicContainer(1, 100)
        self.ship.load(c)
        result = self.ship.sailTo(self.port2)
        self.assertTrue(result)
        self.assertEqual(self.ship.currentPort, self.port2)

    def test_sailTo_not_enough_fuel(self):
        # Дуже важкий контейнер, щоб не вистачило палива
        self.ship.fuel = 1
        c = HeavyContainer(1, 10000)
        self.ship.load(c)
        result = self.ship.sailTo(self.port2)
        self.assertFalse(result)
        self.assertEqual(self.ship.currentPort, self.port1)

    def test_refuel(self):
        self.ship.fuel = 0
        self.ship.reFuel(100)
        self.assertEqual(self.ship.fuel, 100)

if __name__ == "__main__":
    unittest.main()
