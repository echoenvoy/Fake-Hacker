# Fake Hacker Terminal

Looks extremely illegal. Is completely harmless. Great for impressing people who don't know how computers work.

Two versions included:
- **`web/`** — a full browser terminal (zero dependencies, just open the HTML file)
- **`cli/`** — a Python terminal app that runs in your actual terminal

---

## Quick start

### Web version

Just open `web/index.html` in any browser. That's it. No server needed, no npm install, nothing.

```
open web/index.html
```

### Python CLI version

```bash
cd cli
python hacker.py
```

No dependencies. Uses only the Python standard library.

```bash
# Auto-run a hack on startup
python hacker.py --target nasa
python hacker.py --target pentagon
python hacker.py --target google

# Skip the boot sequence
python hacker.py --no-boot

# Combine
python hacker.py --target nasa --no-boot
```

---

## Available commands

Both versions support the same command set:

| Command | What it does |
|---|---|
| `hack <target>` | Full hacking sequence with progress bars and drama |
| `scan <ip>` | Port scan with fake open ports and CVEs |
| `decrypt <file>` | "Decrypt" an intercepted file with hex dump output |
| `trace <signal>` | Hop-by-hop signal trace to a fake origin |
| `ssh <host>` | "Connect" to a remote server |
| `whoami` | Print your terrifying user info |
| `status` | System status panel |
| `ls` | Directory listing full of suspicious files |
| `matrix` | You know what this does |
| `nmap <target>` | Alias for scan |
| `crack <hash>` | Crack a password hash with brute force drama |
| `clear` | Clear the terminal |
| `exit` / `quit` | Dramatic exit with log-wiping message |

### Special hack targets

`hack nasa`, `hack pentagon`, and `hack google` have unique hand-written sequences.
Any other target gets a generic (still dramatic) sequence.

---

## Project structure

```
fake-hacker/
├── web/
│   └── index.html      # Full browser terminal, zero dependencies
├── cli/
│   └── hacker.py       # Python CLI terminal, zero dependencies
└── README.md
```

---

## Web terminal features

- **CRT monitor aesthetic** — scanlines, vignette, screen glow
- **Glitch effect** on the title logo (random, subtle)
- **Custom cursor** — crosshair follows your mouse
- **Typewriter effect** for dramatic commands
- **Animated progress bars** with colour changes
- **Fake hex dumps** that look like real memory output  
- **Live stats** (CPU, MEM, NET, clock) in the top bar that update every 1.2s
- **Command history** — use ↑/↓ arrows to navigate
- **`VT323` + `Share Tech Mono`** fonts for that authentic hacker look

## Python CLI features

- **ANSI colours** throughout — green/amber/red/cyan like a real terminal
- **Typewriter printing** with randomised character timing
- **Progress bars** drawn with block characters
- **Fake hex dumps** 
- **Command history** via Python's input (Ctrl+R works too)
- **Ctrl+C** exits gracefully with a "logs wiped" message
- No dependencies — works on Python 3.6+

---

## Tips

- Walk up to someone's computer, open `index.html`, go fullscreen (F11), leave.
- Set `hacker.py` as your `.bashrc` default shell on a shared computer.
- Run it during a call and pretend not to notice.

---

## License

MIT. Not responsible for any confused coworkers, worried parents, or called bluffs.
