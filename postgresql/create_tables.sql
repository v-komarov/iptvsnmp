CREATE TABLE IF NOT EXISTS circuit (
    cid VARCHAR(20) DEFAULT '',
    circuit_id VARCHAR(100) DEFAULT '',
    date1 VARCHAR(10) DEFAULT '',
    date2 VARCHAR(10) DEFAULT '',
    sid VARCHAR(15) DEFAULT '',
    status INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS devices (
    id INTEGER NOT NULL PRIMARY KEY,
    vendor VARCHAR(50) NOT NULL,
    device VARCHAR(100) NOT NULL,
    snmp_ver VARCHAR(3) NOT NULL,
    data jsonb NOT NULL
);


CREATE UNIQUE INDEX IF NOT EXISTS devices_u ON devices (vendor, device);
CREATE INDEX IF NOT EXISTS devices_j ON devices USING GIN (data);



CREATE TABLE IF NOT EXISTS addresses (
    ip_address VARCHAR(15) NOT NULL PRIMARY KEY,
    device INTEGER REFERENCES devices,
    community VARCHAR(50) NOT NULL
);


