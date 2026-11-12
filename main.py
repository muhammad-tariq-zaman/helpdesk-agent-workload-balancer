"""Balance helpdesk workload across agents and suggest who takes the next ticket.

Usage: python3 main.py agents.csv [--new-tickets 3] [--skill network]
CSV columns: agent,skill,open_tickets,capacity.
Load percent = open_tickets / capacity * 100.
- OVERLOADED: open tickets above capacity.
- AT CAPACITY: open tickets exactly at capacity.
- AVAILABLE: room for more tickets.
When --new-tickets is given, the least-loaded AVAILABLE agent with
the requested --skill (or any skill, if none is given) is suggested
for each new ticket, one at a time, updating the load as it goes.
"""
import argparse, csv, sys

def load_status(open_tickets, capacity):
    if open_tickets > capacity:
        return "OVERLOADED"
    if open_tickets == capacity:
        return "AT CAPACITY"
    return "AVAILABLE"

def analyse(rows):
    out = []
    for row in rows:
        open_tickets = int(row["open_tickets"])
        capacity = int(row["capacity"])
        pct = round(open_tickets / capacity * 100, 1) if capacity else 0.0
        out.append({"agent": row["agent"].strip(),
                    "skill": row["skill"].strip().lower(),
                    "open": open_tickets, "capacity": capacity,
                    "load_pct": pct,
                    "status": load_status(open_tickets, capacity)})
    return sorted(out, key=lambda a: (-a["load_pct"], a["agent"]))

def suggest(agents, new_tickets, skill=None):
    pool = [dict(a) for a in agents
            if a["status"] != "OVERLOADED" and a["open"] < a["capacity"]
            and (skill is None or a["skill"] == skill.lower())]
    assignments = []
    for _ in range(new_tickets):
        if not pool:
            break
        chosen = min(pool, key=lambda a: (a["open"], a["agent"]))
        assignments.append(chosen["agent"])
        chosen["open"] += 1
        if chosen["open"] >= chosen["capacity"]:
            pool.remove(chosen)
    return assignments

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    parser.add_argument("--new-tickets", type=int, default=0,
                        help="new tickets to assign (default: 0, report only)")
    parser.add_argument("--skill", default=None,
                        help="skill the new tickets need (default: any)")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        agents = analyse(list(csv.DictReader(f)))
    for agent in agents:
        print(f"{agent['agent']} ({agent['skill']}): {agent['status']} "
              f"({agent['open']}/{agent['capacity']} tickets, {agent['load_pct']:.1f}%)")
    if args.new_tickets > 0:
        assigned = suggest(agents, args.new_tickets, args.skill)
        for agent in assigned:
            print(f"Assign next ticket to: {agent}")
        if len(assigned) < args.new_tickets:
            print(f"No capacity for {args.new_tickets - len(assigned)} ticket(s).")
    print(f"{sum(1 for a in agents if a['status'] == 'OVERLOADED')} agent(s) overloaded.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
