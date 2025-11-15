import os
import joblib

MODEL_PATH_ENV = "MODEL_PATH"


class ModelNotAvailable(Exception):
    pass


def load_model():
    # Expect a joblib-serialized model by default
    path = os.getenv(MODEL_PATH_ENV, "model/model.joblib")
    if not os.path.exists(path):
        raise ModelNotAvailable(
            f"Model file not found at {path}. Set {MODEL_PATH_ENV}."
        )
    return joblib.load(path)


def predict(model, inputs):
    # Expect 2D array-like inputs
    return model.predict(inputs).tolist()

