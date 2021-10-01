import os


class config:
    def __init__(self, env: bool):
        if env:
            self.pg_username = os.getenv("PG_USERNAME")
            self.pg_password = os.getenv("PG_PASSWORD")
            self.pg_host = os.getenv("PG_HOST") or "localhost"
            self.pg_port = os.getenv("PG_PORT") or "5432"
            self.etherscan_url = (
                os.getenv("ETHERSCAN_URL") or "htps://api.etherscan.io/api"
            )
            self.etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")
            self.discord_webook_url = os.getenv("DISCORD_WEBHOOK_URL")
