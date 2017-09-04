from . import models
from ._builtin import Page, WaitPage
import datetime


class Instructions(Page):
    def is_displayed(self):
        return self.round_number == 1


class Catch(Page):
    form_model = models.Player
    form_fields = ['num_fish_caught_this_year']

    def is_displayed(self):
        return self.session.vars['continue_game']

    def vars_for_template(self):
        current_year = self.round_number
        display_year = current_year - 1 + datetime.date.today().year

        # magic code!
        #if current_year > 1:
        #    self.subsession.num_fish_at_start = self.subsession.in_round(current_year - 1) \
        #            .num_fish_at_start

        #Is it correct?
        if current_year > 1:
            self.subsession.num_fish_at_start_of_year = self.subsession.in_round(current_year - 1) \
                    .num_fish_at_start_of_year

        return {
            'year_number': display_year,
            #'year_number': self.round_number + self.subsession.this_year,
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
        }


class ResultsWaitPage(WaitPage):
    def is_displayed(self):
        return self.session.vars['continue_game']

    def after_all_players_arrive(self):
        self.session.vars['continue_game'] = self.group.set_payoffs()


class Results(Page):
    def is_displayed(self):
        return self.session.vars['continue_game']

    def vars_for_template(self):
        return {
            'num_total_fish_caught': self.participant.payoff,
            'num_fish_left_in_fishery': self.subsession.num_fish_at_start_of_year,
        }

page_sequence = [Instructions,
                 Catch,
                 ResultsWaitPage,
                 Results]
