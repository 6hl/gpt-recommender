import json
import logging
import os
from typing import Any, Optional


class Cache:

    def __init__(self, dir: Optional[str] = None):
        if dir is None:
            dir = os.path.join(os.getcwd(), ".consultant_cache")

        self.objs_path = os.path.join(dir, "cache")

        if not os.path.exists(dir) or not os.path.exists(self.objs_path):
            os.makedirs(dir, exist_ok=True)
            os.makedirs(self.objs_path, exist_ok=True)

        self.map_path = os.path.join(dir, "mapping.json")

        self._cache_map = self._load_cache_map()

    def __call__(
        self, key: str, value: Optional[Any] = None, bypass: bool = False
    ) -> Any | None:
        if bypass:
            return None

        if value is not None:
            return self._update_cache(key, value)

        if key in self._cache_map.keys():
            return self._load_cached_obj(key)

        return None

    def _update_cache(self, k: str, v: Any) -> None:
        obj_path = os.path.join(self.objs_path, f"{k}.cache")
        self._cache_map[k] = obj_path
        self._save_cache_map()
        self._save_cached_obj(obj_path, v)

    def _load_cached_obj(self, key: str) -> Any:
        value_path = self._cache_map[key]
        try:
            value = self._load_json(value_path)
            return value
        except Exception as e:
            logging.debug(f"Failed to load cached obj with error: {e}")
            return None

    def _save_cached_obj(self, obj_path: str, value: Any) -> bool:
        try:
            self._save_json(obj_path, value)
            return True
        except Exception as e:
            logging.debug(f"Failed to save cache obj with error: {e}")
            return False

    def _load_cache_map(self) -> dict:
        try:
            map = self._load_json(self.map_path)
            if map is None:
                return {}
            return map
        except Exception as e:
            logging.debug(
                f"Failed to load cache map with exception: {e}. Creating blank map."
            )
            self._save_json(self.map_path, {})
        return {}

    def _save_cache_map(self) -> bool:
        try:
            self._save_json(self.map_path, self._cache_map)
            return True
        except Exception as e:
            logging.debug(f"Failed to save cache map with error: {e}")
            return False

    def _load_json(self, path: str):
        try:
            with open(path, "r") as f:
                data = json.load(f)
            return data
        except Exception as e:
            logging.debug(f"Failed to load file {path} with error: {e}")
            return None

    def _save_json(self, path: str, data: dict) -> bool:
        try:
            with open(path, "w") as f:
                f.write(json.dumps(data))
            return True
        except Exception as e:
            logging.debug(f"Failed to save file {path} with error: {e}")
            return False
