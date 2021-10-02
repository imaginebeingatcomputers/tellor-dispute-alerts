import requests
import json
from .eth_utils import twos_comp


class EtherscanInstance:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_disputes(self, from_block: int) -> list[dict]:
        url = "https://api.etherscan.io/api"

        payload = {
            "apikey": self.api_key,
            "module": "logs",
            "action": "getLogs",
            "fromBlock": from_block,
            "toBlock": "latest",
            "address": "0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0",
            "topic0": "0xeceec1aebf67772b2440120c4b4dc913a1fe1b865509219f9456785c23b9da64",
        }

        parsed = False
        attempts = 0
        parsed_disputes = []
        while not parsed and attempts < 6:
            attempts += 1
            response = requests.request("GET", url, params=payload)
            if response.status_code == 200:
                logs = json.loads(response.text)["result"]
                for dispute in logs:
                    parsed_dispute = {}
                    parsed_dispute["dispute_id"] = int(dispute["topics"][1], 16)
                    parsed_dispute[
                        "disputed_miner_address"
                    ] = f"{dispute['data'][-40:]}"
                    parsed_dispute["creation_block_number"] = int(
                        dispute["blockNumber"], 16
                    )
                    parsed_dispute["time_created"] = int(dispute["timeStamp"], 16)
                    parsed_dispute["creation_tx"] = dispute["transactionHash"]
                    parsed_disputes.append(parsed_dispute)
        return parsed_disputes

    def get_disputes_tallied(self, from_block: int) -> list[dict]:
        url = "https://api.etherscan.io/api"

        payload = {
            "apikey": self.api_key,
            "module": "logs",
            "action": "getLogs",
            "fromBlock": from_block,
            "toBlock": "latest",
            "address": "0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0",
            "topic0": "0x21459c2f5447ebcf83a7f0a238c32c71076faef0d12295e771c0cb1e10434739",
        }
        parsed = False
        attempts = 0
        while not parsed and attempts < 6:
            attempts += 1
            response = requests.request("GET", url, params=payload)
            if response.status_code == 200:
                logs = json.loads(response.text)["result"]
                parsed_disputes = []
                for dispute in logs:
                    parsed_dispute = {}
                    parsed_dispute["dispute_id"] = int(dispute["topics"][1], 16)
                    parsed_dispute["tallied_block_number"] = int(
                        dispute["blockNumber"], 16
                    )
                    parsed_dispute["time_tallied"] = int(dispute["timeStamp"], 16)
                    parsed_dispute["tallied_tx"] = dispute["transactionHash"]
                    parsed_dispute["tally"] = twos_comp(
                        int(dispute["data"][:66], 16), 256
                    )
                    parsed_dispute["result"] = bool(int(dispute["data"][-64:], 16))
                    parsed_dispute["reporting_party"] = "0x{dispute['data'][90:130]}"
                    parsed_disputes.append(parsed_dispute)
        return parsed_disputes
