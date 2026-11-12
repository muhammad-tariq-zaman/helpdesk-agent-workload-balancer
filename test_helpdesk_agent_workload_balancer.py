import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import analyse, suggest, load_status

def row(agent, skill, open_tickets, capacity):
    return {"agent": agent, "skill": skill, "open_tickets": str(open_tickets),
            "capacity": str(capacity)}

class TestWorkloadBalancer(unittest.TestCase):
    def test_load_percent(self):
        self.assertEqual(analyse([row("ali", "network", 6, 10)])[0]["load_pct"], 60.0)
    def test_overloaded(self):
        self.assertEqual(analyse([row("ali", "network", 12, 10)])[0]["status"], "OVERLOADED")
    def test_at_capacity(self):
        self.assertEqual(analyse([row("ali", "network", 10, 10)])[0]["status"], "AT CAPACITY")
    def test_available(self):
        self.assertEqual(analyse([row("ali", "network", 3, 10)])[0]["status"], "AVAILABLE")
    def test_highest_load_first(self):
        r = analyse([row("a", "network", 2, 10), row("b", "network", 9, 10)])
        self.assertEqual(r[0]["agent"], "b")
    def test_suggest_least_loaded(self):
        agents = analyse([row("a", "network", 8, 10), row("b", "network", 2, 10)])
        self.assertEqual(suggest(agents, 1), ["b"])
    def test_suggest_respects_skill(self):
        agents = analyse([row("a", "printer", 1, 10), row("b", "network", 5, 10)])
        self.assertEqual(suggest(agents, 1, skill="network"), ["b"])
    def test_suggest_skips_full_agent(self):
        agents = analyse([row("a", "network", 10, 10), row("b", "network", 2, 10)])
        self.assertEqual(suggest(agents, 1, skill="network"), ["b"])
    def test_suggest_reports_no_capacity(self):
        agents = analyse([row("a", "network", 10, 10)])
        self.assertEqual(suggest(agents, 1, skill="network"), [])
