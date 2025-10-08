# C++Builder 2007 Post-Build Event - Copy to Multiple Directories

## Overview
This guide explains how to configure C++Builder 2007 (CodeGear/RAD Studio 2007) to automatically copy built executables to multiple directories using post-build events.

## Setting Up Post-Build Events

### 1. Access Build Events Configuration
- Open your project in C++Builder 2007
- Navigate to: **Project → Options → Build Events**

### 2. Configure Post-Build Commands
In the Post-Build Events section, add commands to copy your executable to multiple directories:

```batch
copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Deploy\Directory1\" /Y
copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Deploy\Directory2\" /Y  
copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "D:\Backup\Builds\" /Y
```

## Available Build Macros

C++Builder 2007 provides several predefined macros for use in build events:

| Macro | Description |
|-------|-------------|
| `$(OUTPUTDIR)` | Output directory path |
| `$(OUTPUTNAME)` | Output file name (without extension) |
| `$(PROJECTDIR)` | Project directory |
| `$(PROJECTNAME)` | Project name |

## Command Examples

### Basic Copy Commands
```batch
copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Deploy\Directory1\" /Y
copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Deploy\Directory2\" /Y
copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "\\NetworkShare\Builds\" /Y
```

### Using XCOPY for More Options
XCOPY provides additional features like subdirectory creation:
```batch
xcopy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Deploy\Directory1\" /Y /F
xcopy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Deploy\Directory2\" /Y /F
```

### Chaining Commands
You can chain multiple commands on one line using `&`:
```batch
copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Dir1\" /Y & copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Dir2\" /Y
```

## Configuration Options

### Post-Build Event Execution
Configure when the post-build event should run:
- **Always**: Executes after every build
- **Target is out of date**: Only executes when project has been modified

### Error Handling
- Enable "Cancel on error" to stop the build process if a copy operation fails
- This helps identify deployment issues immediately

## Command Flags Explained

### Copy Command Flags
- `/Y` - Suppresses confirmation prompt for overwriting existing files

### XCOPY Command Flags
- `/Y` - Suppresses confirmation prompt for overwriting
- `/F` - Displays full source and destination file names while copying

## Best Practices

1. **Always Use Quotes**: Enclose paths in quotes to handle spaces in directory names
   ```batch
   copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Program Files\MyApp\" /Y
   ```

2. **Create Directories First**: Ensure target directories exist before copying
   ```batch
   if not exist "C:\Deploy\Directory1\" mkdir "C:\Deploy\Directory1\"
   copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Deploy\Directory1\" /Y
   ```

3. **Add Timestamp to Copies**: Create versioned backups
   ```batch
   copy "$(OUTPUTDIR)\$(OUTPUTNAME).exe" "C:\Backup\$(OUTPUTNAME)_%date:~-4,4%%date:~-10,2%%date:~-7,2%.exe" /Y
   ```

4. **Copy Additional Files**: Include DLLs or config files
   ```batch
   copy "$(OUTPUTDIR)\*.dll" "C:\Deploy\Directory1\" /Y
   copy "$(PROJECTDIR)\config.ini" "C:\Deploy\Directory1\" /Y
   ```

## Viewing Build Output

- Build event commands and their results are displayed in the **Output pane** of the **Messages View**
- This helps verify that files are being copied correctly
- Check for any error messages if copies fail

## Troubleshooting

### Common Issues and Solutions

1. **"The system cannot find the path specified"**
   - Verify target directories exist
   - Check for typos in directory paths
   - Ensure you have write permissions

2. **"Access is denied"**
   - Check file/folder permissions
   - Ensure target file isn't in use
   - Run IDE as administrator if copying to protected locations

3. **Macros Not Expanding**
   - Verify macro names are spelled correctly
   - Use the Macros list in Build Event Commands dialog to insert them
   - Double-click macro names to insert them automatically

## MSBuild Integration

C++Builder 2007 introduced MSBuild as the build engine:
- Project files changed to XML format (.cbproj extension)
- Build events are stored in the project file
- Compatible with MSBuild command-line tools

## Additional Notes

- Pre-Link events are available only for C++ projects
- DOS commands are supported in build events
- Multiple commands can be entered, one per line
- Commands execute in the order listed
- Build stops if "Cancel on error" is enabled and a command fails

---

*Last Updated: January 2025*
*Applies to: C++Builder 2007, CodeGear RAD Studio 2007*