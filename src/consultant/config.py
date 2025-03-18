from typing import Optional

import yaml

from .base_types import Config, ModelArgs, PerformanceArgs, RecommenderArgs


def load_config(yaml_path: Optional[str] = None) -> Config:

    if yaml_path is not None:
        with open(yaml_path, "r") as file:
            config_data = yaml.safe_load(file)
    else:
        config_data = {}

    return Config(
        model=ModelArgs(**config_data.get("model", {})),
        recommender=RecommenderArgs(**config_data.get("recommender", {})),
        performance=PerformanceArgs(**config_data.get("performance", {})),
    )
