from simulation.simulation_engine import simulation_engine


def test_scenario_exists():
    scenario = simulation_engine.get_scenario(1)

    assert scenario is not None
    assert scenario["id"] == 1
    assert scenario["scenario_name"] == "Strait of Hormuz Closure"


def test_disruption_impact():
    impact = simulation_engine.calculate_disruption_impact(1)

    assert impact is not None
    assert impact["severity"] == "Critical"
    assert impact["risk_exposure"] == 4250000
    assert impact["expected_supply_loss_percentage"] == 38.25


def test_alternative_routes():
    routes = simulation_engine.compare_alternative_routes()

    assert len(routes) == 3
    assert routes[0]["route_name"] == "Strategic Reserve Supply Route"


def test_run_simulation():
    result = simulation_engine.run_simulation(1)

    assert result is not None
    assert result["simulation_status"] == "Completed"
    assert result["scenario"]["scenario_id"] == 1
    assert result["alternatives_evaluated"] == 3
    assert result["recommended_alternative"] is not None


def test_invalid_scenario():
    result = simulation_engine.run_simulation(999)

    assert result is None