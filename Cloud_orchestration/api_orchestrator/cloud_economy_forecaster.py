class CloudEconomyForecaster:
    """
    Прогнозира бъдещи финансови разходи въз основа на тенденциите в потреблението.
    """
    def forecast_next_month(self, usage_history: list) -> float:
        # Симулация на линейна регресия
        growth_rate = 1.15
        current_spend = usage_history[-1]
        forecast = current_spend * growth_rate
        print(f"[FORECASTER] Estimated spend for next month: ${forecast:.2f}")
        return forecast