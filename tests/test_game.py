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


def test_cost_explorer_reduces_the_next_payment() -> None:
    game = make_game()
    game.players[0].items.append(Item.COST_EXPLORER)
    game.players[0].position = 14

    message = game.use_item(0, Item.COST_EXPLORER)
    game.take_turn(1)

    assert game.players[0].credits == 250
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


def test_reserved_instance_halves_the_next_cost_space_loss() -> None:
    game = make_game()
    game.players[0].items.append(Item.RESERVED_INSTANCE)

    game.use_item(0, Item.RESERVED_INSTANCE)
    game.take_turn(6)

    assert game.players[0].credits == 280


def test_ddos_attack_targets_the_other_player_and_waf_blocks_it() -> None:
    game = make_game()
    game.players[0].items.append(Item.DDOS_ATTACK)
    game.players[1].items.append(Item.WAF)

    game.use_item(0, Item.DDOS_ATTACK)

    assert game.players[1].credits == 300
    assert Item.WAF not in game.players[1].items


def test_lambda_keeps_the_current_player_for_an_extra_turn() -> None:
    game = make_game()
    game.players[0].items.append(Item.LAMBDA)

    game.use_item(0, Item.LAMBDA)
    game.take_turn(1)

    assert game.current_player_index == 0


def test_region_rumor_is_blocked_by_multi_az() -> None:
    game = make_game()
    game.players[0].items.append(Item.REGION_RUMOR)
    game.players[1].items.append(Item.MULTI_AZ)

    game.use_item(0, Item.REGION_RUMOR)

    assert game.players[1].skip_turns == 0
    assert Item.MULTI_AZ not in game.players[1].items


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
