from game import Game, Item, Question, SpaceType, load_questions


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
    assert game.players[0].credits == 400
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
    assert game.players[0].credits == 200


def test_payment_passage_is_reported_even_when_landing_on_another_space() -> None:
    game = make_game()
    game.players[0].position = 14

    result = game.take_turn(2)

    assert game.players[0].position == 16
    assert result.payment_message is not None
    assert "100 Credits" in result.payment_message


def test_payment_returns_to_previous_checkpoint_when_unaffordable() -> None:
    game = make_game()
    game.players[0].position = 14
    game.players[0].credits = 50

    game.take_turn(1)

    assert game.players[0].position == 0
    assert game.players[0].credits == 50


def test_quiz_waits_for_answer_then_rewards_correct_answer() -> None:
    game = make_game()
    game.players[0].position = 7

    result = game.take_turn(1)

    assert result.question is not None
    assert game.current_player_index == 0
    game.answer_question(0)
    assert game.players[0].credits == 400
    assert game.current_player_index == 1


def test_waf_blocks_ddos_and_is_consumed() -> None:
    game = make_game()
    game.players[0].items.append(Item.WAF)

    game.apply_ddos(0)

    assert game.players[0].credits == 300
    assert Item.WAF not in game.players[0].items


def test_auto_scaling_adds_two_to_next_roll() -> None:
    game = make_game()
    game.players[0].items.append(Item.AUTO_SCALING)

    game.use_item(0, Item.AUTO_SCALING)
    game.take_turn(4)

    assert game.players[0].position == 6
    assert Item.AUTO_SCALING not in game.players[0].items


def test_cost_explorer_can_be_used_for_immediate_credits() -> None:
    game = make_game()
    game.players[0].items.append(Item.COST_EXPLORER)

    message = game.use_item(0, Item.COST_EXPLORER)

    assert game.players[0].credits == 360
    assert Item.COST_EXPLORER not in game.players[0].items
    assert "Cost Explorer" in message


def test_item_spaces_are_available_more_often() -> None:
    game = make_game()

    assert game.space_at(2) is SpaceType.ITEM
    assert game.space_at(56) is SpaceType.ITEM


def test_event_messages_are_selected_from_a_random_pool() -> None:
    game = make_game()
    game.message_pools["gain"] = ["message A", "message B"]

    messages = {game._random_message("gain") for _ in range(12)}

    assert messages == {"message A", "message B"}


def test_player_wins_only_after_final_payment() -> None:
    game = make_game()
    game.players[0].position = 58
    game.players[0].final_payment_paid = True

    game.take_turn(1)

    assert game.winner_index == 0


def test_normal_questions_do_not_repeat_before_the_deck_is_exhausted() -> None:
    questions = [
        Question(f"Question {index}", ("A", "B", "C", "D"), 0, "Explanation")
        for index in range(3)
    ]
    game = Game(questions=questions, rng_seed=7)

    asked = [game._next_question(False).prompt for _ in range(3)]

    assert len(set(asked)) == 3


def test_load_questions_reads_the_project_question_banks() -> None:
    questions = load_questions(["assets/quiz.md", "assets/quiz-architecture.md"])

    assert len(questions) >= 50
    assert all(len(question.choices) == 4 for question in questions)
