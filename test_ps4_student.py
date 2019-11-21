import unittest
import random
import numpy as np
from ps4_classes import CardDecks, BlackJackCard, Busted # remove warnings
from ps4_classes import *
from blackjack import BlackJackHand, play_hand, run_simulation # remove warnings
from blackjack import *

class MockCardDecks(CardDecks):
    """
    Mock representation of CardDecks class used for testing.

    Allows tester to specify which cards to deal.
    """

    def __init__(self, num_decks, card_type, cards_to_deal):
        CardDecks.__init__(self, num_decks, card_type)
        self.cards_to_deal = cards_to_deal

    def deal_card(self):
        return self.cards_to_deal.pop()

    def num_cards_left(self):
        return len(self.cards_to_deal)


def is_within_epsilon(true_value, estimated_value, epsilon):
    return abs(true_value - estimated_value) <= epsilon


def check_within_epsilon(true_values, estimated_values, epsilon):
    """
    Returns True if and only if each value in true_values is within epsilon
    of the corresponding value in estimated_values.
    """
    for i in range(len(true_values)):
        if not is_within_epsilon(true_values[i], estimated_values[i], epsilon):
            return False
    return True


def get_printable_cards(cards):
    """
    Return list of string representations of each card in cards.
    """
    return [str(card) for card in cards]


best_value_error_message = "Your best_val returned %s for cards %s, but it should return %s."
dealer_error_message = "Your mimic_dealer_strategy returned %s when player has %s and dealer has %s, but it should return %s."
peek_error_message = "Your peek_strategy returned %s when player has %s and dealer has %s, but it should return %s."
simple_error_message = "Your simple_strategy returned %s when player has %s and dealer has %s, but it should return %s."
doubledown_error_message = "Your doubledown_strategy returned %s when player has %s and dealer has %s, but it should return %s."

