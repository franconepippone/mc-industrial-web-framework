from pydantic import BaseModel, Field, field_validator
from typing import Literal, Dict, Union

# Minecraft version spec
class MinecraftSpec(BaseModel):
    edition: Literal["Java", "Bedrock", "Any"]
    lower: str
    upper: str

    @field_validator("lower", "upper")
    def validate_version_format(cls, v: str):
        parts = [n.isdigit() for n in v.split(".")]
        if not all(parts):
            raise ValueError("Version must be in format 'X.Y.Z'")
        if len(parts) > 3:
            raise ValueError("Version must have at most 3 parts (X.Y.Z)")
        return v

# Footprint spec
class FootprintSpec(BaseModel):
    length: str | int
    width: str | int
    height: str | int # can be formula like "2*N+3"

    @field_validator("length", "width", "height")
    def validate_dimension(cls, v):
        match v:
            case int():
                if v <= 0:
                    raise ValueError("Dimension must be positive")
            case str():
                allowed_chars = set("0123456789N+-*/() ")
                if not set(v).issubset(allowed_chars):
                    raise ValueError("Dimension string can only contain digits, 'N', and math operators")
            case _:
                raise ValueError("Dimension must be an integer or a string formula")
        
        return v

class BaseDeviceSpec(BaseModel):
    textspecs: str
    repopath: str = "not-set"
    device_class: Literal["rds-router"]
    name: str = "unnamed device"
    versions: Dict[str, str]
    minecraft: MinecraftSpec
    survival_friendliness: Literal["high", "moderate", "low"]
    works_in_nether: bool = False
    locational: bool
    directional: bool
    footprint: FootprintSpec
    

# ------------------------
# RDS Router spec
# ------------------------
class RDSRouterSpec(BaseDeviceSpec):
    package_tech: str
    protocol: Literal["standard-rds", "other"]
    physical_ports: Dict[str, Union[int, str]]  # 'N' allowed
    logical_ports: Dict[str, Union[int, str]]   # 'N' allowed
    chunkloading_included: bool
    package_queue_included: bool
    package_queue_size: int = Field(..., ge=0)
    throughput: int = Field(..., ge=1)
    

    # Validator for YAML typos
    @field_validator("survival_friendliness")
    def fix_survival_typo(cls, v, values, **kwargs):
        if not v in ("high", "moderate", "low"):
            raise ValueError(f"survival_friendliness must be 'high', 'moderate', or 'low', not '{v}'")



def build_device_spec_object(data: dict) -> BaseDeviceSpec:
    device_class = data.get("device_class")
    
    match device_class:
        case "rds-router":
            return RDSRouterSpec(**data)
        case _:
            raise ValueError(f"Unsupported device_class: {device_class}")

