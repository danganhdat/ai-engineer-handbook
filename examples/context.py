"""Fit complete recent turns inside a character budget for a local exercise."""


def select_history(turns: list[str], budget: int) -> list[str]:
    if budget < 0:
        raise ValueError("The fixed prompt already exceeds the budget.")
    selected = []
    for turn in reversed(turns):
        turn_cost = len(turn) + 1  # Include a newline separator.
        if turn_cost > budget:
            break
        selected.append(turn)
        budget -= turn_cost
    return list(reversed(selected))


if __name__ == "__main__":
    print(select_history(["User: hello", "User: return an unopened headset"], 35))
