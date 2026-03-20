from app.services.scoring import ResaleScoringEngine, ScoreInput


def test_opportunity_score_is_bounded() -> None:
    engine = ResaleScoringEngine()
    score = engine.score(
        ScoreInput(
            net_profit_score=100,
            roi_score=90,
            match_confidence_score=85,
            stock_score=70,
            demand_score=65,
            competition_score=80,
            category_score=75,
        )
    )
    assert 0 <= score <= 100
