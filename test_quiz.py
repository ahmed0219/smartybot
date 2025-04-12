def test_generate_quiz():
    from quiz_generator import generate_quiz
    quiz = generate_quiz(num_questions=3)

    assert isinstance(quiz, list)
    assert len(quiz) == 3

    for q in quiz:
        assert "question" in q
        assert "type" in q
        assert "answer" in q
        assert isinstance(q["question"], str)
        assert q["type"] in ["mcq", "true_false", "short"]

        if q["type"] == "mcq":
            assert "options" in q
            assert isinstance(q["options"], list)
            assert len(q["options"]) >= 2
