import psycopg
from loguru import logger


class PostgreSql:
    def __init__(self, username: str, password: str, host: str, port: int, db: str):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.db = db

    def get_last_dispute_block(self) -> tuple:
        conn = psycopg.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            dbname=self.db,
        )
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM {self.db} ORDER BY disputeId DESC"
            )
            last_confirmed_block = cur.fetchone()
        return last_confirmed_block

    def get_last_tally_block(self) -> tuple:
        conn = psycopg.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            dbname=self.db,
        )
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM {self.db} WHERE tallied = true ORDER BY disputeId DESC"
            )
            last_tally_block = cur.fetchone()
        return last_tally_block

    def create_tables(self):
        query = (
            f" CREATE TABLE IF NOT EXISTS {self.db} ("
            """ disputeId              integer PRIMARY KEY,
                requestId              integer NOT NULL, 
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
        )
        try:
            conn = None
            conn = psycopg.connect(
                host=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
                dbname=self.db,
            )
            cur = conn.cursor()
            cur.execute(query)
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
                dbname=self.db,
            )
            logger.info(
                f"Inserting {len(disputes)} newly created disputes into database."
            )
            with conn.cursor() as cur:
                for dispute in disputes:

                    cur.execute(
                        """
                        INSERT INTO disputes (disputeId, requestId, disputeTx, disputeTime, disputeBlockNumber, tallied, disputedMiner)
                        VALUES (%s,%s,%s,%s,%s,false,%s)
                        """,
                        (
                            dispute["dispute_id"],
                            dispute["request_id"],
                            dispute["creation_tx"],
                            dispute["time_created"],
                            dispute["creation_block_number"],
                            dispute["disputed_miner_address"],
                        ),
                    )
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
                dbname=self.db,
            )
            logger.info(
                f"Inserting {len(disputes)} newly tallied disputes into database."
            )
            with conn.cursor() as cur:
                for dispute in disputes:
                    cur.execute(
                        """
                        UPDATE disputes
                        SET tallied = true,
                            tally = %s,
                            tallyTx = %s,
                            tallyBlockNumber = %s,
                            result = %s,
                            reportingParty = %s
                        WHERE disputeId = %s AND tallied = false
                        """,
                        (
                            dispute["tally"],
                            dispute["tallied_tx"],
                            dispute["tallied_block_number"],
                            dispute["result"],
                            dispute["reporting_party"],
                            dispute["dispute_id"],
                        ),
                    )
                    conn.commit()
        except (Exception, psycopg.DatabaseError) as error:
            logger.error(error)
        finally:
            if conn is not None:
                conn.close()
