# Tailscale Custom Domains & Pricing Research Session
**Date**: 2025-01-27
**Context**: Small business considering Tailscale for 50 machines with multiple users

## Research Questions
1. How to use custom domains with Tailscale vs CNAME subdomain approach?
2. Pricing for small businesses with up to 50 machines
3. Account sharing policy - can one user subscription be used by multiple people?

## Key Findings

### Custom Domain Options (2024-2025)

#### CNAME Subdomain Approach (Recommended)
- **Method**: Create wildcard CNAME `*.ts.yourdomain.com` → `tail1da69.ts.net`
- **Benefits**:
  - Easy SSL with wildcard certificates
  - No need for individual DNS records
  - Works well with reverse proxies (Traefik/Nginx)
  - Most practical and widely adopted method

#### Custom Domain Limitations
- Native custom domain support is limited
- Tailscale Funnel still requires CNAME records for custom domains
- Direct custom domain mapping isn't fully supported yet

### Pricing Structure (2024-2025)

#### Current Plans
- **Starter**: $6/user/month (~60 devices per user)
- **Premium**: $18/user/month
- **Additional devices**: $0.50 each beyond user allocation

#### For 50 Machines
- 1 user on Starter plan gets 60 devices
- **Single user cost**: ~$72/year for 50 machines
- **BUT**: This violates terms of service (see below)

#### Discounts Available
- 50% off for non-profits and educational institutions
- Existing customers (pre-Feb 2024) keep current pricing until Feb 2025

### Account Sharing Policy - CRITICAL FINDING

#### Explicit Prohibition
**Tailscale's Acceptable Use Policy states**:
> "A Tailscale user account may not be shared or used by multiple individuals."

#### What This Means
- Each person needs their own Tailscale account
- OAuth login (GitHub, Google, etc.) = individual identity
- Sharing credentials between multiple people violates terms

#### Compliant Business Setup
1. Create business tailnet
2. Invite each employee with their own email/OAuth
3. All 50 machines managed centrally
4. Pay per active user who transfers data monthly

### Real Cost for Multiple Users

#### Actual Business Costs
- **5 people using machines**: $30/month ($360/year)
- **10 people using machines**: $60/month ($720/year)
- **Active user billing**: Only pay for users who transfer data each month

## Implementation Recommendations

### For Custom Domains
```bash
# DNS Configuration (recommended)
*.ts.yourbusiness.com CNAME tail1da69.ts.net

# Example usage
server1.ts.yourbusiness.com → accessible only via Tailscale
app.ts.yourbusiness.com → routes to specific service
```

### For Compliant User Setup
1. **Admin creates business tailnet**
2. **Invite users**: Each employee gets invitation to tailnet
3. **Device management**: All 50 machines connect to shared network
4. **Access control**: Use ACLs to control who accesses what

## Technical Architecture

### DNS Resolution Flow
```
user.ts.yourdomain.com → CNAME → device.yourtailnet.ts.net → Tailscale IP
```

### User Authentication
- Each user: Individual OAuth (GitHub/Google/Microsoft)
- Network access: Shared tailnet with role-based permissions
- Billing: Per active user, not per device

## Cost Comparison

| Approach | Monthly Cost | Compliance | Scalability |
|----------|--------------|------------|-------------|
| 1 shared user | $6 | ❌ Violates ToS | ❌ Limited |
| 5 individual users | $30 | ✅ Compliant | ✅ Good |
| 10 individual users | $60 | ✅ Compliant | ✅ Excellent |

## Action Items for Implementation

### Phase 1: Setup
- [ ] Create business Tailscale account
- [ ] Configure DNS with CNAME wildcards
- [ ] Set up SSL certificates for custom domain

### Phase 2: User Management
- [ ] Invite all employees to tailnet
- [ ] Configure ACLs for appropriate access control
- [ ] Document access procedures for team

### Phase 3: Device Integration
- [ ] Install Tailscale on all 50 machines
- [ ] Configure machines with appropriate tags/roles
- [ ] Test connectivity and custom domain resolution

## Important Notes

### Compliance Warning
- **DO NOT** use shared login approach - violates Tailscale ToS
- Each actual human user needs individual account
- Business liable for policy violations

### Technical Considerations
- CNAME approach works immediately
- Wildcard SSL certificates simplify management
- Reverse proxy integration straightforward

### Budget Planning
- Factor in actual number of human users, not devices
- Consider 50% discount if non-profit/educational
- Plan for user growth - pricing scales linearly

## Sources
- Tailscale official documentation (tailscale.com)
- Pricing FAQ and Terms of Service
- Community implementations and best practices
- 2024-2025 pricing updates and policy changes

---
**Session Result**: CNAME subdomain approach recommended for custom domains. Account sharing not permitted - must license each actual user for compliance.