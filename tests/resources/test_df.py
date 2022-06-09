# Copyright 2018-2022 Xanadu Quantum Technologies Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Unit tests for functions needed for resource estimation with the double factorization method.
"""
import pytest

import pennylane as qml
from pennylane import numpy as np


@pytest.mark.parametrize(
    ("norm", "error", "cost_ref"),
    [
        (72.49779513025341, 0.001, 113880),
    ],
)
def test_estimation_cost(norm, error, cost_ref):
    r"""Test that estimation_cost returns the correct values."""
    cost = qml.resources.estimation_cost(norm, error)

    assert cost == cost_ref


@pytest.mark.parametrize(
    ("constants", "cost_ref", "k_ref"),
    [  # The reference costs and k values are obtained manually, by computing the cost for a range
        # of k values and selecting the k that gives the minimum cost.
        (
            (26, 1, 0, 15.0, -1),
            27,
            1,
        ),
        (
            (26, 1, 0, 1, 0),
            11,
            4,
        ),
        (
            (151.0, 7.0, 151.0, 280, 0),
            589,
            1,
        ),
        (
            (151.0, 7.0, 151.0, 2, 0),
            52,
            16,
        ),
        (
            (151.0, 7.0, 151.0, 30.0, -1),
            168,
            4,
        ),
    ],
)
def test_cost_qrom(constants, cost_ref, k_ref):
    r"""Test that cost_qrom returns the correct values."""
    cost, k = qml.resources.cost_qrom(constants)

    assert cost == cost_ref
    assert k == k_ref