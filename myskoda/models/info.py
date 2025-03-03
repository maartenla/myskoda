"""Models for responses of api/v2/garage/vehicles/{vin}."""

import logging
from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

from mashumaro import field_options
from mashumaro.mixins.orjson import DataClassORJSONMixin

_LOGGER = logging.getLogger(__name__)


class CapabilityId(StrEnum):
    ACCESS = "ACCESS"
    AIR_CONDITIONING = "AIR_CONDITIONING"
    AIR_CONDITIONING_HEATING_SOURCE_AUXILIARY = "AIR_CONDITIONING_HEATING_SOURCE_AUXILIARY"
    AIR_CONDITIONING_HEATING_SOURCE_ELECTRIC = "AIR_CONDITIONING_HEATING_SOURCE_ELECTRIC"
    AIR_CONDITIONING_SAVE_AND_ACTIVATE = "AIR_CONDITIONING_SAVE_AND_ACTIVATE"
    AIR_CONDITIONING_SMART_SETTINGS = "AIR_CONDITIONING_SMART_SETTINGS"
    AIR_CONDITIONING_TIMERS = "AIR_CONDITIONING_TIMERS"
    AUTOMATION = "AUTOMATION"
    BATTERY_CHARGING_CARE = "BATTERY_CHARGING_CARE"
    BATTERY_SUPPORT = "BATTERY_SUPPORT"
    CARE_AND_INSURANCE = "CARE_AND_INSURANCE"
    CHARGE_MODE_SELECTION = "CHARGE_MODE_SELECTION"
    CHARGING = "CHARGING"
    CHARGING_MEB = "CHARGING_MEB"
    CHARGING_MQB = "CHARGING_MQB"
    CHARGING_PROFILES = "CHARGING_PROFILES"
    CHARGING_STATIONS = "CHARGING_STATIONS"
    CUBIC = "CUBIC"
    DEALER_APPOINTMENT = "DEALER_APPOINTMENT"
    DEPARTURE_TIMERS = "DEPARTURE_TIMERS"
    DESTINATIONS = "DESTINATIONS"
    DESTINATION_IMPORT = "DESTINATION_IMPORT"
    DESTINATION_IMPORT_UPGRADABLE = "DESTINATION_IMPORT_UPGRADABLE"
    DIGICERT = "DIGICERT"
    EMERGENCY_CALLING = "EMERGENCY_CALLING"
    EV_ROUTE_PLANNING = "EV_ROUTE_PLANNING"
    EXTENDED_CHARGING_SETTINGS = "EXTENDED_CHARGING_SETTINGS"
    FUEL_STATUS = "FUEL_STATUS"
    GEO_FENCE = "GEO_FENCE"
    GUEST_USER_MANAGEMENT = "GUEST_USER_MANAGEMENT"
    HONK_AND_FLASH = "HONK_AND_FLASH"
    ICE_VEHICLE_RTS = "ICE_VEHICLE_RTS"
    LOYALTY_PROGRAM = "LOYALTY_PROGRAM"
    MAP_UPDATE = "MAP_UPDATE"
    MEASUREMENTS = "MEASUREMENTS"
    MISUSE_PROTECTION = "MISUSE_PROTECTION"
    NEWS = "NEWS"
    ONLINE_SPEECH_GPS = "ONLINE_SPEECH_GPS"
    PARKING_INFORMATION = "PARKING_INFORMATION"
    PARKING_POSITION = "PARKING_POSITION"
    PAY_TO_FUEL = "PAY_TO_FUEL"
    PAY_TO_PARK = "PAY_TO_PARK"
    PLUG_AND_CHARGE = "PLUG_AND_CHARGE"
    POI_SEARCH = "POI_SEARCH"
    POWERPASS_TARIFFS = "POWERPASS_TARIFFS"
    ROADSIDE_ASSISTANT = "ROADSIDE_ASSISTANT"
    ROUTE_IMPORT = "ROUTE_IMPORT"
    ROUTE_PLANNING_5_CHARGERS = "ROUTE_PLANNING_5_CHARGERS"
    ROUTING = "ROUTING"
    SERVICE_PARTNER = "SERVICE_PARTNER"
    SPEED_ALERT = "SPEED_ALERT"
    STATE = "STATE"
    SUBSCRIPTIONS = "SUBSCRIPTIONS"
    TRAFFIC_INFORMATION = "TRAFFIC_INFORMATION"
    TRIP_STATISTICS = "TRIP_STATISTICS"
    VEHICLE_HEALTH_INSPECTION = "VEHICLE_HEALTH_INSPECTION"
    VEHICLE_HEALTH_WARNINGS = "VEHICLE_HEALTH_WARNINGS"
    VEHICLE_HEALTH_WARNINGS_WITH_WAKE_UP = "VEHICLE_HEALTH_WARNINGS_WITH_WAKE_UP"
    VEHICLE_SERVICES_BACKUPS = "VEHICLE_SERVICES_BACKUPS"
    VEHICLE_WAKE_UP = "VEHICLE_WAKE_UP"
    VEHICLE_WAKE_UP_TRIGGER = "VEHICLE_WAKE_UP_TRIGGER"
    WARNING_LIGHTS = "WARNING_LIGHTS"
    WEB_RADIO = "WEB_RADIO"
    WINDOW_HEATING = "WINDOW_HEATING"


