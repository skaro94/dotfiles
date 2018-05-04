#!/bin/zsh

function get_screen_resolution_x {
    xdpyinfo | awk -F '[ x]+' '/dimensions:/{print $3}'
}


function get_screen_resolution_y {
    xdpyinfo | awk -F '[ x]+' '/dimensions:/{print $4}'
}

res_x=$(get_screen_resolution_x)
res_y=$(get_screen_resolution_y)

wmctrl -r :ACTIVE: -e 0,0,0,1460,1020
wmctrl -r 'Android Emulator' -e 0,$res_x,0,-1,-1
wmctrl -r 'Emulator' -e 0,0,0,-1,-1
