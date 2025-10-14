import unittest
from models.port import Port
from models.ship import Ship
from models.container import BasicContainer, HeavyContainer

class TestPortShipSimulation(unittest.TestCase):
    def setUp(self):
        self.port1 = Port(1, 50.0, 30.0)
        self.port2 = Port(2, 51.0, 31.0)

        self.ship = Ship(
            ship_id=101,
            current_port=self.port1,
            fuel=500.0,
            total_weight_capacity=10000,
            max_all=10,
            max_heavy=5,
            max_refrigerated=2,
            max_liquid=2,
            fuel_per_km=1.5
        )
        self.port1.incoming_ship(self.ship)

        self.basic_container = BasicContainer(1, 2000)
        self.heavy_container = HeavyContainer(2, 4000)
        self.port1.containers.extend([self.basic_container, self.heavy_container])

    def test_load_container(self):
        result = self.ship.load(self.basic_container)
        self.assertTrue(result)
        self.assertIn(self.basic_container, self.ship.containers)
        self.assertNotIn(self.basic_container, self.port1.containers)

    def test_unload_container(self):
        self.ship.load(self.basic_container)
        result = self.ship.unload(self.basic_container)
        self.assertTrue(result)
        self.assertNotIn(self.basic_container, self.ship.containers)
        self.assertIn(self.basic_container, self.port1.containers)

    def test_sail_to_port(self):
        self.ship.load(self.basic_container)
        self.ship.sail_to(self.port2)
        self.assertEqual(self.ship.current_port, self.port2)
        self.assertIn(self.ship, self.port2.current)
        self.assertNotIn(self.ship, self.port1.current)

    def test_fuel_consumption(self):
        self.ship.load(self.basic_container)
        initial_fuel = self.ship.fuel
        self.ship.sail_to(self.port2)
        self.assertLess(self.ship.fuel, initial_fuel)

if __name__ == "__main__":
    unittest.main()
