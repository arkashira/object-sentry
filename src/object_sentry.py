import json
from dataclasses import dataclass
from typing import List

@dataclass
class ObjectDetectionModel:
    name: str
    config: dict

class ObjectSentry:
    def __init__(self):
        self.models = [
            ObjectDetectionModel("Model1", {"param1": 1, "param2": 2}),
            ObjectDetectionModel("Model2", {"param3": 3, "param4": 4}),
        ]

    def get_available_models(self):
        return [model.name for model in self.models]

    def select_model(self, model_name):
        for model in self.models:
            if model.name == model_name:
                return model
        raise ValueError("Model not found")

    def configure_model(self, model_name, config):
        model = self.select_model(model_name)
        if not isinstance(config, dict):
            raise ValueError("Invalid config")
        model.config = config
        return model

    def validate_model_config(self, model_name, config):
        if not isinstance(config, dict):
            raise ValueError("Invalid config")
        # Add more validation logic here
        return True
