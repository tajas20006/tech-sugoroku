from game import Game, Item, Question, SpaceType


def make_game() -> Game:
    return Game(
        questions=[
            Question(
                prompt="S3 is an object storage service.",
                choices=("True", "False", "Maybe", "Unknown"),
                answer_index=0,
                explanation="Amazon S3 stores objects.",
            )
        ],
        rng_seed=7,
    )


def test_gain_space_moves_current_player_and_ends_turn() -> None:
    game = make_game()

    result = game.take_turn(3)

    assert result.space_type is SpaceType.GAIN
    assert game.players[0].position == 3
    assert game.players[0].credits == 280
    assert game.current_player_index == 1


def test_loss_never_reduces_credits_below_zero() -> None:
    game = make_game()
    game.players[0].credits = 20

    game.take_turn(6)

    assert game.players[0].credits == 0


def test_payment_deducts_required_credits_when_affordable() -> None:
    game = make_game()
    game.players[0].position = 14

    game.take_turn(1)

    assert game.players[0].position == 15
    assert game.players[0].credits == 50


def test_payment_returns_to_previous_checkpoint_when_unaffordable() -> None:
    game = make_game()
    game.players[0].position = 14
    game.players[0].credits = 100

    game.take_turn(1)

    assert game.players[0].position == 0
    assert game.players[0].credits == 100


def test_quiz_waits_for_answer_then_rewards_correct_answer() -> None:
    game = make_game()
    game.players[0].position = 7

    result = game.take_turn(1)

    assert result.question is not None
    assert game.current_player_index == 0
    game.answer_question(0)
    assert game.players[0].credits == 280
    assert game.current_player_index == 1


def test_waf_blocks_ddos_and_is_consumed() -> None:
    game = make_game()
    game.players[0].items.append(Item.WAF)

    game.apply_ddos(0)

    assert game.players[0].credits == 200
    assert Item.WAF not in game.players[0].items


def test_auto_scaling_adds_two_to_next_roll() -> None:
    game = make_game()
    game.players[0].items.append(Item.AUTO_SCALING)

    game.take_turn(4)

    assert game.players[0].position == 6
    assert Item.AUTO_SCALING not in game.players[0].items


def test_player_wins_only_after_final_payment() -> None:
    game = make_game()
    game.players[0].position = 58
    game.players[0].final_payment_paid = True

    game.take_turn(1)

    assert game.winner_index == 0
