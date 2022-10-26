#!/usr/bin/env python3
import random

from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///some_db.db", echo=True)
# engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)

metadat_obj = MetaData()


with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        #[{"x": 1, "y": 1}, {"x": 2, "y": 4}],
        [{"x": random.randint(1, 99), "y": random.randint(1, 99)} for _ in range(15)]
    )
    conn.commit()

with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 93, "y": 11}],
    )

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM some_table"))
    for row in result:
        print(f"x: {row.x} y: {row.y}")

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM some_table WHERE x >= :x"), {"x": 15})

    print(f"total: {len(result.keys())}")

    for r in result:
        print(f"{r.x, r.y}")

stmt = text("SELECT * FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for r in result:
        print(f"x: {r.x} y:{r.y}")


with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()
