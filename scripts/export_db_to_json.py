"""
Export all tables from a PostgreSQL database to JSON files.

Usage:
  python scripts/export_db_to_json.py --database-url <DATABASE_URL> --outdir send_to

If --database-url is omitted the script will read DATABASE_URL from environment.

This script will create the output directory if missing, list all user tables in the connected database (public schema by default),
and write one JSON file per table with UTF-8 encoding. Datetime/Decimal/bytes are handled.

Note: for very large tables you may want to stream/export in chunks or compress the output.
"""
import argparse
import os
import json
import base64
import decimal
from datetime import date, datetime

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except Exception:
    raise RuntimeError("psycopg2 is required. Install with: pip install psycopg2-binary")


def normalize_value(v):
    """Convert DB value to JSON-serializable form."""
    if v is None:
        return None
    if isinstance(v, (int, float, str, bool)):
        return v
    if isinstance(v, decimal.Decimal):
        # convert Decimal to float if safe, else string
        try:
            return float(v)
        except Exception:
            return str(v)
    if isinstance(v, (datetime, date)):
        return v.isoformat()
    # psycopg2 may return memoryview for bytea; convert to bytes
    if isinstance(v, (bytes, bytearray, memoryview)):
        b = bytes(v)
        # encode bytes as base64 to safely transport binary data in JSON
        return "__bytes_base64:" + base64.b64encode(b).decode("ascii")
    # fallback
    return str(v)


def get_tables(conn, schema_filter=None):
    sql = """
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_type = 'BASE TABLE'
      AND table_schema NOT IN ('pg_catalog','information_schema')
    ORDER BY table_schema, table_name
    """
    if schema_filter:
        sql = sql.replace("table_schema NOT IN ('pg_catalog','information_schema')",
                          "table_schema = %s")
        with conn.cursor() as cur:
            cur.execute(sql, (schema_filter,))
            return cur.fetchall()
    else:
        with conn.cursor() as cur:
            cur.execute(sql)
            return cur.fetchall()


def export_table(conn, schema, table, outdir, chunk_size=10000):
    outname = f"{schema}__{table}.json" if schema != 'public' else f"{table}.json"
    outpath = os.path.join(outdir, outname)
    print(f"Exporting {schema}.{table} -> {outpath}")

    # Use server-side cursor for large tables
    cur_name = f"csr_{schema}_{table}"
    with conn.cursor(name=cur_name, cursor_factory=RealDictCursor) as cur:
        cur.itersize = chunk_size
        cur.execute(f"SELECT * FROM {schema}.{table}")

        first = True
        with open(outpath, "w", encoding="utf-8") as f:
            f.write("[")
            rows_written = 0
            for row in cur:
                # normalize row
                norm = {k: normalize_value(v) for k, v in row.items()}
                if not first:
                    f.write(",\n")
                else:
                    first = False
                json.dump(norm, f, ensure_ascii=False)
                rows_written += 1
            f.write("]")
    print(f"  -> finished ({rows_written} rows)")
    return outpath, rows_written


def main():
    parser = argparse.ArgumentParser(description="Export Postgres DB tables to JSON files")
    parser.add_argument("--database-url", "-d", help="Postgres DATABASE_URL (e.g. postgresql://user:pw@host:5432/db)")
    parser.add_argument("--outdir", "-o", default="send_to", help="Output directory for JSON files")
    parser.add_argument("--schema", "-s", default=None, help="Schema to export (default: all non-system schemas)")
    parser.add_argument("--skip", nargs="*", default=[], help="Table names to skip")
    args = parser.parse_args()

    dburl = args.database_url or os.environ.get("DATABASE_URL") or os.environ.get("SQLALCHEMY_DATABASE_URI")
    if not dburl:
        print("ERROR: No database URL provided. Use --database-url or set DATABASE_URL environment variable.")
        return 2

    outdir = os.path.abspath(args.outdir)
    os.makedirs(outdir, exist_ok=True)

    # connect
    print("Connecting to database...")
    conn = psycopg2.connect(dsn=dburl)

    try:
        tables = get_tables(conn, schema_filter=args.schema)
        # tables is list of (table_schema, table_name)
        if not tables:
            print("No tables found to export.")
            return 0

        total_files = 0
        total_rows = 0
        for schema, table in tables:
            if table in args.skip:
                print(f"Skipping {schema}.{table}")
                continue
            _, rows = export_table(conn, schema, table, outdir)
            total_files += 1
            total_rows += rows

        print(f"Done — exported {total_files} tables, {total_rows} total rows to {outdir}")
        return 0
    finally:
        conn.close()


if __name__ == '__main__':
    raise SystemExit(main())
