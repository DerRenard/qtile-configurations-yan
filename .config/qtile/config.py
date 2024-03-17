from asyncio import SubprocessProtocol
import subprocess
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget # it sould be AS WIDGET!!!! DO NOT CHANGE THE NAME
from qtile_extras.widget import decorations
# from libqtile.utils import guess_terminal
import os

mod = "mod4"
terminal = "alacritty" #guess_terminal()

keys = [
    #---------- focusing -------------
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    #---------------------------------
    
    #----------- moving --------------
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    #---------------------------------
    
    #---------- resizing -------------
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    #---------------------------------

    #----- Manipulating Windows ------
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    #---------------------------------
    
    #------- Qtile's system ----------
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"), #reload config
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"), #exit qtile
    #---------------------------------
    
    #-------- Running Apps -----------
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "Escape", lazy.spawn(["sh","-c","$HOME/.config/rofi/launchers/type-1/launcher.sh"]), desc="Runs rofi"),
    # Key([mod], "Escape", lazy.spawn("rofi -show drun -show-icons"), desc="Runs rofi"),
    Key([mod], "backslash", lazy.spawn("xkill"), desc="Runs kill cursor"),
    #---------------------------------

    #--------- Screenshot ------------
    Key([mod], "bracketleft", lazy.spawn(["sh", "-c", "maim -s $HOME/Pictures/Screenshots/$(date +%F_%H-%M-%S)_partial.png"])),
    Key([mod], "bracketright", lazy.spawn(["sh", "-c", "maim $HOME/Pictures/Screenshots/$(date +%F_%H-%M-%S)_fullscreen.png"])),
    #---------------------------------
    Key([mod, "shift"], "bracketleft", lazy.spawn(["sh", "-c", "maim -s | xclip -selection clipboard -t image/png"])),
    Key([mod, "shift"], "bracketright", lazy.spawn(["sh", "-c", "maim | xclip -selection clipboard -t image/png"])),
    #---------------------------------
    #----------- Sound ---------------
    Key([], "XF86AudioMute", lazy.spawn("amixer -c 0 sset Master toggle")), # Mute
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -c 0 sset Master 1- unmute")), # Audio -
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -c 0 sset Master 1+ unmute")), # Audio +
    #---------------------------------
    #------- Keyboard Layout ---------
    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
    #---------------------------------
    #--------- Lockscreen ------------
    Key([mod, "shift","control"], "s", lazy.spawn(["sh","-c","$HOME/.config/rofi/applets/bin/powermenu.sh"])),
    #---------------------------------

]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)

# for vt in range(1, 8):
    # keys.append(
        # Key(
            # ["control", "mod1"],
            # f"f{vt}",
            # lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            # desc=f"Switch to VT{vt}",
        # )
    # )


#-------- Workspaces ---------
groups = [Group(i) for i in "123456789"] # change in "" for get another name of workspaces

