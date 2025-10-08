# Tailscale MagicDNS Fix Guide

## Problem
Tailscale MagicDNS stops working when `/etc/resolv.conf` gets overwritten with manual DNS servers (like Google's 8.8.8.8).

## Symptoms
- `nslookup machine-name.tailnet.ts.net` returns NXDOMAIN
- `/etc/resolv.conf` shows Google DNS servers instead of systemd-resolved
- `tailscale status` shows network is connected but DNS resolution fails

## Root Cause
Something (script, manual edit, etc.) directly overwrote `/etc/resolv.conf` with hardcoded DNS servers, bypassing systemd-resolved's proper DNS routing.

## Diagnosis Commands
```bash
# Check current resolv.conf content
cat /etc/resolv.conf

# Check if it's a symlink (should be)
ls -la /etc/resolv.conf

# Check systemd-resolved DNS configuration
resolvectl status

# Test MagicDNS directly (should work)
nslookup machine-name.tailnet.ts.net 100.100.100.100

# Check when resolv.conf was last modified
stat /etc/resolv.conf
```

## Fix (The Solution)
```bash
# Remove the manually overwritten resolv.conf
sudo rm /etc/resolv.conf

# Restore proper systemd-resolved symlink
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

# Reset Tailscale DNS settings (if needed)
sudo tailscale down && sudo tailscale up --accept-dns=true
```

## Verification
After fix, `/etc/resolv.conf` should show:
- `nameserver 127.0.0.53` (systemd-resolved stub)
- `search tail1da69.ts.net asapllc.com` (includes Tailscale domain)

Test MagicDNS:
```bash
nslookup machine-name.tail1da69.ts.net
# Should now resolve to 100.x.x.x IP
```

## Prevention
- Avoid directly editing `/etc/resolv.conf`
- Use `resolvectl` or NetworkManager for DNS changes
- Check scripts that might hardcode DNS servers

## Technical Notes
- Tailscale DNS (100.100.100.100) is properly configured on tailscale0 interface
- systemd-resolved routes .ts.net queries to Tailscale DNS automatically
- Manual DNS overrides break this intelligent routing

Date: August 6, 2025
Status: ✅ Verified working solution