# helpdesk-agent-workload-balancer

Balance helpdesk workload from a CSV of agents: load percent per agent, OVERLOADED / AT CAPACITY / AVAILABLE status, and with --new-tickets it suggests the least-loaded available agent with the requested skill for each new ticket.

## How to run

```sh
python3 main.py agents.csv --new-tickets 2 --skill network
```

## Example output

```
ali (network): AVAILABLE (6/10 tickets, 60.0%)
sara (network): OVERLOADED (12/10 tickets, 120.0%)
Assign next ticket to: ali
Assign next ticket to: ali
1 agent(s) overloaded.
```

Standard library only. Run the tests with `python3 -m unittest discover`.
