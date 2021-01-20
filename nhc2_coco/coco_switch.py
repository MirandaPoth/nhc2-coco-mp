import logging

from .coco_entity import CoCoEntity
from .const import KEY_STATUS, KEY_BASICSTATE, VALUE_ON, VALUE_OFF
from .helpers import extract_property_value_from_device

_LOGGER = logging.getLogger(__name__)

class CoCoSwitch(CoCoEntity):

    @property
    def is_on(self):
        return self._is_on

    @property
    def on_off_property(self):
        # 'BasicState' for generic and alloff, 'Status' for the rest
        return self._on_off_property

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._is_on = None
        self._on_off_property = None
        self.update_dev(dev, callback_container)

    def turn_on(self):
        self._command_device_control(self._uuid, self.on_off_property, VALUE_ON)
        _LOGGER.debug(self.name + ' is turning ' + self.on_off_property + ' ON')

    def turn_off(self):
        self._command_device_control(self._uuid, self.on_off_property, VALUE_OFF)
        _LOGGER.debug(self.name + ' is turning ' + self.on_off_property + ' OFF')

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        status_value = extract_property_value_from_device(dev, KEY_STATUS)
        # MP 20/01/2021 for generic and alloff, property 'BasicState' says whether it's off or on, not 'Status'
        if status_value:
            self._on_off_property = KEY_STATUS
        else: 
            self._on_off_property = KEY_BASICSTATE
        _LOGGER.debug('For ' + self.name + ', self.on_off_property is ' + self.on_off_property)
        # MP debugging ...
        basicstate_value = extract_property_value_from_device(dev, KEY_BASICSTATE)
        if basicstate_value:
            _LOGGER.debug('BasicState of device ' + self.model + ' ' + self.uuid + ' ' + self.name + ' is ' + basicstate_value)

        """
        if status_value and self._is_on != (self.on_off_property == VALUE_ON):
            self._is_on = (status_value == VALUE_ON)
            has_changed = True
        """            

        if ( status_value and self._is_on != (status_value == VALUE_ON) ) or \
            ( basicstate_value and self._is_on != (basicstate_value == VALUE_ON) ):
            self._is_on = (status_value == VALUE_ON)
            has_changed = True

        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()
