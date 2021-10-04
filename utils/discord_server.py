from discord import RequestsWebhookAdapter, Webhook
from loguru import logger
import discord


class DiscordServer:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def post_tally(self, disputes: list) -> None:
        webhook = Webhook.from_url(
            self.webhook_url,
            adapter=RequestsWebhookAdapter(),
        )
        logger.info(f"Posting {len(disputes)} newly tallied disputes to discord.")
        for dispute in disputes:
            message = discord.Embed(title="Dispute tallied", description=f"Dispute {dispute['dispute_id']} tallied.", url=f"https://etherscan.io/tx/{dispute['tallied_tx']}")
            message.add_field(name="Tallied Dispute ID", value=dispute['dispute_id'])
            message.add_field(name="Tally", value=dispute['tally'])
            message.add_field(name="Result", value="Successfully Disputed" if dispute['result'] else "Dispute rejected")
            webhook.send(embed=message)

    def post_dispute(self, disputes: list[dict]) -> None:
        webhook = Webhook.from_url(
            self.webhook_url,
            adapter=RequestsWebhookAdapter(),
        )
        logger.info(f"Posting {len(disputes)} newly created disputes to discord.")
        for dispute in disputes:
            message = discord.Embed(title="Dispute created", description=f"Dispute {dispute['dispute_id']} created.", url=f"https://etherscan.io/tx/{dispute['creation_tx']}")
            message.add_field(name="Disputed Request ID", value=dispute['dispute_id'])
            message.add_field(name="Disputed Miner", value=dispute["disputed_miner_address"])
            webhook.send(embed=message)
