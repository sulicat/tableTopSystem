#!/bin/sh

v4l2-ctl -c white_balance_temperature_auto=0
v4l2-ctl -c white_balance_temperature=4000
v4l2-ctl -c exposure_auto_priority=0
v4l2-ctl -c exposure_auto=1
v4l2-ctl -c exposure_absolute=150