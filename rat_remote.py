#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# modprobe uinput

from evdev import InputDevice, categorize, ecodes
import uinput
from subprocess import *
import sys, os

DISABLED = False
CODE_LEFT = 272
CODE_RIGHT = 273
CODE_MID = 274
CODE_MOVE_X = 0
CODE_MOVE_Y = 1
CODE_SCROLL = 8

EVENT_NONE = 0
EVENT_LEFT_CLICK = 1
EVENT_RIGHT_CLICK = 2
EVENT_MID_CLICK = 3
EVENT_SCROLL_UP = 4
EVENT_SCROLL_DOWN = 5
EVENT_LEFT_SCROLL_UP = 6
EVENT_LEFT_SCROLL_DOWN = 7
EVENT_RIGHT_SCROLL_UP = 8
EVENT_RIGHT_SCROLL_DOWN = 9
EVENT_LEFT_RIGHT_UP = 10
EVENT_LEFT_RIGHT_DOWN = 11
EVENT_LEFT_RIGHT_SCROLL_UP = 12
EVENT_LEFT_RIGHT_SCROLL_DOWN = 13
EVENT_MID_SCROLL_UP = 14
EVENT_MID_SCROLL_DOWN = 15

MAP_EVENT_TO_NAME = [
    "EVENT_NONE",
    "EVENT_LEFT_CLICK",
    "EVENT_RIGHT_CLICK",
    "EVENT_MID_CLICK",
    "EVENT_SCROLL_UP",
    "EVENT_SCROLL_DOWN",
    "EVENT_LEFT_SCROLL_UP",
    "EVENT_LEFT_SCROLL_DOWN",
    "EVENT_RIGHT_SCROLL_UP",
    "EVENT_RIGHT_SCROLL_DOWN",
    "EVENT_LEFT_RIGHT_UP",
    "EVENT_LEFT_RIGHT_DOWN",
    "EVENT_LEFT_RIGHT_SCROLL_UP",
    "EVENT_LEFT_RIGHT_SCROLL_DOWN",
    "EVENT_MID_SCROLL_UP",
    "EVENT_MID_SCROLL_DOWN",
]

virtual_mouse = uinput.Device([
    uinput.BTN_LEFT,
    uinput.BTN_MIDDLE,
    uinput.BTN_RIGHT,
    uinput.REL_X,
    uinput.REL_Y,
    uinput.REL_WHEEL,
    uinput.REL_HWHEEL,
])

# Initialize keyboard, choosing used keys
virtual_keyboard = uinput.Device([
    uinput.KEY_KEYBOARD,
    uinput.KEY_LEFTCTRL,
    uinput.KEY_LEFTSHIFT,
    uinput.KEY_LEFTALT,
    uinput.KEY_ESC,
    uinput.KEY_ENTER,
    uinput.KEY_SPACE,
    uinput.KEY_TAB,
    uinput.KEY_F2,
    uinput.KEY_F4,
    uinput.KEY_1,
    uinput.KEY_2,
    uinput.KEY_A,
    uinput.KEY_B,
    uinput.KEY_C,
    uinput.KEY_D,
    uinput.KEY_E,
    uinput.KEY_F,
    uinput.KEY_G,
    uinput.KEY_H,
    uinput.KEY_I,
    uinput.KEY_J,
    uinput.KEY_K,
    uinput.KEY_L,
    uinput.KEY_M,
    uinput.KEY_N,
    uinput.KEY_O,
    uinput.KEY_P,
    uinput.KEY_Q,
    uinput.KEY_R,
    uinput.KEY_S,
    uinput.KEY_T,
    uinput.KEY_U,
    uinput.KEY_V,
    uinput.KEY_W,
    uinput.KEY_X,
    uinput.KEY_Y,
    uinput.KEY_Z,
    ])
# virtual_keyboard.emit_click(uinput.KEY_H)
# virtual_keyboard.emit(uinput.KEY_LEFTCTRL, 1)
# virtual_keyboard.emit(uinput.KEY_LEFTCTRL, 0)

virtual_keyboard.emit_click(uinput.KEY_KEYBOARD)

dev = InputDevice('/dev/input/by-id/usb-Logitech_USB_Receiver-event-mouse')
print dev
count_movement_times = 0
COUNT_MOVEMENT_LIMIT = 10

