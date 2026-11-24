import unittest
from unittest.mock import patch
from src.order_service import create_order

class TestOrderService(unittest.TestCase):

    def setUp(self):
        self.data = {
            "customer_name": "Mahasiswa FT",
            "tenant_name": "Kantin Teknik",
            "food_name": "Nasi Ayam",
            "quantity": 2,
            "unit_price": 15000,
            "pickup_time": "2026-11-25T12:30:00+07:00"
        }

    @patch("src.order_service.get_table")
    def test_create_order(self, mock_get_table):
        result = create_order(self.data)

        self.assertEqual(result["total_price"], 30000)
        self.assertEqual(result["status"], "PENDING")
        self.assertIn("order_id", result)
        self.assertIn("created_at", result)
        self.assertIn("updated_at", result)

        mock_get_table.return_value.put_item.assert_called_once_with(
            Item=result,
            ConditionExpression="attribute_not_exists(order_id)"
        )

    @patch("src.order_service.get_table")
    def test_invalid_quantity(self, mock_get_table):
        self.data["quantity"] = -1

        with self.assertRaises(ValueError):
            create_order(self.data)

        mock_get_table.assert_not_called()

    @patch("src.order_service.get_table")
    def test_missing_field(self, mock_get_table):
        del self.data["food_name"]

        with self.assertRaises(ValueError):
            create_order(self.data)

        mock_get_table.assert_not_called()

    @patch("src.order_service.get_table")
    def test_invalid_price(self, mock_get_table):
        self.data["unit_price"] = 0

        with self.assertRaises(ValueError):
            create_order(self.data)

        mock_get_table.assert_not_called()

if __name__ == "__main__":
    unittest.main()