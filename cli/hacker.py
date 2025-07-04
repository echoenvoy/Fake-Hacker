#!/usr/bin/env python3
"""
hacker.py — Fake Hacker Terminal (Python CLI edition)
──────────────────────────────────────────────────────
A fully interactive fake hacking terminal.
Runs in your actual terminal with ANSI colors, progress bars, and drama.

Usage:
    python hacker.py
    python hacker.py --target nasa     # auto-run a hack sequence
    python hacker.py --no-boot         # skip the boot animation
"""

import time
import random
import sys
import os
import argparse
import threading
import shutil

# ── ANSI colours ──────────────────────────────────────────────────────────────
class C:
    RESET   = '\033[0m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    # Greens
    G       = '\033[92m'   # bright green
    GD      = '\033[32m'   # dim green
    # Others
    CYAN    = '\033[96m'
    AMBER   = '\033[93m'
    RED     = '\033[91m'
    WHITE   = '\033[97m'
    MUTED   = '\033[90m'

def c(color, text):
    return f"{color}{text}{C.RESET}"

def g(text):     return c(C.G, text)
def gd(text):    return c(C.GD, text)
def cy(text):    return c(C.CYAN, text)
def am(text):    return c(C.AMBER, text)
def rd(text):    return c(C.RED, text)
def mu(text):    return c(C.MUTED, text)
def w(text):     return c(C.WHITE, text)

# ── Terminal width ─────────────────────────────────────────────────────────────
def tw():
    return shutil.get_terminal_size((80, 24)).columns

# ── Printing helpers ───────────────────────────────────────────────────────────
def println(text='', delay=0):
    if delay:
        time.sleep(delay)
    print(text)

def typeprint(text, speed=0.025, newline=True):
    """Print one character at a time."""
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed + random.uniform(0, 0.015))
    if newline:
        print()

def sleep(ms):
    time.sleep(ms / 1000)

def rnd(a, b):
    return random.randint(a, b)

def prompt_str():
    return f"{rd('root')}@{g('darknet')}:{am('~')}# "

def show_prompt(cmd=None):
    if cmd:
        print(prompt_str() + g(cmd))
    else:
        sys.stdout.write(prompt_str())
        sys.stdout.flush()

def divider(char='─', color=C.GD):
    print(f"{color}{char * min(tw(), 72)}{C.RESET}")

def blank():
    print()

# ── Progress bar ───────────────────────────────────────────────────────────────
def progress(label, duration=1.2, color=C.G, width=30):
    sys.stdout.write(f"  {color}{label}{C.RESET}  [")
    sys.stdout.flush()
    steps = width
    step_time = duration / steps
    for i in range(steps):
        time.sleep(step_time)
        sys.stdout.write(f"{color}█{C.RESET}")
        sys.stdout.flush()
    print(f"] {g('100%  ✓')}")

# ── Hex dump ───────────────────────────────────────────────────────────────────
def hex_dump(lines=5, delay=0.06):
    for i in range(lines):
        addr  = format(i * 16, '08X')
        bytes_row = ' '.join(format(random.randint(0, 255), '02X') for _ in range(16))
        ascii_row = ''.join(
            chr(random.randint(33, 126)) for _ in range(16)
        )
        print(mu(f"  {addr}  {bytes_row}  |{ascii_row}|"))
        time.sleep(delay)

