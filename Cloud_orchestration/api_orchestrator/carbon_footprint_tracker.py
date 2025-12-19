class CarbonFootprintTracker:
    """
    Следи екологичното влияние на облачните ресурси.
    Помага на компаниите да постигнат Net Zero цели.
    """
    def calculate_emissions(self, power_kwh: float, pue_factor: float):
        # PUE (Power Usage Effectiveness) е стандарт в индустрията
        co2_emissions = power_kwh * pue_factor * 0.4 # kg CO2
        print(f"[GREEN-OPS] This workload produced {co2_emissions:.2f} kg of CO2.")
        return co2_emissions