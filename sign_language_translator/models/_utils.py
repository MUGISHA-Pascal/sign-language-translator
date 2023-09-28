"""Extra Utility functions models placed here to avoid circular imports.

This module contains various utility functions and classes to assist with models.

Functions:
    get_model(model_code: str, sign_language=None, text_language=None, video_feature_model=None):
        Get the model based on the provided model code and optional parameters.
"""

from __future__ import annotations

__all__ = [
    "get_model",
]

from os.path import join
from typing import TYPE_CHECKING

from sign_language_translator.config.enums import (
    ModelCodeGroups,
    ModelCodes,
    normalize_short_code,
)
from sign_language_translator.config.settings import Settings
from sign_language_translator.utils import download_resource

if TYPE_CHECKING:
    from enum import Enum


def get_model(model_code: str | Enum, *args, **kwargs):
    """
    Get the model based on the provided model code and optional parameters.
    See sign_language_translator.config.enums.ModelCodes
    (or slt.ModelCodes) for a list of supported model codes.

    Args:
        model_code (str): The code representing the desired model.

    Returns:
        Any: The instantiated model object if successful, or None if no model found.

    Raises:
        ValueError: If inappropriate argument values are provided for text_language, sign_language, or video_feature_model.
    """

    model_code = normalize_short_code(model_code)
    if model_code == ModelCodes.CONCATENATIVE_SYNTHESIS.value:
        from sign_language_translator.models import ConcatenativeSynthesis

        # TODO: validate arg types
        return ConcatenativeSynthesis(*args, **kwargs)

    elif model_code in ModelCodeGroups.ALL_NGRAM_LANGUAGE_MODELS.value:
        from sign_language_translator.models import NgramLanguageModel

        download_resource(
            f"models/{model_code}", progress_bar=True, leave=False, chunk_size=1048576
        )
        return NgramLanguageModel.load(
            join(Settings.RESOURCES_ROOT_DIRECTORY, "models", model_code)
        )
    elif model_code in ModelCodeGroups.ALL_MIXER_LANGUAGE_MODELS.value:
        from sign_language_translator.models import MixerLM

        download_resource(
            f"models/{model_code}", progress_bar=True, leave=False, chunk_size=1048576
        )
        return MixerLM.load(
            join(Settings.RESOURCES_ROOT_DIRECTORY, "models", model_code)
        )
    elif model_code in ModelCodeGroups.ALL_TRANSFORMER_LANGUAGE_MODELS.value:
        from sign_language_translator.models import TransformerLanguageModel

        download_resource(
            f"models/{model_code}", progress_bar=True, leave=False, chunk_size=1048576
        )
        return TransformerLanguageModel.load(
            join(Settings.RESOURCES_ROOT_DIRECTORY, "models", model_code)
        )
    elif model_code in ModelCodeGroups.ALL_MEDIAPIPE_EMBEDDING_MODELS.value:
        from sign_language_translator.models import MediaPipeLandmarksModel

        parts = model_code.split("-")

        pose_version = int(parts[parts.index("pose") + 1])
        # hand_version = int(parts[parts.index("hand") + 1])
        names = ["lite", "full", "heavy"]

        return MediaPipeLandmarksModel(
            pose_model_name=f"pose_landmarker_{names[pose_version]}.task",
            # hand_model_name=f"hand_landmarker_{names[hand_version]}.task",
            # number_of_persons=1,
        )

    return None