# ── ASCII art logo ─────────────────────────────────────────────────────────────
LOGO = r"""
  ██╗  ██╗ ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗
  ██║  ██║ ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
  ███████║ ███████║███████║██║     █████╔╝ █████╗  ██████╔╝
  ██╔══██║ ╚════██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
  ██║  ██║      ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
  ╚═╝  ╚═╝      ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""

# ── Boot sequence ──────────────────────────────────────────────────────────────
BOOT = [
    (gd('[ SYS  ] Kernel 6.6.8-darknet-x86_64 initialized'),        0.0 ),
    (gd('[ BIOS ] Secure boot: ') + rd('BYPASSED'),                  0.08),
    (gd('[ NET  ] VPN tunnel established — 17 hops anonymized'),     0.08),
    (gd('[ CRYPT] Tor circuit built: RU → DE → JP → US'),            0.09),
    (gd('[ CRYPT] AES-256 session keys generated'),                  0.08),
    (gd('[ SCAN ] Shodan feed connected'),                           0.09),
    (g ('[ OK   ] darknet shell ready'),                             0.12),
]

def boot():
    os.system('cls' if os.name == 'nt' else 'clear')
    for line, delay in BOOT:
        time.sleep(delay)
        println(line)

    println()
    for line in LOGO.strip('\n').split('\n'):
        println(g(line))
        time.sleep(0.04)

    println()
    println(cy("  Welcome back, root. 3 new targets available."))
    println(mu("  Type  help  to see available commands."))
    println()

# ── Commands ───────────────────────────────────────────────────────────────────

def cmd_help(args):
    blank()
    cmds = [
        ('hack <target>',      'Initiate a full hacking sequence'),
        ('scan <ip>',          'Port scan a target'),
        ('decrypt <file>',     'Decrypt an intercepted file'),
        ('trace <signal>',     'Trace a network signal to origin'),
        ('ssh <host>',         'Connect to a remote server'),
        ('whoami',             'Print current user info'),
        ('status',             'Show system status'),
        ('ls',                 'List directory contents'),
        ('matrix',             'Activate matrix mode'),
        ('nmap <target>',      'Alias for scan'),
        ('crack <hash>',       'Crack a password hash'),
        ('clear',              'Clear the terminal'),
        ('exit / quit',        'Exit the terminal'),
        ('help',               'Show this message'),
    ]
    divider()
    println(cy(f"  {'COMMAND':<24} DESCRIPTION"))
    divider()
    for cmd, desc in cmds:
        println(f"  {cy(cmd):<33} {mu('—')} {w(desc)}")
    divider()
    blank()


def cmd_hack(args):
    target = (args or 'nasa').strip().lower()
    TARGET = target.upper()

    sequences = {
        'nasa': [
            (g,  '[*] Establishing connection to NASA Goddard mainframe...'),
            (g,  '[+] Bypassing firewall layer 1/3... done'),
            (g,  '[+] Bypassing firewall layer 2/3... done'),
            (g,  '[+] Bypassing firewall layer 3/3... done'),
            (w,  '[*] Accessing satellite uplink array...'),
            (w,  '[*] Decrypting Pentagon subnet...'),
            (am, '[!] ALERT: Intrusion detection triggered — spoofing MAC'),
            (g,  '[+] MAC spoofed successfully. Continuing...'),
            (w,  '[*] Downloading astronaut memes...'),
            (w,  '[*] Downloading moon landing footage (unedited)...'),
            (g,  '[+] Exfiltrating 47,832 classified documents...'),
            (g,  '[+] HACK COMPLETE. NASA has been compromised. 😎'),
        ],
        'pentagon': [
            (w,  '[*] Routing through 12 anonymous proxies...'),
            (w,  '[*] Accessing Pentagon secure intranet...'),
            (am, '[!] BIOMETRIC WALL DETECTED — deploying deepfake bypass'),
            (g,  '[+] Biometrics bypassed. Inside the network.'),
            (w,  '[*] Scanning classified folder structure...'),
            (cy, '[*] Found: /TOP_SECRET/aliens/roswell_real.mp4'),
            (cy, '[*] Found: /TOP_SECRET/JFK/who_did_it.txt'),
            (w,  '[*] Downloading everything...'),
            (g,  '[+] Download complete. 2.3 TB exfiltrated.'),
            (g,  '[+] HACK COMPLETE. Pentagon has been compromised. 😎'),
        ],
        'google': [
            (w,  '[*] Connecting to Google datacenter, The Dalles OR...'),
            (w,  '[*] Exploiting CVE-2024-0001 zero-day...'),
            (g,  '[+] Root access to search index granted.'),
            (cy, '[*] Your search history loading...'),
            (mu, '    > "how to look cool at parties"'),
            (mu, '    > "is cereal a soup"'),
            (mu, '    > "can dolphins be trusted"'),
            (am, '[!] Looks like we already know everything about you.'),
            (g,  '[+] HACK COMPLETE. Google is now yours. 😎'),
        ],
    }

    steps = sequences.get(target, [
        (w,  f'[*] Looking up target: {TARGET}...'),
        (w,  '[*] Running OSINT sweep...'),
        (g,  '[+] Found 3 open ports: 22, 80, 8443'),
        (w,  '[*] Deploying exploit payload...'),
        (g,  f'[+] Shell obtained: {target}@victim:~$'),
        (w,  '[*] Elevating privileges...'),
        (g,  '[+] root access granted.'),
        (w,  '[*] Downloading everything interesting...'),
        (g,  f'[+] HACK COMPLETE. {TARGET} has been compromised. 😎'),
    ])

    blank()
    typeprint(cy(f"Initiating hack sequence on target: {TARGET}"), speed=0.03)
    blank()
    progress('Establishing encrypted tunnel', 0.9)
    blank()

    delays = [0.6, 0.5, 0.45, 0.45, 0.7, 0.65, 0.6, 0.5, 0.55, 0.6, 0.6, 0.8]
    for i, (color_fn, text) in enumerate(steps):
        time.sleep(delays[i] if i < len(delays) else 0.5)
        println(f"  {color_fn(text)}")

    blank()
    progress('Covering tracks             ', 1.4, C.AMBER)
    blank()
    println(g("  [+] All traces erased. You were never here."))
    hex_dump(3, 0.04)
    blank()


def cmd_scan(args):
    ip = args or f"{rnd(1,255)}.{rnd(0,255)}.{rnd(0,255)}.{rnd(1,255)}"
    blank()
    typeprint(f"Starting Nmap 7.94 scan on {ip}...", speed=0.025)
    time.sleep(0.2)
    progress('Host discovery            ', 0.7)
    blank()

    all_ports = [
        (22,   'ssh',   'OpenSSH 9.1'),
        (80,   'http',  'nginx 1.25.3'),
        (443,  'https', 'nginx 1.25.3'),
        (3306, 'mysql', 'MySQL 8.0.35'),
        (8080, 'http',  'Apache Tomcat 10.1'),
        (21,   'ftp',   'vsftpd 3.0.5'),
    ]
    ports = [p for p in all_ports if random.random() > 0.35]

    println(cy(f"  {'PORT':<9} {'STATE':<7} {'SERVICE':<10} VERSION"))
    println(mu('  ' + '─' * 56))
    for port, svc, version in ports:
        println(f"  {g(str(port)):<18} {'open':<7} {svc:<10} {mu(version)}")
        time.sleep(0.12)

    blank()
    println(g(f"  [+] {len(ports)} open port(s) found. {rnd(1,5)} known CVEs detected."))
    if ports:
        println(am(f"  [!] Recommended exploits: EternalBlue, Log4Shell, Dirty COW"))
    blank()


def cmd_decrypt(args):
    fname = args or 'intercepted_comms.enc'
    blank()
    println(w(f"  [*] Target: {fname}"))
    println(w(  "  [*] Detecting cipher..."))
    time.sleep(0.6)
    println(g(  "  [+] Detected: AES-256-CBC with PBKDF2 key derivation"))
    time.sleep(0.4)
    progress('Brute-forcing IV          ', 1.0)
    progress('Deriving master key       ', 1.6, C.CYAN)
    time.sleep(0.3)
    println(g(  "  [+] KEY FOUND: 4f3a9b2e1c8d7f56"))
    blank()
    println(cy( "  [*] Decrypted contents:"))
    hex_dump(4, 0.05)
    println(g(f"  [+] Plaintext saved to /tmp/decrypted_{int(time.time())}.txt"))
    blank()


def cmd_trace(args):
    target = args or 'unknown-signal'
    blank()
    typeprint(w(f"  [*] Tracing signal origin: {target}"), speed=0.025)
    blank()

    hops = [
        ('10.0.0.1',       'Local gateway',            'US', '1ms'   ),
        ('185.220.101.47', 'Tor exit node #1',          'DE', '43ms'  ),
        ('45.33.32.156',   'Relay node',                'JP', '127ms' ),
        ('77.88.55.77',    'Unknown — no RDNS',         'RU', '189ms' ),
        ('104.18.0.0',     'CloudFlare edge',           'FR', '201ms' ),
        (f'{rnd(1,255)}.{rnd(0,255)}.0.1', 'Origin host', 'CN', '247ms'),
    ]

    for i, (ip, label, country, lat) in enumerate(hops):
        println(f"  {mu(str(i+1)):<5} {g(ip):<22} [{cy(country)}]  {w(label):<30} {mu(lat)}")
        time.sleep(0.28)

    blank()
    println(g(f"  [+] Signal traced to: {hops[-1][1]} ({hops[-1][2]})"))
    println(am(f"  [!] Coordinates locked: {random.uniform(-90,90):.4f}°N, {random.uniform(-180,180):.4f}°E"))
    blank()


def cmd_whoami(args):
    blank()
    println(cy("  uid=0(root) gid=0(root) groups=0(root),27(sudo),1337(h4x0r)"))
    println(am("  clearance:    ULTRA TOP SECRET"))
    println(rd("  threat level: CRITICAL"))
    println(w( "  reputation:   Interpol Most Wanted #4"))
    blank()


def cmd_status(args):
    blank()
    divider('━')
    println(cy(f"  {'SYSTEM STATUS':^68}"))
    divider('━')
    blank()
    rows = [
        ('VPN',        'ACTIVE — 17 hops',           g),
        ('TOR',        'ACTIVE — circuit rebuilt',    g),
        ('FIREWALL',   'BYPASSED',                    am),
        ('ANTIVIRUS',  'DISABLED (obviously)',         rd),
        ('ENCRYPTION', 'AES-256 / ChaCha20-Poly1305', g),
        ('UPTIME',     f'{rnd(1,99)}d {rnd(0,23)}h {rnd(0,59)}m', mu),
        ('TARGETS',    '3 queued / 14 compromised',   g),
        ('FBI THREAT', 'ELEVATED 🚔',                 am),
    ]
    for k, v, cfn in rows:
        println(f"  {mu(k):<16} {cfn(v)}")
        time.sleep(0.08)
    blank()
    divider('━')
    blank()


def cmd_ls(args):
    blank()
    files = [
        ('drwxr-xr-x', 'root', '4096',   'exploits/',              cy),
        ('drwxr-xr-x', 'root', '4096',   'stolen_data/',           cy),
        ('-rwxr-xr-x', 'root', '102400', 'zero_day_exploit.py',    g),
        ('-rw-r--r--', 'root', '2048',   'pentagon_login.txt',     w),
        ('-rw-r--r--', 'root', '819200', 'nsa_secrets.tar.gz',     w),
        ('-rwxr-xr-x', 'root', '4096',   'cover_tracks.sh',        g),
        ('-rw-r--r--', 'root', '1024',   '.bash_history',           mu),
        ('-rwxr-xr-x', 'root', '8192',   'tunnel.sh',              g),
    ]
    println(mu(f"  total {len(files) * 8}"))
    for perm, usr, size, name, cfn in files:
        println(f"  {mu(perm)}  {mu(usr):<6} {mu(usr):<6} {mu(size.rjust(8))}  {cfn(name)}")
        time.sleep(0.05)
    blank()


def cmd_ssh(args):
    host = args or 'target.darknet.onion'
    blank()
    typeprint(w(f"  Connecting to {host}..."), speed=0.03)
    time.sleep(0.5)
    println(mu("  [*] Negotiating SSH-2.0-OpenSSH_9.1"))
    time.sleep(0.4)
    println(g( "  [+] Host key accepted (Ed25519)"))
    time.sleep(0.3)
    println(g( "  [+] Authentication successful"))
    blank()
    println(mu(f"  Last login: Wed Jan 01 00:00:00 2025"))
    blank()
    println(g(f"  root@{host}:~# _"))
    blank()


def cmd_matrix(args):
    blank()
    typeprint(cy("  Activating matrix mode..."), speed=0.04)
    time.sleep(0.3)
    chars = 'アイウエオカキクケコサシスセソタチツテトナニヌネノ0123456789ABCDEF日本語中'
    for row in range(10):
        line = ''.join(random.choice(chars) for _ in range(min(tw()-4, 70)))
        clr = [C.G, C.GD, C.MUTED][min(row // 4, 2)]
        println(f"  {clr}{line}{C.RESET}")
        time.sleep(0.07)
    blank()
    println(cy("  You are The One."))
    blank()


def cmd_crack(args):
    hash_val = args or 'e3b0c44298fc1c14'
    blank()
    println(w(f"  [*] Hash: {hash_val}"))
    println(w(  "  [*] Detecting hash type..."))
    time.sleep(0.5)
    println(g(  "  [+] Detected: SHA-1"))
    time.sleep(0.3)
    println(w(  "  [*] Loading rockyou.txt (14,341,564 entries)..."))
    progress('Dictionary attack         ', 1.2)
    time.sleep(0.2)
    println(am( "  [-] Wordlist exhausted. Switching to brute-force..."))
    progress('Brute force (6-char)      ', 1.8, C.AMBER)
    passwords = ['hunter2','p@ssw0rd','letmein','123456','qwerty','iloveyou','admin','monkey']
    time.sleep(0.3)
    println(g(f"  [+] CRACKED: {random.choice(passwords)}"))
    blank()


def cmd_clear(args):
    os.system('cls' if os.name == 'nt' else 'clear')


COMMAND_MAP = {
    'help':    cmd_help,
    'hack':    cmd_hack,
    'scan':    cmd_scan,
    'nmap':    cmd_scan,
    'decrypt': cmd_decrypt,
    'trace':   cmd_trace,
    'ssh':     cmd_ssh,
    'whoami':  cmd_whoami,
    'status':  cmd_status,
    'ls':      cmd_ls,
    'dir':     cmd_ls,
    'matrix':  cmd_matrix,
    'crack':   cmd_crack,
    'clear':   cmd_clear,
}

# ── REPL ───────────────────────────────────────────────────────────────────────
def repl():
    while True:
        try:
            show_prompt()
            raw = input().strip()
        except (EOFError, KeyboardInterrupt):
            blank()
            println(am("  [!] Session terminated. Clearing logs..."))
            time.sleep(0.4)
            println(g("  [+] Done. You were never here."))
            blank()
            sys.exit(0)

        if not raw:
            continue

        parts = raw.split(None, 1)
        cmd   = parts[0].lower()
        args  = parts[1] if len(parts) > 1 else None

        if cmd in ('exit', 'quit', 'q'):
            blank()
            println(am("  [!] Disconnecting..."))
            time.sleep(0.3)
            println(g("  [+] Logs wiped. Goodbye."))
            blank()
            sys.exit(0)

        if cmd in COMMAND_MAP:
            try:
                COMMAND_MAP[cmd](args)
            except KeyboardInterrupt:
                blank()
                println(rd("  [!] Command interrupted."))
                blank()
        else:
            blank()
            println(rd(f"  bash: {cmd}: command not found"))
            println(mu("  Try 'help' to see available commands."))
            blank()


# ── Entry point ────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description='Fake Hacker Terminal — looks very illegal, is completely harmless.'
    )
    parser.add_argument('--target',  '-t', help='Auto-run: hack <target>')
    parser.add_argument('--no-boot', '-n', action='store_true', help='Skip boot animation')
    args = parser.parse_args()

    if not args.no_boot:
        boot()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        println(g(LOGO))

    if args.target:
        show_prompt(f"hack {args.target}")
        cmd_hack(args.target)

    repl()


if __name__ == '__main__':
    main()
