import json
import unittest
from unittest.mock import patch
from src.database import BUCKET_NAME
from src.order_service import create_order


class TestOrderService(unittest.TestCase):

    def setUp(self):
        self.valid_data = {
            "customer_name": "Rila",
            "tenant_name": "Masakan Jawa",
            "food_name": "Nasi Ayam",
            "quantity": 2,
            "unit_price": 15000,
            "pickup_time": "2026-11-25T12:00:00+07:00"
        }

    @patch("src.order_service.get_s3_client")
    def test_create_order(self, mock_s3_client):
        order = create_order(self.valid_data)

        self.assertIn("order_id", order)
        self.assertEqual(order["total_price"], 30000)
        self.assertEqual(order["status"], "PENDING")
        self.assertIn("created_at", order)
        self.assertIn("updated_at", order)

        mock_s3 = mock_s3_client.return_value

        mock_s3.put_object.assert_called_once_with(
            Bucket=BUCKET_NAME,
            Key=f"orders/{order['order_id']}.json",
            Body=json.dumps(order).encode("utf-8"),
            ContentType="application/json"
        )

    @patch("src.order_service.get_s3_client")
    def test_invalid_quantity(self, mock_s3_client):
        data = self.valid_data.copy()
        data["quantity"] = 0

        with self.assertRaises(ValueError):
            create_order(data)

        mock_s3_client.assert_not_called()

    @patch("src.order_service.get_s3_client")
    def test_invalid_price(self, mock_s3_client):
        data = self.valid_data.copy()
        data["unit_price"] = -15000

        with self.assertRaises(ValueError):
            create_order(data)

        mock_s3_client.assert_not_called()

    @patch("src.order_service.get_s3_client")
    def test_missing_field(self, mock_s3_client):
        data = self.valid_data.copy()
        del data["food_name"]

        with self.assertRaises(ValueError):
            create_order(data)

        mock_s3_client.assert_not_called()


if __name__ == "__main__":
    unittest.main()