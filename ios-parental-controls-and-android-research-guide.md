# iOS Parental Controls & Android-on-iPhone Research Guide

## Table of Contents
1. [Android on iPhone Research Summary](#android-on-iphone-research-summary)
2. [iOS 15+ Parental Controls Guide](#ios-15-parental-controls-guide)
3. [Implementation Steps](#implementation-steps)
4. [Troubleshooting & Considerations](#troubleshooting--considerations)

---

## Android on iPhone Research Summary

### Project Sandcastle (2020-Present)

**Status**: Abandoned since March 2020, community fixes available but limited

**Compatibility**: 
- iPhone 7, iPhone 7 Plus, iPod Touch 7th generation only
- Requires checkra1n jailbreak

**Major Limitations**:
- ❌ No audio output
- ❌ No cellular connectivity  
- ❌ No Bluetooth
- ❌ No camera functionality
- ❌ No GPU acceleration
- ❌ No Google Play Services
- ❌ Read-only storage (experimental APFS support)
- ❌ Non-persistent (loses everything on reboot)

**Reality Check**: Technical demonstration only, not viable for daily use.

### iDroid Project (Historical)

**Status**: Dead and abandoned - described as "extremely buggy" and "not stable"

**Compatibility**: 
- Original iPhone through iPhone 6 Plus (older hardware only)
- Required jailbreak

**User Experience**:
- Sluggish performance due to insufficient RAM/CPU
- Only basic phone functions worked
- Not recommended for any practical use

### checkra1n Jailbreak (Current Status 2023-2024)

**Compatibility**:
- iPhone 5s through iPhone X only
- iOS 12.0 through iOS 14.8.1
- **Cannot work on iPhone 11+ (no checkm8 exploit)**
- **iOS 18 will end checkra1n compatibility entirely**

**Platform Support**:
- macOS and Linux only
- Windows version never materialized despite promises

**Important Notes**:
- Semi-tethered (requires re-jailbreak after each reboot)
- Legal concerns: Apple's license prohibits alternative OSes
- Security risks associated with jailbreaking

### Bottom Line on Android-on-iPhone

- **Not recommended** for any practical use
- Limited to very old hardware with major functionality gaps
- Projects largely abandoned by developers
- Becoming impossible on newer hardware
- Legal and security implications

---

## iOS 15+ Parental Controls Guide

### Overview

iOS 15 and later versions include comprehensive built-in parental controls through **Screen Time** and **Content & Privacy Restrictions**. No jailbreaking or third-party apps required.

### Method 1: Screen Time & Content Restrictions

#### Initial Setup

1. **Access Screen Time**:
   - Go to **Settings > Screen Time**
   - Choose "This is My Child's [Device]"

2. **Set Screen Time Passcode**:
   - Tap **Use Screen Time Passcode**
   - Create a secure passcode (prevents child from changing settings)

3. **Enable Content & Privacy Restrictions**:
   - Tap **Content & Privacy Restrictions**
   - Enter Screen Time passcode
   - Turn on Content & Privacy Restrictions

#### App Control Options

**Allowed Apps** (Hide/Show Apps):
- Navigate to **Content & Privacy Restrictions > Allowed Apps**
- Toggle off apps you want to hide:
  - Safari (web browser)
  - Camera
  - FaceTime
  - iTunes Store
  - App Store
  - Mail
  - And more...

**App Limits** (Time Restrictions):
- Go to **Screen Time > App Limits > Add Limit**
- Select app categories (Social, Games, Entertainment, etc.)
- Set daily time limits or block entirely (set to 1 minute)

**App Store Controls**:
- **Content & Privacy Restrictions > iTunes & App Store Purchases**
- Prevent:
  - Installing apps
  - Deleting apps  
  - In-app purchases
  - App downloads

#### Content Filtering

**Web Content**:
- **Content & Privacy Restrictions > Content Restrictions > Web Content**
- Options:
  - **Unrestricted Access**
  - **Limit Adult Websites** (recommended)
  - **Allowed Websites Only** (whitelist only)

**Age-Appropriate Content**:
- Set ratings for Movies, TV Shows, Books, Apps
- Block explicit music and podcasts
- Restrict Siri web search

### Method 2: Guided Access (Single App Mode)

#### Setup Guided Access

1. **Enable Feature**:
   - Go to **Settings > Accessibility > Guided Access**
   - Turn on Guided Access

2. **Set Passcode**:
   - Tap **Passcode Settings**
   - **Set Guided Access Passcode**
   - Optionally enable Face ID/Touch ID for quicker exit

#### Using Guided Access

1. **Start Session**:
   - Open the desired app
   - Triple-click Home button (iPhone 8-) or Side button (iPhone X+)
   - Circle screen areas to disable (optional)
   - Tap **Start**

2. **End Session**:
   - Triple-click Home/Side button
   - Enter Guided Access passcode
   - Or use Face ID/Touch ID if enabled

#### Guided Access Options

- **Time Limits**: Set session duration with audio alerts
- **Hardware Controls**: Disable volume buttons, motion sensing
- **Touch Areas**: Block specific screen regions
- **Keyboard**: Disable keyboard if not needed

### Method 3: Family Sharing Integration

#### Remote Management

1. **Set Up Family Sharing**:
   - **Settings > Family > Add Family Member**
   - Create child Apple ID if needed

2. **Remote Screen Time Management**:
   - **Settings > Family > [Child's Name] > Screen Time**
   - Manage all restrictions remotely
   - Receive weekly Screen Time reports

#### Ask to Buy Feature

- **Settings > Family > [Child's Name] > Ask to Buy**
- Requires parent approval for:
  - App downloads
  - In-app purchases
  - iTunes purchases

---

## Implementation Steps

### Quick Setup for Basic Protection

1. **Enable Screen Time** with passcode
2. **Hide problematic apps** (Safari, App Store, Camera if needed)
3. **Set web content filtering** to "Limit Adult Websites"
4. **Block app installations** and in-app purchases
5. **Set communication limits** if needed

### Advanced Setup for Strict Control

1. **All basic protections** above
2. **Whitelist-only web access** (Allowed Websites Only)
3. **App limits** for games/social media (1 minute = effectively blocked)
4. **Downtime scheduling** (bedtime restrictions)
5. **Communication limits** (restrict who child can contact)

### Single-App Scenarios

- **Educational apps**: Use Guided Access to lock into learning apps
- **Video watching**: Lock into video apps with disabled controls
- **Games**: Prevent app-switching during gameplay

---

## Troubleshooting & Considerations

### Common Issues

**Screen Time Not Working**:
- Ensure iOS is updated to latest version
- Check that Screen Time passcode is different from device passcode
- Restart device after making changes

**Apps Still Accessible**:
- Hidden apps may still appear in Spotlight search
- Use **Content & Privacy Restrictions > Siri** to disable Siri suggestions
- Check Control Center for app access

**Time Limits Bypassed**:
- Ensure "One More Minute" option is disabled
- Use "Block at Downtime" instead of app limits for stricter control
- Consider Guided Access for foolproof single-app sessions

### Important Security Notes

**Emergency Access**:
- Emergency calling still works even with restrictions
- **Important**: Guided Access disables crash detection and emergency features

**Backup Plans**:
- Always keep Screen Time passcode secure and backed up
- Test restrictions before handing device to child
- Have backup device available for emergencies

### Age-Appropriate Defaults (Under 13)

iOS automatically enables for children under 13:
- Communication Safety (nudity detection)
- Screen Distance warnings
- "Limit Adult Websites" web filtering
- Ask to Buy for purchases

### Best Practices

1. **Start conservative** - easier to relax restrictions than add them later
2. **Regular reviews** - adjust restrictions as child matures
3. **Communication** - explain restrictions to older children
4. **Model behavior** - use Screen Time for yourself too
5. **Balance** - allow age-appropriate freedom and exploration

### Legal and Ethical Considerations

- Respect child's developing privacy needs
- Consider local laws regarding monitoring
- Be transparent about restrictions with older children
- Regular family discussions about digital wellness

---

## Conclusion

iOS 15+ provides robust, built-in parental controls that don't require jailbreaking or third-party apps. The combination of Screen Time restrictions, Guided Access, and Family Sharing offers comprehensive protection suitable for various ages and use cases.

For older devices that can't update to recent iOS versions, the built-in restrictions are still preferable to attempting to install Android, which is impractical and poses security risks.

**Last Updated**: June 2025
**iOS Versions Covered**: iOS 15, iOS 16, iOS 17, iOS 18
**Device Compatibility**: All supported iPhone models