class CapabilityStatus(StrEnum):
    DEACTIVATED_BY_ACTIVE_VEHICLE_USER = "DEACTIVATED_BY_ACTIVE_VEHICLE_USER"
    DISABLED_BY_USER = "DISABLED_BY_USER"
    FRONTEND_SWITCHED_OFF = "FRONTEND_SWITCHED_OFF"
    INITIALLY_DISABLED = "INITIALLY_DISABLED"
    INSUFFICIENT_BATTERY_LEVEL = "INSUFFICIENT_BATTERY_LEVEL"
    LICENSE_EXPIRED = "LICENSE_EXPIRED"
    LICENSE_MISSING = "LICENSE_MISSING"
    LOCATION_DATA_DISABLED = "LOCATION_DATA_DISABLED"


@dataclass
class Capability(DataClassORJSONMixin):
    id: CapabilityId
    statuses: list[CapabilityStatus]

    def is_available(self) -> bool:
        """Check whether the capability can currently be used.

        It looks like every status is an indication that the capability is not available.
        """
        return not self.statuses


def drop_unknown_capabilities(value: list[dict]) -> list[Capability]:
    """Drop any unknown capabilities and log a message."""
    unknown_capabilities = [c for c in value if c["id"] not in CapabilityId]
    if unknown_capabilities:
        _LOGGER.info(f"Dropping unknown capabilities: {unknown_capabilities}")
    return [Capability.from_dict(c) for c in value if c["id"] in CapabilityId]


@dataclass
class Capabilities(DataClassORJSONMixin):
    capabilities: list[Capability] = field(
        metadata=field_options(deserialize=drop_unknown_capabilities)
    )


@dataclass
class Battery(DataClassORJSONMixin):
    capacity: int = field(metadata=field_options(alias="capacityInKWh"))


class BodyType(StrEnum):
    SUV = "SUV"
    SUV_COUPE = "SUV Coupe"
    COMBI = "Combi"
    LIFTBACK = "Liftback"


class VehicleState(StrEnum):
    ACTIVATED = "ACTIVATED"


@dataclass
class Engine(DataClassORJSONMixin):
    type: str
    power: int = field(metadata=field_options(alias="powerInKW"))
    capacity_in_liters: float | None = field(
        default=None, metadata=field_options(alias="capacityInLiters")
    )


@dataclass
class Gearbox(DataClassORJSONMixin):
    type: str


@dataclass
class Specification(DataClassORJSONMixin):
    body: BodyType
    engine: Engine
    model: str
    title: str
    manufacturing_date: date = field(metadata=field_options(alias="manufacturingDate"))
    model_year: str = field(metadata=field_options(alias="modelYear"))
    system_code: str = field(metadata=field_options(alias="systemCode"))
    system_model_id: str = field(metadata=field_options(alias="systemModelId"))
    battery: Battery | None = field(default=None)
    max_charging_power: int | None = field(
        default=None, metadata=field_options(alias="maxChargingPowerInKW")
    )
    trim_level: str | None = field(default=None, metadata=field_options(alias="trimLevel"))


@dataclass
class ServicePartner(DataClassORJSONMixin):
    id: str = field(metadata=field_options(alias="servicePartnerId"))


class ErrorType(StrEnum):
    MISSING_RENDER = "MISSING_RENDER"


@dataclass
class Error(DataClassORJSONMixin):
    description: str
    type: ErrorType


@dataclass
class Info(DataClassORJSONMixin):
    """Basic vehicle information."""

    state: VehicleState
    specification: Specification
    vin: str
    name: str
    capabilities: Capabilities
    device_platform: str = field(metadata=field_options(alias="devicePlatform"))
    service_partner: ServicePartner = field(metadata=field_options(alias="servicePartner"))
    workshop_mode_enabled: bool = field(metadata=field_options(alias="workshopModeEnabled"))
    software_version: str | None = field(
        default=None, metadata=field_options(alias="softwareVersion")
    )
    license_plate: str | None = field(default=None, metadata=field_options(alias="licensePlate"))
    errors: list[Error] | None = field(default=None)

    def has_capability(self, cap: CapabilityId) -> bool:
        """Check for a capability.

        Checks whether a vehicle generally has a capability.
        Does not check whether it's actually available.
        """
        return any(capability.id == cap for capability in self.capabilities.capabilities)

    def is_capability_available(self, cap: CapabilityId) -> bool:
        """Check for capability availability.

        Checks whether the vehicle has the capability and whether it is currently
        available. A capability can be unavailable for example if it's deactivated
        by the currently active user.
        """
        return any(
            capability.id == cap and capability.is_available()
            for capability in self.capabilities.capabilities
        )

    def get_model_name(self) -> str:
        """Return the name of the vehicle's model."""
        model = self.specification.model
        engine = self.specification.engine
        model_year = self.specification.model_year
        system_model_id = self.specification.system_model_id
        return f"{model} {engine} {model_year} ({system_model_id})"
