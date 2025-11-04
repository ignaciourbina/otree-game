from otree.api import Bot, Submission

from . import pages


class PlayerBot(Bot):
    cases = ["min_runtime", "benchmarkish", "max_runtime"]

    def play_round(self):
        options = sorted(
            self.group.runtime_options(), key=lambda option: option["runtime"]
        )

        if self.case == "benchmarkish":
            target = self.group.bounded_optimal_runtime
            choice = min(options, key=lambda option: abs(option["runtime"] - target))
        elif self.case == "max_runtime":
            choice = options[-1]
        else:
            choice = options[0]

        yield Submission(pages.Decision, {"runtime_choice": choice["id"]})
        yield pages.Results

        assert self.player.token_payoff >= self.group.token_floor
        assert self.player.runtime_years == choice["runtime"]
