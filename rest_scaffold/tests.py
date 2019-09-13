"""
Unit tests
"""

import json

from django.contrib.auth.models import Group
from django.db.models import Model
from django.test import TestCase

from .templatetags.rest_scaffold import rest_scaffold


class RestScaffoldTemplateTagTestCase(TestCase):
    """
    Tests for the `rest_scaffold` template tag.
    """

    def test_user_with_app(self):
        """
        Test with ``User`` model, with both model and app provided.
        """
        s = json.loads(
            rest_scaffold(
                {"csrf_token": "example_csrf_token"},
                "user",
                "auth",
                api_root="/api",
                fields="id,username",
            )["configuration"]
        )
        expected_config = json.loads(
            json.dumps(
                {
                    "title": "Users",
                    "subtitle": "auth / User",
                    "recordTitle": "User",
                    "pkField": "id",
                    "fields": ["id", "username"],
                    "url": "/api/auth/user",
                    "csrfToken": "example_csrf_token",
                }
            )
        )
        for t in ["title", "subtitle", "recordTitle", "pkField", "url", "csrfToken"]:
            self.assertEqual(expected_config[t], s[t])
        self.assertEqual([x["name"] for x in s["fields"]], expected_config["fields"])

    def test_group_without_app(self):
        """
        Test with ``Group`` model, with only the model string provided.
        """
        s = json.loads(
            rest_scaffold(
                {"csrf_token": "example_csrf_token"},
                "group",
                api_root="/api",
                fields="id,name",
            )["configuration"]
        )
        expected_config = json.loads(
            json.dumps(
                {
                    "title": "Groups",
                    "subtitle": "auth / Group",
                    "recordTitle": "Group",
                    "pkField": "id",
                    "fields": ["id", "name"],
                    "url": "/api/auth/group",
                    "csrfToken": "example_csrf_token",
                }
            )
        )
        for t in ["title", "subtitle", "recordTitle", "pkField", "url", "csrfToken"]:
            self.assertEqual(expected_config[t], s[t])
        self.assertEqual([x["name"] for x in s["fields"]], expected_config["fields"])

    def test_group_with_model_object(self):
        """
        Test with ``Group`` model, passing the model object.
        """
        s = json.loads(
            rest_scaffold(
                {"csrf_token": "example_csrf_token"},
                Group,
                api_root="/api",
                fields="id,name",
            )["configuration"]
        )
        expected_config = json.loads(
            json.dumps(
                {
                    "title": "Groups",
                    "subtitle": "auth / Group",
                    "recordTitle": "Group",
                    "pkField": "id",
                    "fields": ["id", "name"],
                    "url": "/api/auth/group",
                    "csrfToken": "example_csrf_token",
                }
            )
        )
        for t in ["title", "subtitle", "recordTitle", "pkField", "url", "csrfToken"]:
            self.assertEqual(expected_config[t], s[t])
        self.assertEqual([x["name"] for x in s["fields"]], expected_config["fields"])

    def test_bad_model(self):
        """
        Test passing an invalid model string.
        """
        s = rest_scaffold({}, "xyz")
        self.assertEqual(s.get("error"), "model not found")

    def test_bad_model_object(self):
        """
        Test passing an invalid model object.
        """
        s = rest_scaffold({}, Model)
        self.assertEqual(s.get("error"), "model not installed")

    def test_bad_model_type(self):
        """
        Test passing an object that isn't even a model.
        """
        s = rest_scaffold({}, 3)
        self.assertEqual(s.get("error"), "model is not the proper type")

    def test_bad_app(self):
        """
        Test passing an invalid app string.
        """
        s = rest_scaffold({}, "xyz", "xyz")
        self.assertTrue(s.get("error"), "app not found")

    def test_bad_model_in_app(self):
        """
        Test passing an invalid model string with a valid app string.
        """
        s = rest_scaffold({}, "xyz", "auth")
        self.assertTrue(s.get("error"), "model not found in that app")
