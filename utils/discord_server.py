from discord import RequestsWebhookAdapter, Webhook
from loguru import logger


class DiscordServer:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def post_tally(self, disputes: list) -> None:
        webhook = Webhook.from_url(
            self.webhook_url,
            adapter=RequestsWebhookAdapter(),
        )
        logger.info(f"Posting {len(disputes)} newly created nodes to discord.")
        for dispute in disputes:
            webhook.send(
                f"Node {dispute['dispute_id']} created.\n https://etherscan.io/tx/{dispute['creation_tx']}"
            )

    def post_dispute(self, disputes: list[dict]) -> None:
        webhook = Webhook.from_url(
            self.webhook_url,
            adapter=RequestsWebhookAdapter(),
        )
        logger.info(f"Posting {len(disputes)} newly confirmed nodes to discord.")
        for dispute in disputes:
            webhook.send(
                f"Node {dispute['dispute_id']} tallied.\n https://etherscan.io/tx/{dispute['tally_tx']}"
            )