class TestPS4(unittest.TestCase):
    #######################
    # BlackJackHand Tests #
    #######################

    def test_01_best_value_no_aces_1(self):
        # no cards
        cards = []
        self.assertEqual(BlackJackHand.best_value(cards), 0, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 0))

    def test_02_best_value_no_aces_2(self):
        # less than 21
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            '3', 'C'), BlackJackCard('K', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 15, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 15))

    def test_03_best_value_one_ace_1(self):
        # less than 21, A with value 11
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('7', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 20, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 20))

    def test_04_best_value_one_ace_2(self):
        # less than 21, A with value 1
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('K', 'S')]
        self.assertEqual(BlackJackHand.best_value(cards), 13, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 13))

    def test_05_best_value_multiple_aces_1(self):
        # one A with value 1, one A with value 11
        cards = [BlackJackCard('2', 'C'), BlackJackCard(
            'A', 'C'), BlackJackCard('A', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 14, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 14))

    def test_06_best_value_multiple_aces_2(self):
        # two A with value 1
        cards = [BlackJackCard('2', 'C'), BlackJackCard('A', 'C'), BlackJackCard(
            'A', 'S'), BlackJackCard('8', 'H'), BlackJackCard('K', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 22, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 22))
    
    def test_06_best_value_multiple_aces_3(self):
        cards = [BlackJackCard('A', 'C'), BlackJackCard('A', 'C'), BlackJackCard(
            '3', 'S'), BlackJackCard('7', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 12, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 12))
    
    def test_06_best_value_multiple_aces_4(self):
        cards = [BlackJackCard('A', 'C'), BlackJackCard('A', 'C'), BlackJackCard(
            '3', 'S'), BlackJackCard('A', 'H'), BlackJackCard('5', 'H')]
        self.assertEqual(BlackJackHand.best_value(cards), 21, best_value_error_message % (
            BlackJackHand.best_value(cards), get_printable_cards(cards), 21))

    def test_07_mimic_dealer_strategy_1(self):
        # less than 17, hit
        player_cards = [BlackJackCard('5', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('6', 'C'), BlackJackCard('3', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.mimic_dealer_strategy(), BlackJackHand.hit, dealer_error_message % (
            hand.mimic_dealer_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.hit))

    def test_08_mimic_dealer_strategy_2(self):
        # 17, stand
        player_cards = [BlackJackCard('7', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('6', 'C'), BlackJackCard('3', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.mimic_dealer_strategy(), BlackJackHand.stand, dealer_error_message % (
            hand.mimic_dealer_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_09_peek_strategy_1(self):
        # player < dealer, hit
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('K', 'C')]
        dealer_cards = [BlackJackCard('K', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.peek_strategy(), BlackJackHand.hit, peek_error_message % (
            hand.peek_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.hit))

    def test_10_peek_strategy_2(self):
        # player == dealer, stand
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('K', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.peek_strategy(), BlackJackHand.stand, peek_error_message % (
            hand.peek_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_11_peek_strategy_3(self):
        # player > dealer, stand
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.peek_strategy(), BlackJackHand.stand, peek_error_message % (
            hand.peek_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_12_simple_strategy_1(self):
        # player > 17
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.simple_strategy(), BlackJackHand.stand, simple_error_message % (
            hand.simple_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_13_simple_strategy_2(self):
        # player == 17
        player_cards = [BlackJackCard('7', 'C'), BlackJackCard('A', 'C')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.simple_strategy(), BlackJackHand.stand, simple_error_message % (
            hand.simple_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))

    def test_14_doubledown_strategy_1(self):
        # player < 11 (has 10)
        player_cards = [BlackJackCard('2', 'C'), BlackJackCard('8', 'D')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.doubledown_strategy(), BlackJackHand.hit, doubledown_error_message % (
            hand.doubledown_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.hit))
    
    def test_15_doubledown_strategy_2(self):
        # player > 11 (has 17)
        player_cards = [BlackJackCard('9', 'C'), BlackJackCard('8', 'D')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.doubledown_strategy(), BlackJackHand.stand, doubledown_error_message % (
            hand.doubledown_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.stand))
    
    def test_16_doubledown_strategy_3(self):
        # player == 11
        player_cards = [BlackJackCard('2', 'C'), BlackJackCard('9', 'H')]
        dealer_cards = [BlackJackCard('3', 'S'), BlackJackCard('J', 'C')]
        deck = CardDecks(2, BlackJackCard)
        hand = BlackJackHand(deck)
        hand.set_initial_cards(player_cards, dealer_cards)
        self.assertEqual(hand.doubledown_strategy(), BlackJackHand.doubledown, doubledown_error_message % (
            hand.doubledown_strategy(), get_printable_cards(player_cards), get_printable_cards(dealer_cards), BlackJackHand.doubledown))
        
        # make sure the bet doubles when doubling down
        cards_to_deal = [BlackJackCard('9', 'D'), BlackJackCard('9', 'S'), *dealer_cards, *player_cards]
        mockdeck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(mockdeck, initial_bet=2.0)
        hand.set_initial_cards(player_cards, dealer_cards)
        initial_bet = hand.get_bet()
        self.assertEqual(initial_bet, 2.0, "Inaccurate initial bet, found %s, expected %s" % (initial_bet, 2.0))
        def strategy(hand):
            if hand.deck.num_cards_left() == 2:
                return BlackJackHand.doubledown # trigger play_player_turn to double the bet
            else:
                return BlackJackHand.stand
        hand.play_player_turn(strategy)
        new_bet = hand.get_bet()
        self.assertEqual(new_bet, 4.0, "Your doubledown strategy did not double the current bet to %s, found %s" %
                         (4.0, new_bet))
           
    def test_17_play_player_turn_1(self):
        # player busts
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('K', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        def strategy(hand):
            if hand.deck.num_cards_left() > 0:
                return BlackJackHand.hit
            return BlackJackHand.stand

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        self.assertRaises(Busted, hand.play_player_turn, strategy)
        

    def test_18_play_player_turn_2(self):
        # player does not bust
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('3', 'S'), BlackJackCard(
            '3', 'S'), *dealer_hand, *player_hand]

        def strategy(hand):
            if hand.deck.num_cards_left() > 0:
                return BlackJackHand.hit
            return BlackJackHand.stand

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        try:
            hand.play_player_turn(strategy)
        except:
            self.fail('Your play_player_turn busted when it should not have.')

    def test_19_play_dealer_turn_1(self):
        # dealer busts
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('K', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        self.assertRaises(Busted, hand.play_dealer_turn)

    def test_20_play_dealer_turn_2(self):
        # dealer does not bust
        player_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        dealer_hand = [BlackJackCard('2', 'S'), BlackJackCard('2', 'S')]
        cards_to_deal = [BlackJackCard('3', 'S'), BlackJackCard(
            'K', 'S'), *dealer_hand, *player_hand]

        deck = MockCardDecks(4, BlackJackCard, cards_to_deal)
        hand = BlackJackHand(deck)
        try:
            hand.play_dealer_turn()
        except:
            self.fail('Your play_dealer_turn busted when it should not have.')

    ###################
    # play_hand Tests #
    ###################

    def test_21_play_hand_mimic_dealer_strategy_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.mimic_dealer_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with dealer strategy.')

    def test_22_play_hand_mimic_dealer_strategy_2(self):
        random.seed(5)
        correct_return = 2
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.mimic_dealer_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with dealer_dealer strategy.')

    def test_23_play_hand_peek_strategy_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.peek_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with peek strategy.')

    def test_24_play_hand_peek_strategy_2(self):
        random.seed(5)
        correct_return = 2.0
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.peek_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')

    def test_25_play_hand_simple_strategy_1(self):
        random.seed(3)
        correct_return = 0
        deck = CardDecks(1, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.simple_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')

    def test_26_play_hand_simple_strategy_2(self):
        random.seed(5)
        correct_return = 2.0
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.simple_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from play_hand is not correct with simple strategy.')
        
    def test_27_play_hand_doubledown_strategy_1(self):
        random.seed(6)
        correct_return = 1.0
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.doubledown_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from doubledown strategy actual (%f) differs from expected (%f) too much' %
                        (player_return, correct_return))
                
    def test_28_play_hand_doubledown_strategy_2(self):
        random.seed(7)
        correct_return = 0.0 #@TODO give a mock deck to see return be 4x initial bet
        deck = CardDecks(8, BlackJackCard)
        amount_bet, player_return = play_hand(deck, BlackJackHand.doubledown_strategy)
        self.assertTrue(is_within_epsilon(correct_return, player_return, 0.0001),
                        'Return from doubledown strategy actual (%f) differs from expected (%f) too much' %
                        (player_return, correct_return))

    ########################
    # run_simulation Tests #
    ########################
    
    # helper function to run a simulation and test the resulting (returns, mean, and std) against
    # the supplied expected values
    #
    # this function currently must use the random number generator seed of 0 to match with 
    # the hardcoded expected values in the tests.
    #
    def sim_run_check(self, correct_mean, correct_std, strategy, strategy_str, 
                                        bet, num_decks, num_hands, num_trials, show_plot):
        random.seed(0) # Must be zero for deterministically producing expected vals!
        returns, mean, std = run_simulation(strategy, bet, num_decks, num_hands, num_trials, show_plot)
        self.assertTrue(is_within_epsilon(np.mean(returns), correct_mean, 0.0001),
                        'Mean of %s simulation returns (%f) not within tolerance of correct val (%f)' % \
                        (strategy_str, np.mean(returns), correct_mean))
        self.assertTrue(is_within_epsilon(np.std(returns), correct_std, 0.0001),
                        'Std. dev. of %s simulation returns (%f) not within tolerance of correct val (%f)' % \
                        (strategy_str, np.std(returns), correct_std))
        self.assertTrue(
            is_within_epsilon(correct_mean, mean, 0.0001),
            'Mean of %s simulation (%s) not within tolerance of correct val (%s)' % \
            (strategy_str, mean, correct_mean))
        self.assertTrue(
            is_within_epsilon(correct_std, std, 0.0001),
            'Std. dev. of %s simulation (%s) not within tolerance of correct val (%s)' % \
            (strategy_str, std, correct_std))

    def test_29_run_simulation_mimic_dealer(self):
        correct_mean = -6.044375
        correct_std = 22.19167002186575
        self.sim_run_check(correct_mean, correct_std, BlackJackHand.mimic_dealer_strategy,
                           "mimic_dealer", 2, 8, 20, 4000, False)

    def test_30_run_simulation_peek(self):
        correct_mean = -0.1825
        correct_std = 21.89051892372586
        self.sim_run_check(correct_mean, correct_std, BlackJackHand.peek_strategy, 
                           "peek", 2, 8, 20, 4000, False)

    def test_31_run_simulation_simple(self):
        correct_mean = -3.3925
        correct_std = 21.8872895478
        self.sim_run_check(correct_mean, correct_std, BlackJackHand.simple_strategy,
                           "simple", 2, 8, 20, 4000, False)
        
    def test_32_run_simulation_doubledown(self):
        #correct_mean = 3.072500
        #correct_std = 24.547602
        correct_mean = -2.540875
        correct_std = 22.238588
        self.sim_run_check(correct_mean, correct_std, BlackJackHand.doubledown_strategy,
                           "doubledown", 2, 8, 20, 4000, False)


# Dictionary mapping function names from the above TestCase class to
# the point value each test is worth.
point_values = {
    'test_01_best_value_no_aces_1': 0.10,
    'test_02_best_value_no_aces_2': 0.10,
    'test_03_best_value_one_ace_1': 0.10,
    'test_04_best_value_one_ace_2': 0.10,
    'test_05_best_value_multiple_aces_1': 0.10,
    'test_06_best_value_multiple_aces_2': 0.10,
    'test_06_best_value_multiple_aces_3': 0.05,
    'test_06_best_value_multiple_aces_4': 0.05,
    'test_07_mimic_dealer_strategy_1': 0.21,
    'test_08_mimic_dealer_strategy_2': 0.21,
    'test_09_peek_strategy_1': 0.21,
    'test_10_peek_strategy_2': 0.21,
    'test_11_peek_strategy_3': 0.21,
    'test_12_simple_strategy_1':0.21,
    'test_13_simple_strategy_2':0.21,
    'test_14_doubledown_strategy_1':0.21,
    'test_15_doubledown_strategy_2':0.21,
    'test_16_doubledown_strategy_3':0.21,
    'test_17_play_player_turn_1': 0.40,
    'test_18_play_player_turn_2': 0.40,
    'test_19_play_dealer_turn_1': 0.40,
    'test_20_play_dealer_turn_2': 0.40,
    'test_21_play_hand_mimic_dealer_strategy_1': 0.30,
    'test_22_play_hand_mimic_dealer_strategy_2': 0.30,
    'test_23_play_hand_peek_strategy_1': 0.30,
    'test_24_play_hand_peek_strategy_2': 0.30,
    'test_25_play_hand_simple_strategy_1': 0.30,
    'test_26_play_hand_simple_strategy_2': 0.30,
    'test_27_play_hand_doubledown_strategy_1': 0.30,
    'test_28_play_hand_doubledown_strategy_2': 0.30,
    'test_29_run_simulation_mimic_dealer': 0.30,
    'test_30_run_simulation_peek': 0.30,
    'test_31_run_simulation_simple': 0.30,
    'test_32_run_simulation_doubledown': 0.30
}


# Subclass to track a point score and appropriate
# grade comment for a suit of unit tests
class Results_600(unittest.TextTestResult):

    # We override the init method so that the Result object
    # can store the score and appropriate test output.
    def __init__(self, *args, **kwargs):
        super(Results_600, self).__init__(*args, **kwargs)
        self.output = []
        self.points = 8

    def addFailure(self, test, err):
        test_name = test._testMethodName
        msg = str(err[1])
        self.handleDeduction(test_name, msg)
        super(Results_600, self).addFailure(test, err)

    def addError(self, test, err):
        test_name = test._testMethodName
        self.handleDeduction(test_name, None)
        super(Results_600, self).addError(test, err)

    def handleDeduction(self, test_name, message):
        point_value = point_values[test_name]
        if message is None:
            message = 'Your code produced an error on test %s.' % test_name
        self.output.append('[-%s]: %s' % (point_value, message))
        self.points -= point_value

    def getOutput(self):
        if len(self.output) == 0:
            return "All correct!"
        return '\n'.join(self.output)

    def getPoints(self):
        return self.points


if __name__ == '__main__':

    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS4))
    result = unittest.TextTestRunner(
        verbosity=2, resultclass=Results_600).run(suite)

    output = result.getOutput()
    points = result.getPoints()

    # weird bug with rounding
    if points < .1:
        points = 0

    print("\nProblem Set 4 Unit Test Results:")
    print(output)
    print("Points: %s/8\n" % points)
