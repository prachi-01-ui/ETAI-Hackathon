import json
from pathlib import Path


class SimulationEngine:

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent

        self.scenarios_file = (
            self.project_root
            / "data"
            / "risk_scenarios.json"
        )

        self.routes_file = (
            self.project_root
            / "data"
            / "alternative_routes.json"
        )

        self.scenarios = []
        self.alternative_routes = []

        self.load_data()

    def load_data(self):

        with open(
            self.scenarios_file,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

            self.scenarios = data.get(
                "scenarios",
                [],
            )

        with open(
            self.routes_file,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

            self.alternative_routes = data.get(
                "alternative_routes",
                [],
            )

    def get_scenario(self, scenario_id: int):

        for scenario in self.scenarios:

            if scenario["id"] == scenario_id:
                return scenario

        return None

    def calculate_disruption_impact(
        self,
        scenario_id: int,
    ):

        scenario = self.get_scenario(
            scenario_id
        )

        if not scenario:
            return None

        probability = scenario["probability"]

        financial_impact = (
            scenario["estimated_financial_impact"]
        )

        supply_loss = (
            scenario[
                "estimated_supply_loss_percentage"
            ]
        )

        risk_exposure = round(
            probability * financial_impact,
            2,
        )

        expected_supply_loss = round(
            probability * supply_loss,
            2,
        )

        return {
            "scenario_id": scenario["id"],
            "scenario_name": scenario[
                "scenario_name"
            ],
            "severity": scenario["severity"],
            "probability": probability,
            "estimated_delay_days": scenario[
                "estimated_delay_days"
            ],
            "estimated_financial_impact":
                financial_impact,
            "risk_exposure": risk_exposure,
            "expected_supply_loss_percentage":
                expected_supply_loss,
            "recommended_strategy": scenario[
                "recommended_strategy"
            ],
        }

    def compare_alternative_routes(self):

        available_routes = [
            route
            for route in self.alternative_routes
            if route["availability"]
            in ["Available", "Emergency Only"]
        ]

        ranked_routes = sorted(
            available_routes,
            key=lambda route: (
                route["risk_level"] != "Low",
                route["transit_days"],
                route["estimated_cost"],
            ),
        )

        return ranked_routes

    def run_simulation(
        self,
        scenario_id: int,
    ):

        impact = self.calculate_disruption_impact(
            scenario_id
        )

        if not impact:
            return None

        alternatives = (
            self.compare_alternative_routes()
        )

        best_route = (
            alternatives[0]
            if alternatives
            else None
        )

        return {
            "simulation_status": "Completed",
            "scenario": impact,
            "recommended_alternative":
                best_route,
            "alternatives_evaluated":
                len(alternatives),
        }


simulation_engine = SimulationEngine()