from . import pages
from ._builtin import Bot


class PlayerBot(Bot):
    cases = [
        {
            'p2_decision': {'contract_accepted': True, 'agent_work_effort': 10},
            'p1_payoff': c(46),
            'p2_payoff': c(34),
        },
        {
            'p2_decision': {'contract_accepted': False},
            'p1_payoff': c(46),
            'p2_payoff': c(34),
        },
    ]

    def play_round(self):
        case = self.case
        # intro
        yield (pages.Introduction)

        if self.player.id_in_group == 1:
            # P1/A - propose contract
            yield (
                pages.Offer, {'agent_fixed_pay': 10, 'agent_return_share': 0.6}
            )
        else:
            # P2/B - accept or reject contract
            yield (pages.Accept, case['p2_decision'])
        yield (pages.Results)

        if self.player.id_in_group == 1:
            assert self.player.payoff == case['p1_payoff']
        else:
            assert self.player.payoff == case['p2_payoff']
