import pennylane as qml
from pennylane.devices import DefaultQubit
from pennylane.operation import Observable, AnyWires


class TestObservableWithObjectReturnType:
    """Unit tests for differentiation of observables returning an object"""

    def test_custom_return_type(self):
        """Test differentiation of a QNode on a device supporting a
        special observable that returns an object rathern than a nummber."""

        class SpecialObject:
            """SpecialObject
            A special object that conveniently encapsulates the return value of
            a special observable supported by a special device and which supports
            multiplication with scalars and addition.
            """

            def __init__(self, val):
                self.val = val

            def __mul__(self, other):
                new = SpecialObject(self.val)
                new *= other
                return new

            def __imul__(self, other):
                self.val *= other
                return self

            def __rmul__(self, other):
                return self * other

            def __iadd__(self, other):
                self.val += other.val if isinstance(other, self.__class__) else other
                return self

            def __add__(self, other):
                new = SpecialObject(self.val)
                new += other.val if isinstance(other, self.__class__) else other
                return new

            def __radd__(self, other):
                return self + other

        class SpecialObservable(Observable):
            """SpecialObservable"""

            num_wires = AnyWires
            num_params = 0
            par_domain = None

            def diagonalizing_gates(self):
                """Diagonalizing gates"""
                return []

        class DeviceSupporingSpecialObservable(DefaultQubit):
            name = "Device supporing SpecialObservable"
            short_name = "default.qibit.specialobservable"
            observables = DefaultQubit.observables.union({"SpecialObservable"})

            def expval(self, observable, **kwargs):
                if self.analytic and isinstance(observable, SpecialObservable):
                    val = super().expval(qml.PauliZ(wires=0), **kwargs)
                    return SpecialObject(val)

                return super().expval(observable, **kwargs)

        dev = DeviceSupporingSpecialObservable(wires=1, shots=None)

        # force diff_method='parameter-shift' because otherwise
        # PennyLane swaps out dev for default.qubit.autograd
        @qml.qnode(dev, diff_method="parameter-shift")
        def qnode(x):
            qml.RY(x, wires=0)
            return qml.expval(SpecialObservable(wires=0))

        @qml.qnode(dev, diff_method="parameter-shift")
        def reference_qnode(x):
            qml.RY(x, wires=0)
            return qml.expval(qml.PauliZ(wires=0))

        assert isinstance(qnode(0.2), SpecialObject)
