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

page_sequence = [Bid,
                 ResultsWaitPage,
                 Results]
