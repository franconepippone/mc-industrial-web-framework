from typing import Optional
from abc import ABC, abstractmethod

from spec_schemas import BaseDeviceSpec, SpecDeviceClass, RDSRouterSpec, RDSPackageSpec

class BaseSpecFilter(ABC):
    device_class: SpecDeviceClass
    versions: 

    def matches(self, spec: BaseDeviceSpec) -> bool:
        pass

class RDSRouterFilter(BaseSpecFilter):
    device_class = SpecDeviceClass.RDS_ROUTER
    min_throughput: Optional[int] = None
    max_throughput: Optional[int] = None
    survival_friendliness: Optional[str] = None

    def matches(self, spec: RDSRouterSpec) -> bool:
        if spec.device_class != self.device_class:
            return False

        if self.min_throughput is not None and spec.throughput < self.min_throughput:
            return False
        if self.max_throughput is not None and spec.throughput > self.max_throughput:
            return False
        if self.survival_friendliness and spec.survival_friendliness != self.survival_friendliness:
            return False

        return True