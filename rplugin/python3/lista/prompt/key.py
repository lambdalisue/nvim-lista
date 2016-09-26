import curses.ascii


class Keys:
    CR = curses.ascii.CR
    ESC = curses.ascii.ESC
    DEL = curses.ascii.DEL
    BS = curses.ascii.BS

    C_A = ord(curses.ascii.ctrl('a'))
    C_B = ord(curses.ascii.ctrl('b'))
    C_D = ord(curses.ascii.ctrl('d'))
    C_E = ord(curses.ascii.ctrl('e'))
    C_F = ord(curses.ascii.ctrl('f'))
    C_H = ord(curses.ascii.ctrl('h'))
    C_N = ord(curses.ascii.ctrl('n'))
    C_P = ord(curses.ascii.ctrl('p'))
    C_R = ord(curses.ascii.ctrl('r'))
    C_CARET = ord(curses.ascii.ctrl('^'))

    Up = "ku"
    Down = "kd"
    Left = "kl"
    Right = "kr"

    Home = "kh"
    End = "@7"
    PageUp = "kP"
    PageDown = "kN"

    Backspace = "kb"
