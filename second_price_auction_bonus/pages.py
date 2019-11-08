from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_winner()


class Results(Page):
    pass

class ResultsSummary(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        player_in_all_rounds = self.player.in_all_rounds()

        return dict(
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            paying_round=self.session.vars['paying_round'],
            player_in_all_rounds=player_in_all_rounds,
        )



page_sequence = [Bid,
                 ResultsWaitPage,
                 Results,
                 ResultsSummary]
