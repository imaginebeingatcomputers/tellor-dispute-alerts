import psycopg
from loguru import logger


class PostgreSql:
    def __init__(self, username: str, password: str, host: str, port: int):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def get_last_dispute_block(self) -> tuple:
        conn = psycopg.connect(
            host=self.host, port=self.port, user=self.username, password=self.password
        )
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM disputes WHERE tallied = True ORDER BY disputeId DESC"
            )
            last_confirmed_block = cur.fetchone()
        return last_confirmed_block

    def get_last_tally_block(self) -> tuple:
        conn = psycopg.connect(
            host=self.host, port=self.port, user=self.username, password=self.password
        )
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM disputes WHERE tallied = False ORDER BY disputeId DESC"
            )
            last_tally_block = cur.fetchone()
        return last_tally_block

    def create_tables(self):
        commands = [
            """ CREATE TABLE IF NOT EXISTS disputes (
                        disputeId              integer PRIMARY KEY,
                        disputeTx              varchar NOT NULL,
                        disputeTime            integer NOT NULL,
                        disputeBlockNumber     integer NOT NULL,
                        tallied                boolean NOT NULL, 
                        disputedMiner          varchar NOT NULL,
                        tally                  numeric,
                        tallyTx                varchar,
                        tallyBlockNumber       integer,
                        result                 varchar,
                        reportingParty         varchar
                      ) """
        ]
        try:
            conn = None
            conn = psycopg.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
            )
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            cur.close()
            conn.commit()
            logger.info("Tables created successfully")
        except (Exception, psycopg.DatabaseError) as error:
            logger.error(error)
        finally:
            if conn is not None:
                conn.close()

    def insert_disputes(self, disputes: list[dict]) -> None:
        try:
            conn = None
            conn = psycopg.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
            )
            logger.info(
                f"Inserting {len(disputes)} newly created disputes into database."
            )
            with conn.cursor() as cur:
                for dispute in disputes:
                    query = (
                        "INSERT INTO disputes (disputeId, disputeTx, disputeTime, disputeBlockNumber, tallied, disputedMiner)"
                        "VALUES ("
                        f"    {dispute['dispute_id']},"
                        f"    {dispute['creation_tx']},"
                        f"    {dispute['time_created']},"
                        f"    {dispute['creation_block_number']},"
                        "    false,"
                        f"    {dispute['disputed_miner_address']}"
                        ")"
                    )
                    cur.execute(query)
                    conn.commit()
        except (Exception, psycopg.DatabaseError) as error:
            logger.error(error)
        finally:
            if conn is not None:
                conn.close()

    def update_tallied_disputes(self, disputes: list) -> None:
        try:
            conn = None
            conn = psycopg.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
            )
            logger.info(
                f"Inserting {len(disputes)} newly tallied disputes into database."
            )
            with conn.cursor() as cur:
                for dispute in disputes:
                    query = (
                        "UPDATE disputes"
                        "SET tallied = true"
                        f"    tally = {dispute['tally']}"
                        f"    tallyTx = {dispute['tallied_tx']}"
                        f"    tallyBlockNumber = {dispute['tallied_block_number']}"
                        f"    result = {dispute['result']}"
                        f"    reportingParty = {dispute['reporting_party']}"
                        f"WHERE dispute_id = {dispute['dispute_id']} AND tallied = false"
                    )
                    cur.execute(query)
                    conn.commit()
        except (Exception, psycopg.DatabaseError) as error:
            logger.error(error)
        finally:
            if conn is not None:
                conn.close()
