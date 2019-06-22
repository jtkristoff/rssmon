# as postgres user
CREATE DATABASE rssmon OWNER jtk;
# as jtk
CREATE TABLE anchor (
  id            BIGINT UNIQUE NOT NULL PRIMARY KEY,
  probe         BIGINT NOT NULL,
  country       TEXT NOT NULL,
  city          TEXT NOT NULL,
  ip_v4         INET NOT NULL,
  as_v4         BIGINT NOT NULL,
  ip_v6         INET,
  as_v6         BIGINT
);

CREATE TABLE measure_soa (
    ts       TIMESTAMP NOT NULL,
    probe    BIGINT NOT NULL,
    type     TEXT NOT NULL,
    ns       TEXT NOT NULL,
    rt       NUMERIC (8, 3) NOT NULL
);
