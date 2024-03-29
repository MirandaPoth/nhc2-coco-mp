# MP
import logging

from .coco_entity import CoCoEntity
# MP Added the last two to cope with generics_as_switches. More related code below.
from .const import KEY_STATUS, VALUE_ON, VALUE_OFF, KEY_BASICSTATE, VALUE_TRIGGERED 
from .helpers import extract_property_value_from_device

# MP
_LOGGER = logging.getLogger(__name__)

class CoCoSwitch(CoCoEntity):

    @property
    def is_on(self):
        return self._is_on

    # MP
    @property
    def on_off_property(self):
        # MP 'BasicState' for generic and alloff, 'Status' for the rest
        return self._on_off_property

    def __init__(self, dev, callback_container, client, profile_creation_id, command_device_control):
        super().__init__(dev, callback_container, client, profile_creation_id, command_device_control)
        self._is_on = None
        # MP
        self._on_off_property = None
        self.update_dev(dev, callback_container)

    def turn_on(self):
        # ORIGINAL: self._command_device_control(self._uuid, KEY_STATUS, VALUE_ON)

        # MP This gets called from HA when it wants to turn it ON
        _LOGGER.debug('HA is turning switch ON ' + self.name + ' (on_off_property is ' + self.on_off_property + ')')
        if self.on_off_property == KEY_BASICSTATE:
            self._command_device_control(self._uuid, self.on_off_property, VALUE_TRIGGERED)
        else:
            self._command_device_control(self._uuid, self.on_off_property, VALUE_ON)


    def turn_off(self):
        # ORIGINAL: self._command_device_control(self._uuid, KEY_STATUS, VALUE_OFF)

        # MP 18/09/2021 Need to cope with Basicstate too like above
        _LOGGER.debug('HA is turning switch OFF ' + self.name + ' (on_off_property is ' + self.on_off_property + ')')
        if self.on_off_property == KEY_BASICSTATE:
            # These devices are like a toggle, you press to turn on and press to turn off again
            self._command_device_control(self._uuid, self.on_off_property, VALUE_TRIGGERED)
        else:
            self._command_device_control(self._uuid, self.on_off_property, VALUE_OFF)

    def update_dev(self, dev, callback_container=None):
        has_changed = super().update_dev(dev, callback_container)
        status_value = extract_property_value_from_device(dev, KEY_STATUS)

        # MP 16-09-2021 (from 20/01/2021) for generic and alloff, property 'BasicState' says whether it's off or on, not 'Status'
        if status_value:
            self._on_off_property = KEY_STATUS
        else: 
            self._on_off_property = KEY_BASICSTATE
        basicstate_value = extract_property_value_from_device(dev, KEY_BASICSTATE)

        # MP debugging
        _LOGGER.debug('HA is updating switch device ' + self.name + ' (on_off_property is ' + self.on_off_property + ')')
        #_LOGGER.debug('For ' + self.name + ', self.on_off_property is ' + self.on_off_property)
        if basicstate_value:
            _LOGGER.debug('BasicState of device ' + self.model + ' ' + self.uuid + ' ' + self.name + ' is ' + basicstate_value)
        else:
            _LOGGER.debug('Status of device ' + self.model + ' ' + self.uuid + ' ' + self.name + ' is ' + status_value)

        # ORIGINAL:
        #if status_value and self._is_on != (status_value == VALUE_ON):
        #    self._is_on = (status_value == VALUE_ON)
        #    has_changed = True

        if ( status_value and self._is_on != (status_value == VALUE_ON) ) or \
            ( basicstate_value and self._is_on != (basicstate_value == VALUE_ON) ):
            self._is_on = (status_value == VALUE_ON)
            has_changed = True

        # MP debugging
        if has_changed:
            _LOGGER.debug('... has_changed is True')
        else:
            _LOGGER.debug('... has_changed is False')

        return has_changed

    def _update(self, dev):
        has_changed = self.update_dev(dev)
        if has_changed:
            self._state_changed()
