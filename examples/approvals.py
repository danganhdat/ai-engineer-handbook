"""Model the state transitions for a single in-memory note proposal."""

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class Proposal:
    run_id: str
    owner: str
    text: str


@dataclass
class NoteStore:
    proposals: dict[str, Proposal] = field(default_factory=dict)
    decisions: dict[str, Literal["approved", "rejected"]] = field(default_factory=dict)
    notes: dict[str, str] = field(default_factory=dict)

    def propose(self, proposal: Proposal) -> None:
        if proposal.run_id in self.proposals:
            raise ValueError("Run already has a proposal.")
        if not proposal.text.strip() or len(proposal.text) > 500:
            raise ValueError("A note must have 1 to 500 characters.")
        self.proposals[proposal.run_id] = proposal

    def decide(self, run_id: str, actor: str, *, approved: bool) -> str:
        proposal = self.proposals[run_id]
        if actor != proposal.owner:
            raise PermissionError("Only the owner can decide.")
        if run_id not in self.decisions:
            if approved:
                self.notes[run_id] = proposal.text
                self.decisions[run_id] = "approved"
            else:
                self.decisions[run_id] = "rejected"
        return self.decisions[run_id]


if __name__ == "__main__":
    store = NoteStore()
    store.propose(Proposal("run-1", "training", "Review the returns policy."))
    print(f"Before approval: {len(store.notes)} notes")
    print(store.decide("run-1", "training", approved=True))
    store.decide("run-1", "training", approved=True)
    print(f"After repeating approval: {len(store.notes)} note")
