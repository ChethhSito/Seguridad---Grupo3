import unittest

from app import app


class LabBehaviorTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_links_to_forms_and_report(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        for path in ("/inseguro/buscar", "/seguro/buscar", "/inseguro/saludo", "/seguro/saludo", "/reporte"):
            self.assertIn(path, page)
        report = self.client.get("/reporte")
        self.assertEqual(report.status_code, 200)
        report.close()

    def test_normal_search_matches_in_both_routes(self):
        for route in ("/inseguro/buscar", "/seguro/buscar"):
            response = self.client.get(route, query_string={"nombre": "ana"})
            self.assertEqual(response.json, {"usuarios": ["ana"]})

    def test_sql_input_changes_only_insecure_query(self):
        value = "' OR 1=1 -- "
        unsafe = self.client.get("/inseguro/buscar", query_string={"nombre": value})
        safe = self.client.get("/seguro/buscar", query_string={"nombre": value})
        self.assertEqual(unsafe.json, {"usuarios": ["ana", "luis"]})
        self.assertEqual(safe.json, {"usuarios": []})

    def test_html_is_escaped_only_in_safe_route(self):
        value = "<script>alert(1)</script>"
        unsafe = self.client.get("/inseguro/saludo", query_string={"nombre": value})
        safe = self.client.get("/seguro/saludo", query_string={"nombre": value})
        self.assertIn(value, unsafe.get_data(as_text=True))
        self.assertNotIn(value, safe.get_data(as_text=True))
        self.assertIn("&lt;script&gt;", safe.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
