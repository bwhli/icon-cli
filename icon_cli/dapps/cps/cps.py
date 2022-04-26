from icon_cli.contracts import Contracts
from icon_cli.icx import Icx
from icon_cli.utils import die, hex_to_int


class Cps(Icx):
    def __init__(self, network) -> None:
        super().__init__(network)

        if network != "mainnet":
            die("This command only supports mainnet at this time.", "error")

    ##############################
    # PROPOSALS/PROGRESS REPORTS #
    ##############################

    def get_active_proposals(self) -> list:
        contributor_addresses = self.get_contributors()
        active_proposals = []
        for contributor_address in contributor_addresses:
            proposals = self._get_active_proposals(contributor_address)
            if len(proposals) > 0:
                for proposal in proposals:
                    proposal["last_progress_report"] = hex_to_int(
                        proposal["last_progress_report"]
                    )
                    proposal["new_progress_report"] = hex_to_int(
                        proposal["new_progress_report"]
                    )
                    active_proposals.append(proposal)
        return active_proposals

    def get_progress_reports(self):
        params = {"_status": "_waiting", "_end_index": 50, "_start_index": 0}
        progress_reports = self.call(
            Contracts.get_contract_from_name("cps", self.network),
            "get_progress_reports",
            params,
        )
        for progress_report in progress_reports["data"]:
            for k, v in progress_report.items():
                if v[:2] == "0x":
                    print("Hello!")
                    progress_report[k] = hex_to_int(v)

        return progress_reports

    def get_remaining_progress_reports_to_vote(self, address: str):
        params = {"_wallet_address": address, "_project_type": "progress_report"}
        progress_reports = self.call(
            Contracts.get_contract_from_name("cps", self.network),
            "get_remaining_project",
            params,
        )
        return progress_reports

    def get_remaining_proposals_to_vote(self, address: str):
        params = {"_wallet_address": address, "_project_type": "proposal"}
        proposals = self.call(
            Contracts.get_contract_from_name("cps", self.network),
            "get_remaining_project",
            params,
        )
        return proposals

    ################
    # CONTRIBUTORS #
    ################

    def get_contributors(self) -> list:
        params = {"_start_index": 0, "_end_index": 100}
        contributors = self.call(
            Contracts.get_contract_from_name("cps", self.network),
            "get_contributors",
            params,
        )
        return contributors

    def get_validators(self) -> list:
        validators = self.call(
            Contracts.get_contract_from_name("cps", self.network), "get_PReps"
        )
        for validator in validators:
            validator["delegated"] = int(validator["delegated"], 16)
        return validators

    ############
    # TREASURY #
    ############

    def get_treasury_balance(self) -> int:
        balance = self.call(
            Contracts.get_contract_from_name("cps", self.network), "get_remaining_fund"
        )
        balance["ICX"] = hex_to_int(balance["ICX"])
        balance["bnUSD"] = hex_to_int(balance["bnUSD"])
        return balance

    ##############################
    # INTERNAL UTILITY FUNCTIONS #
    ##############################

    def _get_active_proposals(self, address: str):
        params = {"_wallet_address": address}
        proposals = self.call(
            Contracts.get_contract_from_name("cps", self.network),
            "get_active_proposals",
            params,
        )
        return proposals