for i in groups:
    keys.extend(
        [
            Key( # mod1 + group number = switch to group 
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            Key( # mod1 + shift + group number = switch to & move focused window to group
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
        ]
    )
#-----------------------------

#------- variables --------
colors = [
    ["#16161a", "#16161a"], # 1
    ['#DCDFE4', '#DCDFE4'], # 2
    ['#16161a', '#16161a'], # 3
    ['#f25c5c', '#f25c5c'], # 4
    ['#55b682', '#55b682'], # 5
    ['#ff9c6a', '#ff9c6a'], # 6
    ['#7aaaff', '#7aaaff'], # 7
    ['#f17ac6', '#f17ac6'], # 8
    ['#B87AFF', '#B87AFF'], # 9
    ['#e9ecf2', '#e9ecf2'], # 10 
    ['#212126', '#212126'], # 11
    ['#2a2a30', '#2a2a30'], # 12
    ['#373740', '#373740'], # 13
    ['#4f4f5c', '#4f4f5c'], # 14
    ['#676778', '#676778'], # 15
    ['#212126', '#212126'], # 16
    ['#9595ab', '#9595ab'], # 17
    ['#18181c', '#18181c'], # 18
    ["#43059c", "#43059c"], # 19
    ['#6f0aff', '#6f0aff']  # 20
]

fsize_icons = 16
fsize_text = 14
fsize_onlyIcons = 24
#--------------------------

layouts = [
    layout.Columns(
        # border_focus_stack=[colors[8], colors[9]],
        border_focus = colors[19],
        border_normal = colors[18], 
        border_on_single = True, 
        border_width = 3,
        margin = [2, 2, 2, 2],
        margin_on_single = [2, 2, 2, 2]
        ),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font = "JetBrainsMonoNL Nerd Font",
    padding = 2, # paddings between all widgets in bar
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar( # top left right bottom
            [
                # decorations.*
                # decorations []
                widget.Spacer(5),
                #------- Logo -------
                widget.TextBox(
                    " ",
                    # " ",
                    fontsize = fsize_onlyIcons,
                    foreground = "#0a9df2",
                    # foreground = colors[3][0],
                    mouse_callbacks = {"Button1": lazy.spawn("/home/yan/.config/rofi/launchers/type-1/launcher.sh")},
                    ),
                #---------------------
                widget.Spacer(2),
                #---- Workspaces -----
                widget.GroupBox(
                    fontsize=fsize_onlyIcons,
                    this_current_screen_border = colors[6],
                    block_highlight_text_color = colors[6],
                    highlight_method = 'line',
                    fmt='',
                    hide_unused = True,
                    padding = 5,
                    borderwidth = 4
                    ),
                #---------------------
                widget.Spacer(5),
                #------ Memory -------
                widget.Memory(
                    fontsize=fsize_text,
                    fmt = " {}",
                    measure_mem='G',
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[4][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        )
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                #------- CPU ---------
                widget.CPU(
                    fontsize=fsize_text,
                    fmt = " {}",
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[3][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        )
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                #---- Temperature ----
                widget.ThermalSensor(
                    fontsize=fsize_text,
                    fmt = " {}",
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[5][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        )
                    ],
                    ),
                widget.Spacer(5),
                widget.ThermalSensor(
                    fontsize=fsize_text,
                    metric = False,
                    threshold = 194,
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[5][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        )
                    ],
                    ),
                #---------------------

                #---------------------
                widget.Spacer(), 
                #---------------------
                
                #----- Calendar- -----
                widget.Clock(
                    fontsize=fsize_text,
                    format="%m.%d.%y",
                    fmt = "  {}",
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[7][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        ),
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                #------- Time --------
                widget.Clock(
                    fontsize=fsize_text,
                    format="%H:%M",
                    fmt = " {}",
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[8][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        ),
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                #-------- Day --------
                widget.Clock(
                    fontsize=fsize_text,
                    format="%A",
                    fmt = "󱛡 {}",
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[7][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        ),
                    ],
                    ),
                #---------------------

                #---------------------
                widget.Spacer(),
                #---------------------
                #----- Apss Tray -----
                widget.Systray(
                    fontsize=fsize_text,
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[6][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        )
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                #---- Disk Usage -----
                widget.DF(
                    fontsize=fsize_text,
                    format = ' ({uf}{m}|{r:.0f}%)',
                    partition = '/home',
                    update_interval = 1,
                    visible_on_warn = False,
                    measure = 'G',
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[8][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        )
                    ],
                    ),
                widget.Spacer(5),
                widget.DF(
                    fontsize=fsize_text,
                    format = '󱂶 ({uf}{m}|{r:.0f}%)',
                    partition = '/',
                    update_interval = 1,
                    visible_on_warn = False,
                    measure = 'G',
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[8][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        )
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                # ------ Battery ------ 
                # widget.Battery(
                #     fontsize=fsize_text,
                #     battery = "BAT0",
                #     charge_char = "󰂐",
                #     discharge_char = "󰂍",
                #     empty_char = "󱟨",
                #     full_char = "󰁹",
                #     unknown_char = "󱃌",
                #     fmt = "  {}",
                #     format = "{char} {percent:2.0%}",
                #     low_percentage = 0.2, 
                #     low_foreground = colors[3][0],
                #     update_interval = 10,
                #     notification_timeout = 0,
                #     decorations = [
                #         decorations.BorderDecoration(
                #             border_width = [0, 0, 2, 0],
                #             colour = [
                #                 colors[7][0], 
                #                 ],
                #             padding = 0,
                #             margin_x = 2,
                #             margin_y = 2,
                #         )
                #     ],
                #     ),
                #--------------------- 
                # widget.Spacer(5),
                #---- Brightness ----- 
                # widget.Backlight(
                #     fontsize=fsize_text,
                #     fmt = "󰃠 {}",
                #     decorations = [
                #         decorations.BorderDecoration(
                #             border_width = [0, 0, 2, 0],
                #             colour = [
                #                 colors[7][0], 
                #                 ],
                #             padding = 0,
                #             margin_x = 2,
                #             margin_y = 2,
                #         )
                #     ],
                #     ),
                #---------------------
                # widget.Spacer(5),
                #------ Volume -------
                widget.Volume(
                    fontsize=fsize_text,
                    # emoji = True,
                    # emoji_list = ['󰕿 ','󰖀 ','󰕾 ',' '],
                    fmt = "󰕾 {}",
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[5][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        )
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                #------- Net ---------
                widget.Net(
                    fontsize=fsize_text,
                    format='Wiznet:  {down:.0f}{down_suffix}  {up:.0f}{up_suffix}',
                    interface='eno1',
                    # interface='wlan0',
                    fmt = "  {}",
                    mouse_callbacks = {"Button1": lazy.spawn(["sh","-c","$HOME/.config/rofi/rofi-wifi-menu/rofi-wifi-menu.sh"])},
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[3][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        ),
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                #----- Keyboard ------
                widget.KeyboardLayout(
                    fontsize=fsize_text,
                    configured_keyboards = ['us', 'ru'],
                    fmt="󰥻 {}",
                    decorations = [
                        decorations.BorderDecoration(
                            border_width = [0, 0, 2, 0],
                            colour = [
                                colors[4][0], 
                                ],
                            padding = 0,
                            margin_x = 2,
                            margin_y = 2,
                        ),
                    ],
                    ),
                #---------------------
                widget.Spacer(5),
                #---- Exit Tray ------ 
                widget.TextBox(
                    "⏻ ",
                    fontsize=16,
                    foreground = "#f01a24",
                    mouse_callbacks = {"Button1": lazy.spawn(["sh","-c","$HOME/.config/rofi/applets/bin/powermenu.sh"])},
                    ),
                #---------------------
                widget.Spacer(5),
            ],
            30,
            # background = "#00000000", #fully transparent
            background = "#00000099", # not fully transparent

            # Border Size
            # border_width=[2, 2, 2, 2],  # Draw top and bottom borders
            # border_color=["ff00ff", "ff00ff", "ff00ff", "ff00ff"]  # Borders are magenta
        ),
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

#---------- Autostart ------------ 
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/Autostart.sh')
    subprocess.Popen([home])
#---------------------------------