dev.grab()

button_left = False
button_right = False
button_mid = False

only_button_left_click = False
only_button_right_click = False
only_button_mid_click = False
both_left_right_click = False

current_window = ""

for event in dev.read_loop():
    map_event = EVENT_NONE
    if event.code == CODE_LEFT:
        count_movement_times = 0
        only_button_right_click = False
        only_button_mid_click = False
        if event.value == 1:
            button_left = True
            if button_right:
                map_event = EVENT_LEFT_RIGHT_DOWN
                both_left_right_click = True
            else:
                only_button_left_click = True
        elif event.value == 0:
            button_left = False
            if only_button_left_click:
                map_event = EVENT_LEFT_CLICK
                only_button_left_click = False
            if both_left_right_click and not button_right:
                map_event = EVENT_LEFT_RIGHT_UP
                both_left_right_click = False

    elif event.code == CODE_RIGHT:
        count_movement_times = 0
        only_button_left_click = False
        only_button_mid_click = False
        if event.value == 1:
            button_right = True
            if button_left:
                map_event = EVENT_LEFT_RIGHT_DOWN
                both_left_right_click = True
            else:
                only_button_right_click = True
        elif event.value == 0:
            button_right = False
            if only_button_right_click:
                map_event = EVENT_RIGHT_CLICK
                only_button_right_click = False
            if both_left_right_click and not button_left:
                map_event = EVENT_LEFT_RIGHT_UP
                both_left_right_click = False

    elif event.code == CODE_MID:
        count_movement_times = 0
        only_button_left_click = False
        only_button_right_click = False
        if event.value == 1:
            button_mid = True
            only_button_mid_click = True
        elif event.value == 0:
            button_mid = False
            if only_button_mid_click:
                map_event = EVENT_MID_CLICK
                only_button_mid_click = False

    elif event.code == CODE_SCROLL:
        count_movement_times = 0
        only_button_left_click = False
        only_button_right_click = False
        only_button_mid_click = False
        both_left_right_click = False
        if event.value == 1:    # up
            if button_left and button_right:
                map_event = EVENT_LEFT_RIGHT_SCROLL_UP
            elif button_left:
                map_event = EVENT_LEFT_SCROLL_UP
            elif button_right:
                map_event = EVENT_RIGHT_SCROLL_UP
            elif button_mid:
                map_event = EVENT_MID_SCROLL_UP
            else:
                map_event = EVENT_SCROLL_UP
        elif event.value == -1:  # down
            if button_left and button_right:
                map_event = EVENT_LEFT_RIGHT_SCROLL_DOWN
            elif button_left:
                map_event = EVENT_LEFT_SCROLL_DOWN
            elif button_right:
                map_event = EVENT_RIGHT_SCROLL_DOWN
            elif button_mid:
                map_event = EVENT_MID_SCROLL_DOWN
            else:
                map_event = EVENT_SCROLL_DOWN

    elif event.code == CODE_MOVE_X and DISABLED:
        count_movement_times += 1
        if count_movement_times > COUNT_MOVEMENT_LIMIT:
            only_button_left_click = False
            only_button_right_click = False
            only_button_mid_click = False
            both_left_right_click = False
        if event.value != 0:
            virtual_mouse.emit(uinput.REL_X, event.value)
            if button_left or button_right:
                virtual_mouse.emit(uinput.REL_HWHEEL, -event.value)

    elif event.code == CODE_MOVE_Y and DISABLED:
        count_movement_times += 1
        if count_movement_times > COUNT_MOVEMENT_LIMIT:
            only_button_left_click = False
            only_button_right_click = False
            only_button_mid_click = False
            both_left_right_click = False
        if event.value != 0:
            virtual_mouse.emit(uinput.REL_Y, event.value)
            if button_left or button_right:
                virtual_mouse.emit(uinput.REL_WHEEL, event.value)

    if map_event > 0:
        # if not current_window or map_event == EVENT_MID_CLICK:
        bufsize = 1024
        cmd_listwds = "ratpoison -c 'windows %c %s'|grep '*'"
        run_listwds = Popen(cmd_listwds, shell=True, bufsize=bufsize, stdout=PIPE).stdout
        current_window = run_listwds.read().split()[0]

        # print MAP_EVENT_TO_NAME[map_event]
        # print current_window
        base_config = {
            EVENT_LEFT_RIGHT_SCROLL_DOWN: (uinput.KEY_F4,),
            EVENT_LEFT_RIGHT_SCROLL_UP: (uinput.KEY_F2,),
        }

        map_config = {
            "Terminator": {
                EVENT_LEFT_CLICK: (uinput.KEY_L,),
                EVENT_RIGHT_CLICK: (uinput.KEY_R,),
                EVENT_MID_CLICK: (uinput.KEY_M,),
                EVENT_SCROLL_UP: [uinput.KEY_LEFTCTRL,
                                  uinput.KEY_A,],
                EVENT_SCROLL_DOWN: [uinput.KEY_LEFTCTRL,
                                    uinput.KEY_F,],
                EVENT_LEFT_RIGHT_DOWN: (uinput.KEY_B,),
                EVENT_LEFT_RIGHT_UP: [uinput.KEY_LEFTCTRL,
                                      uinput.KEY_B,],
                EVENT_RIGHT_SCROLL_UP: (uinput.KEY_H,),
                EVENT_RIGHT_SCROLL_DOWN: (uinput.KEY_J,),
                EVENT_LEFT_SCROLL_UP: (uinput.KEY_K,),
                EVENT_LEFT_SCROLL_DOWN: (uinput.KEY_L,),
            },
            "main.py": {
                EVENT_LEFT_CLICK: (uinput.KEY_ENTER,),
                EVENT_RIGHT_CLICK: (uinput.KEY_ESC,),
                EVENT_MID_CLICK: (uinput.KEY_SPACE,),
                EVENT_SCROLL_UP: (uinput.KEY_H,),
                EVENT_SCROLL_DOWN: (uinput.KEY_L,),
                # EVENT_LEFT_RIGHT_DOWN: (uinput.KEY_SPACE,),
                # EVENT_LEFT_RIGHT_UP: (uinput.KEY_SPACE,),
                EVENT_RIGHT_SCROLL_UP: (uinput.KEY_K,),
                EVENT_RIGHT_SCROLL_DOWN: (uinput.KEY_J,),
                EVENT_LEFT_SCROLL_UP: (uinput.KEY_2,),
                EVENT_LEFT_SCROLL_DOWN: (uinput.KEY_1,),
            },

            "Chromium": {
                EVENT_LEFT_CLICK: (uinput.KEY_S,),
                EVENT_RIGHT_CLICK: (uinput.KEY_SPACE,),
            },
            "Chromium.def": {
                EVENT_LEFT_CLICK: ((uinput.KEY_G,),
                                   (uinput.KEY_G,),),

                EVENT_RIGHT_CLICK: ([uinput.KEY_LEFTSHIFT, uinput.KEY_G,],
                                    [uinput.KEY_LEFTSHIFT, uinput.KEY_G,],),

                EVENT_MID_CLICK: (uinput.KEY_T,),

                EVENT_SCROLL_UP: [ # uinput.KEY_LEFTCTRL,
                                  uinput.KEY_K,],

                EVENT_SCROLL_DOWN: [ # uinput.KEY_LEFTCTRL,
                                    uinput.KEY_J,],

                EVENT_LEFT_RIGHT_DOWN: (uinput.KEY_B,),

                EVENT_LEFT_RIGHT_UP: [uinput.KEY_LEFTCTRL,
                                      uinput.KEY_TAB,],

                EVENT_RIGHT_SCROLL_UP: (uinput.KEY_H,),

                EVENT_RIGHT_SCROLL_DOWN: (uinput.KEY_J,),

                EVENT_LEFT_SCROLL_UP: (uinput.KEY_K,),

                EVENT_LEFT_SCROLL_DOWN: (uinput.KEY_L,),
            },
        }

        if map_event in base_config:
            keys = base_config[map_event]
        else:
            keys = map_config.get(current_window, {}).get(map_event, [])
        if len(keys) > 1:
            if type(keys) == tuple:
                for key in keys:
                    if len(key) > 1:
                        virtual_keyboard.emit_combo(key)
                    else:
                        virtual_keyboard.emit_click(key[0])
            else:
                virtual_keyboard.emit_combo(keys)
        elif len(keys) == 1:
            virtual_keyboard.emit_click(keys[0])

dev.ungrab()
