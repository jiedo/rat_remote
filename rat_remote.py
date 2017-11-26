#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

# modprobe uinput

from evdev import InputDevice, categorize, ecodes
import uinput


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
    uinput.KEY_TAB,
    uinput.KEY_W,
    uinput.KEY_Q,
    ])
# virtual_keyboard.emit_click(uinput.KEY_H)
# virtual_keyboard.emit(uinput.KEY_LEFTCTRL, 1)
# virtual_keyboard.emit(uinput.KEY_LEFTCTRL, 0)

virtual_keyboard.emit_click(uinput.KEY_KEYBOARD)

dev = InputDevice('/dev/input/event8')
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

    elif event.code == CODE_MOVE_X :
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

    elif event.code == CODE_MOVE_Y :
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
        print MAP_EVENT_TO_NAME[map_event]
        if map_event == EVENT_LEFT_CLICK:
            virtual_mouse.emit(uinput.BTN_LEFT, 1)
            virtual_mouse.emit(uinput.BTN_LEFT, 0)

        elif map_event == EVENT_RIGHT_CLICK:
            virtual_mouse.emit(uinput.BTN_RIGHT, 1)
            virtual_mouse.emit(uinput.BTN_RIGHT, 0)

        elif map_event == EVENT_MID_CLICK:
            virtual_mouse.emit(uinput.BTN_MIDDLE, 1)
            virtual_mouse.emit(uinput.BTN_MIDDLE, 0)

        elif map_event == EVENT_SCROLL_UP:
            virtual_keyboard.emit_combo([
                uinput.KEY_LEFTCTRL,
                uinput.KEY_LEFTSHIFT,
                uinput.KEY_TAB,
            ])
        elif map_event == EVENT_SCROLL_DOWN:
            virtual_keyboard.emit_combo([
                uinput.KEY_LEFTCTRL,
                uinput.KEY_TAB,
            ])

        elif map_event == EVENT_LEFT_RIGHT_UP:
            virtual_keyboard.emit_combo([
                uinput.KEY_LEFTCTRL,
                uinput.KEY_W,
            ])
        elif map_event == EVENT_LEFT_SCROLL_DOWN:
            pass

        elif map_event == EVENT_LEFT_SCROLL_UP:
            virtual_mouse.emit(uinput.REL_HWHEEL, 1)
        elif map_event == EVENT_LEFT_SCROLL_DOWN:
            virtual_mouse.emit(uinput.REL_HWHEEL, -1)

dev.ungrab()
