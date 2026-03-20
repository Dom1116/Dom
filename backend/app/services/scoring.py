from dataclasses import dataclass


@dataclass
class ScoreWeights:
    net_profit: float = 0.30
    roi: float = 0.20
    match_confidence: float = 0.15
    stock_availability: float = 0.10
    demand_velocity: float = 0.10
    competition_risk: float = 0.10
    category_risk: float = 0.05


@dataclass
class ScoreInput:
    net_profit_score: float
    roi_score: float
    match_confidence_score: float
    stock_score: float
    demand_score: float
    competition_score: float
    category_score: float


class ResaleScoringEngine:
    """Calculates final opportunity score (0-100) from weighted components."""

    def __init__(self, weights: ScoreWeights | None = None) -> None:
        self.weights = weights or ScoreWeights()

    def score(self, data: ScoreInput) -> float:
        weighted = (
            data.net_profit_score * self.weights.net_profit
            + data.roi_score * self.weights.roi
            + data.match_confidence_score * self.weights.match_confidence
            + data.stock_score * self.weights.stock_availability
            + data.demand_score * self.weights.demand_velocity
            + data.competition_score * self.weights.competition_risk
            + data.category_score * self.weights.category_risk
        )
        return round(max(0.0, min(100.0, weighted)), 2)
