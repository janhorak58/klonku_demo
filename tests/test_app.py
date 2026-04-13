import unittest

from app import create_app
from app.state import store
from mock_backend import create_app as create_backend_app


class FrontendSmokeTests(unittest.TestCase):
    def setUp(self):
        store.reset()
        self.backend_app = create_backend_app()
        self.backend_app.testing = True
        self.backend_client = self.backend_app.test_client()
        self.app = create_app()
        self.app.testing = True
        self.app.config["BACKEND_TEST_CLIENT"] = self.backend_client
        self.client = self.app.test_client()

    def login_student(self):
        return self.client.post(
            "/login",
            data={"email": "jan.novak@tul.cz", "password": "demo12345"},
            follow_redirects=False,
        )

    def login_admin(self):
        return self.client.post(
            "/login",
            data={"email": "petra.svobodova@klonku.cz", "password": "admin12345"},
            follow_redirects=False,
        )

    def test_public_routes_render(self):
        for path in ["/login", "/register", "/forgot-password", "/reset-password", "/demo"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)

    def test_student_flow_routes_render(self):
        login_response = self.login_student()
        self.assertEqual(login_response.status_code, 302)

        for path in [
            "/dashboard",
            "/projects/proj-sentiment",
            "/projects/proj-sentiment/versions/ver-sentiment-3/analysis",
            "/projects/proj-sentiment/versions/ver-sentiment-3",
            "/projects/proj-sentiment/versions/ver-sentiment-3/diff",
            "/profile",
        ]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)

    def test_admin_routes_render(self):
        login_response = self.login_admin()
        self.assertEqual(login_response.status_code, 302)

        for path in [
            "/admin",
            "/admin/users",
            "/admin/users/user-jan",
            "/admin/faculties",
            "/admin/faculties/fm/pipeline",
            "/admin/error-types",
            "/admin/allowed-domains",
            "/admin/audit-log",
        ]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, path)

    def test_analysis_status_endpoint_returns_json(self):
        self.login_student()
        response = self.client.get("/api/analysis-status/proj-logistics/ver-logistics-1")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("status", payload)
        self.assertIn("progress", payload)

    def test_older_versions_render_results_and_diff(self):
        self.login_student()
        self.assertEqual(self.client.get("/projects/proj-sentiment/versions/ver-sentiment-2").status_code, 200)
        self.assertEqual(self.client.get("/projects/proj-sentiment/versions/ver-sentiment-2/diff").status_code, 200)
        self.assertEqual(self.client.get("/projects/proj-small-business/versions/ver-business-5").status_code, 200)
        self.assertEqual(self.client.get("/projects/proj-small-business/versions/ver-business-5/diff").status_code, 200)

    def test_backend_contains_endpoint_surface_from_spec(self):
        actual = set()
        for rule in self.backend_app.url_map.iter_rules():
            for method in sorted(rule.methods - {"HEAD", "OPTIONS"}):
                actual.add((method, rule.rule))

        expected = {
            ("POST", "/auth/register"),
            ("POST", "/auth/login"),
            ("POST", "/auth/google"),
            ("POST", "/auth/refresh"),
            ("POST", "/auth/logout"),
            ("GET", "/auth/verify-email/<token>"),
            ("POST", "/auth/forgot-password"),
            ("POST", "/auth/reset-password"),
            ("GET", "/users/me"),
            ("PUT", "/users/me"),
            ("GET", "/users/me/usage"),
            ("GET", "/projects"),
            ("POST", "/projects"),
            ("GET", "/projects/<project_id>"),
            ("PUT", "/projects/<project_id>"),
            ("DELETE", "/projects/<project_id>"),
            ("GET", "/projects/<project_id>/pipeline-config"),
            ("PUT", "/projects/<project_id>/pipeline-config"),
            ("GET", "/projects/<project_id>/versions"),
            ("POST", "/projects/<project_id>/versions"),
            ("GET", "/projects/<project_id>/versions/<version_id>"),
            ("GET", "/projects/<project_id>/versions/<version_id>/document"),
            ("GET", "/projects/<project_id>/versions/<version_id>/errors"),
            ("GET", "/projects/<project_id>/versions/<version_id>/diff"),
            ("DELETE", "/projects/<project_id>/versions/<version_id>"),
            ("GET", "/projects/<project_id>/versions/<version_id>/analysis"),
            ("POST", "/projects/<project_id>/versions/<version_id>/analysis/retry"),
            ("GET", "/faculties/<faculty_id>/pipeline-steps"),
            ("GET", "/errors/<error_id>"),
            ("GET", "/error-types"),
            ("GET", "/admin/users"),
            ("GET", "/admin/users/<user_id>"),
            ("PUT", "/admin/users/<user_id>"),
            ("DELETE", "/admin/users/<user_id>"),
            ("GET", "/admin/faculties"),
            ("POST", "/admin/faculties"),
            ("GET", "/admin/faculties/<faculty_id>/pipeline-steps"),
            ("POST", "/admin/faculties/<faculty_id>/pipeline-steps"),
            ("PUT", "/admin/pipeline-steps/<step_id>"),
            ("DELETE", "/admin/pipeline-steps/<step_id>"),
            ("GET", "/admin/error-types"),
            ("POST", "/admin/error-types"),
            ("PUT", "/admin/error-types/<type_id>"),
            ("DELETE", "/admin/error-types/<type_id>"),
            ("GET", "/admin/allowed-domains"),
            ("POST", "/admin/allowed-domains"),
            ("PATCH", "/admin/allowed-domains/<domain_id>"),
            ("DELETE", "/admin/allowed-domains/<domain_id>"),
            ("GET", "/admin/audit-log"),
        }

        self.assertTrue(expected.issubset(actual), expected - actual)


if __name__ == "__main__":
    unittest.main()
