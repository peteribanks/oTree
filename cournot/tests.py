# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from ._builtin import Bot
from .models import Constants
from . import views


class PlayerBot(Bot):

    cases = ['min', 'max']

    def play_round(self):
        yield (views.Introduction)

        if self.case == 'min':
            yield (views.Decide, {'units': 0})
            # if player produces 0, nothing is sold and they make 0
            assert self.player.payoff == c(0)

        if self.case == 'max':
            yield (views.Decide, {'units': Constants.max_units_per_player})
            # if everyone produces max, price is driven to 0
            assert self.player.payoff == c(0)

        yield (views.Results)
