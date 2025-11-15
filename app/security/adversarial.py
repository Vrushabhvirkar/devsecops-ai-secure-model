from typing import Tuple
import numpy as np


def basic_input_screen(
    x: np.ndarray,
    value_range: Tuple[float, float] = (0.0, 1.0),
    max_linf_eps: float = 0.4,
):
    """
    Very basic guardrail:
    - Ensures numeric inputs are within expected range
    - Flags inputs with extreme L-infinity norm wrt center (0.5)

    Returns (is_suspicious, reason)
    """
    if not np.isfinite(x).all():
        return True, "Non-finite values detected"

    low, high = value_range
    if (x < low).any() or (x > high).any():
        return True, "Out-of-range values"

    linf = float(np.max(np.abs(x - 0.5)))
    if linf > max_linf_eps:
        return True, f"High L∞ deviation ({linf:.3f})"

    return False, "ok"

