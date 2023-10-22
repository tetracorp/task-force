---
title: "Keyboard controls"
category: analysis
---

Keyboard commands work only on the title screen, move phase and fire phase.

### Title screen controls

As an undocumented feature, the title screen can be controlled with the keyboard
instead of the mouse.

- **Spacebar**: Play
- **F1**: Difficulty
- **F2**: Toggle music
- **F3**: Enter seed
- **F4**: Toggle centre play
- **F5**: Instructions

ESC is supposed to quit the game, but the relevant code is missing from the
executable. In the released source code, there's a check in the main loop for
they Escape key being pressed (raw value #117, which after a `not.b` and `ror.b
#1` has a [scancode](https://wiki.amigaos.net/wiki/Keymap_Library) of `$45` or
Escape). However, in would only trigger if Escape was held after leaving the
debriefing screen. In the released executable it just branches back to the title
screen. In the source, that branch instruction has been commented out.

Source code:

```assembly
main      jsr     initglobal
.mainloop jsr     cls
          jsr     titlescn
          jsr     missionscn
          jsr     teamscreen
          jsr     game
          jsr     debriefscn
          cmp.b   #117,$bfec01
          bne     .mainloop
;         bra     .mainloop
          rts
```

Disassembled fragment of executable:

```assembly
main      jsr     initglobal
.mainloop jsr     cls
          jsr     titlescn
          jsr     missionscn
          jsr     teamscreen
          jsr     game
          jsr     debriefscn
          bra.w   .mainloop
          rts
```

### Documented in-game controls

There are in-game controls, but the in-game Instructions already mentions these.
I'll repeat them here for completeness, and to note that there are no others.

During fire phase:

- **Return**: Detonate Remex.
- **Spacebar**: Pass (skip turn).
- **S**: Toggle music.
- **M**: Toggle map.

During keyboard phase:

- **M**: Toggle map.
- **S**: Toggle music.
- **Cursor up**: Move up.
- **Cursor down**: Move down.
- **Cursor left**: Move left.
- **Cursor right**: Move right.
- **Spacebar**: Pass (skip turn).

There are no keyboard controls to select weapon. Using the mouse, you can select
weapons in either move or fire phase, although there's no benefit to changing
weapons in movement phase.

Both the red buttons by the cursor detonate Remex; they work identically,
although of course only in fire mode. You can plant up to 10 Remex, and pressing
the button once will detonate all Remex. Detonating Remex uses up the user's
turn.
