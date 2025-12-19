class AIInferenceUnit:
    """
    Виртуална единица, оптимизирана за машинно обучение.
    Управлява GPU паметта и зареждането на тегла на модели (Model Weights).
    """
    def __init__(self, model_id: str):
        self.model_id = model_id
        self._gpu_allocated = False
        self._precision = "float16"

    def load_model(self):
        self._gpu_allocated = True
        print(f"[AI-UNIT] Model {self.model_id} loaded into VRAM with {self._precision} precision.")

    def run_inference(self, input_data: str):
        """Симулира невронна обработка."""
        if not self._gpu_allocated: return "Error: Model not loaded"
        print(f"[AI-UNIT] Processing inference for input: {input_data[:20]}...")
        return f"AI_Result_for_{self.model_id}"