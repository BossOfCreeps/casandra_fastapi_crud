CREATE KEYSPACE IF NOT EXISTS test WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : '1' };

CREATE TABLE IF NOT EXISTS test.example_model
(
    example_id   uuid PRIMARY KEY,
    created_at   timestamp,
    description  text,
    example_type int
);