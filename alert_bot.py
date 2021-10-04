from utils.discord_server import DiscordServer
from loguru import logger
from datetime import datetime
import sched
import time
from utils.postgresql import PostgreSql
import argparse
from utils.etherscan import EtherscanInstance

s = sched.scheduler(time.time, time.sleep)
log_time = datetime.utcnow()
logger.add(f"file_{log_time.year}.{log_time.day}.{log_time.month}.log")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pg-password",
        "-p",
        type=str,
        action="store",
        dest="pg_password",
        required=True,
    )
    parser.add_argument(
        "--pg-username",
        "-u",
        type=str,
        action="store",
        dest="pg_username",
        required=True,
    )
    parser.add_argument(
        "--pg-host",
        type=str,
        action="store",
        dest="pg_host",
        required=True,
    )
    parser.add_argument(
        "--pg-port",
        "-o",
        type=str,
        action="store",
        dest="pg_port",
        required=True,
    )
    parser.add_argument(
        "--etherscan-api-key",
        action="store",
        type=str,
        dest="etherscan_api_key",
        required=True,
    )
    parser.add_argument(
        "--etherscan_url",
        type=str,
        action="store",
        dest="etherscan_url",
        default="https://api.etherscan.io/api",
    )
    parser.add_argument(
        "--discord-webook-url",
        type=str,
        dest="discord_webook_url",
        required=True,
    )
    parser.add_argument(
        "--daemonize",
        "-d",
        action="store_true",
    )
    parser.add_argument(
        "--database-name",
        type=str,
        action="store",
        dest="database_name",
        default="disputes",
    )
    args = parser.parse_args()
    return args


def update(arg_namespace, pg_instance):
    etherscan_instance = EtherscanInstance(api_key=arg_namespace.etherscan_api_key)
    discord_instance = DiscordServer(webhook_url=arg_namespace.discord_webook_url)
    last_dispute = pg_instance.get_last_dispute_block()
    if last_dispute is None:
        disputes = etherscan_instance.get_disputes(11895800)
        pg_instance.insert_disputes(disputes)
    else:
        try:
            disputes = etherscan_instance.get_disputes(last_dispute[3] + 1)
            if len(disputes) != 0:
                discord_instance.post_dispute(disputes)
                pg_instance.insert_disputes(disputes)
        except (KeyError, Exception) as error:
            logger.warning("Failed retrieving last dispute")
            logger.error(error)
    last_tallied = pg_instance.get_last_tally_block()
    if last_tallied is None:
        tallied_disputes = etherscan_instance.get_disputes_tallied(11895800)
        pg_instance.update_tallied_disputes(tallied_disputes)
    else:
        try:
            tallied_disputes = etherscan_instance.get_disputes_tallied(last_tallied[9] + 1)
            if len(tallied_disputes) != 0:
                discord_instance.post_tally(tallied_disputes)
                pg_instance.update_tallied_disputes(tallied_disputes)
        except (KeyError, Exception) as error:
            logger.warning("Failure retrieving last tally.")
            logger.error(error)


def main():
    arg_namespace = parse_args()
    pg_instance = PostgreSql(
        username=arg_namespace.pg_username,
        password=arg_namespace.pg_password,
        host=arg_namespace.pg_host,
        port=arg_namespace.pg_port,
        db=arg_namespace.database_name,
    )
    pg_instance.create_tables()
    if arg_namespace.daemonize:
        while True:
            update(arg_namespace, pg_instance)
            time.sleep(300)
    else:
        update(arg_namespace, pg_instance)


if __name__ == "__main__":
    main()
