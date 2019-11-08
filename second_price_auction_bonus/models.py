from otree.api import (
    models, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c
)


class Constants(BaseConstants):
    name_in_url = 'second_price_auction_bonus'
    players_per_group = 3
    num_rounds = 2

    min_allowable_bid = c(0)
    max_allowable_bid = c(10)


class Subsession(BaseSubsession):

    def creating_session(self):
        import random
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
        for p in self.get_players():
            item_value = random.uniform(
                Constants.min_allowable_bid,
                Constants.max_allowable_bid
            )
            p.item_value = round(item_value, 1)


class Group(BaseGroup):

    highest_bid = models.CurrencyField(initial = -1)
    second_highest_bid = models.CurrencyField(initial = -1)

    def set_winner(self):

        # Determine highest and second highest bids.
        players = self.get_players()
        for p in players:
            if p.bid_amount >= self.highest_bid:
                self.second_highest_bid = self.highest_bid
                self.highest_bid = p.bid_amount
            elif p.bid_amount > self.second_highest_bid:
                self.second_highest_bid = p.bid_amount

        # Determine winner.
        players_with_highest_bid = [p for p in players if p.bid_amount == self.highest_bid]
        import random
        winner = random.choice(
            players_with_highest_bid)  # if tie, winner is chosen at random
        winner.is_winner = True
        for p in players:
            p.set_payoff()



class Player(BasePlayer):
    item_value = models.CurrencyField(
        doc="""Individual value of the item to be auctioned"""
    )

    bid_amount = models.CurrencyField(
        min=Constants.min_allowable_bid,
        doc="""Amount bid by the player"""
    )

    def bid_amount_max(self):
        return self.item_value

    is_winner = models.BooleanField(
        initial=False,
        doc="""Indicates whether the player is the winner"""
    )

    round_payoff = models.CurrencyField(
        initial=0,
        doc="""Amount earned by the player in this round"""
    )

    def set_payoff(self):
        if self.is_winner:
            self.round_payoff = self.item_value - self.group.second_highest_bid
        else:
            self.round_payoff = 0

        if self.subsession.round_number == self.session.vars['paying_round']:
            self.payoff = self.round_payoff
