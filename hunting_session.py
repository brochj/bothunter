from dataclasses import dataclass, field


@dataclass
class HuntingSession:
    term: str
    analyzed_accounts: set[str] = field(default_factory=set)
    possible_bots_found: set[str] = field(default_factory=set)

    def total_accounts_analyzed(self) -> int:
        return len(self.analyzed_accounts)

    def total_possible_bots_found(self) -> int:
        return len(self.possible_bots_found)

    def add_possible_bot(self, username: str) -> None:
        self.possible_bots_found.add(username)

    def add_analyzed_account(self, username: str) -> None:
        self.analyzed_accounts.add(username)
