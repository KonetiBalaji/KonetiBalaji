#!/usr/bin/env python3
"""Unit tests for update_readme.py core logic."""

import unittest
from update_readme import RepoInfo, generate_goals_section, generate_timestamp, update_section


class TestRepoInfoTimeAgo(unittest.TestCase):
    """Tests for RepoInfo.time_ago property."""

    def _make_repo(self, days_ago: int) -> RepoInfo:
        return RepoInfo(
            name="test",
            url="https://github.com/test/test",
            description="",
            language=None,
            stars=0,
            forks=0,
            days_ago=days_ago,
        )

    def test_today(self):
        self.assertEqual(self._make_repo(0).time_ago, "today")

    def test_yesterday(self):
        self.assertEqual(self._make_repo(1).time_ago, "yesterday")

    def test_days(self):
        self.assertEqual(self._make_repo(3).time_ago, "3 days ago")

    def test_one_week(self):
        self.assertEqual(self._make_repo(7).time_ago, "1 week ago")

    def test_weeks(self):
        self.assertEqual(self._make_repo(14).time_ago, "2 weeks ago")

    def test_one_month(self):
        self.assertEqual(self._make_repo(30).time_ago, "1 month ago")

    def test_months(self):
        self.assertEqual(self._make_repo(90).time_ago, "3 months ago")

    def test_one_year(self):
        self.assertEqual(self._make_repo(365).time_ago, "1 year ago")

    def test_years(self):
        self.assertEqual(self._make_repo(730).time_ago, "2 years ago")


class TestGenerateGoalsSection(unittest.TestCase):
    """Tests for generate_goals_section."""

    def test_empty_repos(self):
        result = generate_goals_section([])
        self.assertIn("check back soon", result)

    def test_single_repo(self):
        repo = RepoInfo(
            name="my-project",
            url="https://github.com/user/my-project",
            description="A cool project",
            language="Python",
            stars=5,
            forks=2,
            days_ago=0,
        )
        result = generate_goals_section([repo])
        self.assertIn("[my-project]", result)
        self.assertIn("A cool project", result)
        self.assertIn("`Python`", result)
        self.assertIn("*Updated today*", result)
        self.assertIn("5", result)
        self.assertIn("2", result)

    def test_repo_no_language_no_stars(self):
        repo = RepoInfo(
            name="docs",
            url="https://github.com/user/docs",
            description="",
            language=None,
            stars=0,
            forks=0,
            days_ago=1,
        )
        result = generate_goals_section([repo])
        self.assertIn("[docs]", result)
        self.assertIn("*Updated yesterday*", result)
        self.assertNotIn("`None`", result)


class TestGenerateTimestamp(unittest.TestCase):
    """Tests for generate_timestamp."""

    def test_format(self):
        result = generate_timestamp()
        self.assertIn("Auto-updated on", result)
        self.assertIn("UTC", result)
        self.assertIn("<div", result)


class TestUpdateSection(unittest.TestCase):
    """Tests for update_section."""

    def test_replaces_section(self):
        content = "before\n<!-- START -->\nold\n<!-- END -->\nafter"
        result = update_section(content, "<!-- START -->", "<!-- END -->", "new\n")
        self.assertIn("<!-- START -->\nnew\n<!-- END -->", result)
        self.assertIn("before", result)
        self.assertIn("after", result)
        self.assertNotIn("old", result)

    def test_missing_markers_returns_unchanged(self):
        content = "no markers here"
        result = update_section(content, "<!-- START -->", "<!-- END -->", "new\n")
        self.assertEqual(result, content)

    def test_multiline_content_replaced(self):
        content = "<!-- A -->\nline1\nline2\nline3\n<!-- B -->"
        result = update_section(content, "<!-- A -->", "<!-- B -->", "replaced\n")
        self.assertEqual(result, "<!-- A -->\nreplaced\n<!-- B -->")


if __name__ == "__main__":
    unittest.main()
