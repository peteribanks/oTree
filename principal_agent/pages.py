from ._builtin import Page, WaitPage
from .models import Constants, cost_from_effort


class Introduction(Page):
    pass


class Offer(Page):
    def is_displayed(self):
        return self.player.role() == 'principal'

    form_model = 'group'
    form_fields = ['agent_fixed_pay', 'agent_return_share']


class OfferWaitPage(WaitPage):
    def vars_for_template(self):
        if self.player.role() == 'agent':
            body_text = "You are Participant B. Waiting for Participant A to propose a contract."
        else:
            body_text = "Waiting for Participant B."
        return {'body_text': body_text}


class Accept(Page):
    def is_displayed(self):
        return self.player.role() == 'agent'

    form_model = 'group'
    form_fields = ['contract_accepted', 'agent_work_effort']

    #timeout_seconds = 3 * 60
    timeout_submission = {
        'contract_accepted': False,
        'agent_work_effort': 1,
    }

    def error_message(self, values):
        if values['contract_accepted'] and values['agent_work_effort'] == None:
            return 'If you accept the contract, you must select a work effort.'


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    def vars_for_template(self):
        if self.group.contract_accepted:
            effort = self.group.agent_work_effort
            effort_cost = cost_from_effort(self.group.agent_work_effort)
        else:
            effort = effort_cost = 'N/A'
        return {
            'received': self.player.payoff - Constants.base_pay,
            'effort': effort,
            'effort_cost': effort_cost,
        }


page_sequence = [Introduction,
                 Offer,
                 OfferWaitPage,
                 Accept,
                 ResultsWaitPage,
                 Results]
