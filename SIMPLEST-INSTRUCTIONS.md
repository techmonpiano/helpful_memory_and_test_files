# SIMPLEST POSSIBLE SSH INSTRUCTIONS

## **🎯 For Connecting to Partsfortechs:**

```
"Create zencart SSH session using the automation script"
```

**That's it!** Claude should automatically:
1. ✅ Run the script
2. ✅ Execute the generated commands  
3. ✅ Return working PID

---

## **📋 Alternative Phrasing:**

```
"Set up automated SSH to zencart"
```

```
"Connect to zencart using the one-command script"
```

```
"Create SSH session for zencart server"
```

---

## **🤖 What Claude Should Do Automatically:**

1. **Run**: `python3 ~/shawndev1/helpful_memory_and_test_files/one-command-ssh.py zencart`
2. **See the generated commands**
3. **Execute them immediately** (no prompting needed)
4. **Return the working PID**

---

## **🔧 Why We Can't Eliminate Steps Completely:**

**Technical Limitation**: Only the MCP client (Claude) can call `start_process()` and get a PID that works with `interact_with_process()`. Scripts cannot directly create MCP-managed processes.

**So the minimal automation is:**
- Script generates exact commands
- Claude auto-executes them
- Returns working PID

---

## **✅ Expected Result:**

After saying "Create zencart SSH session", you should get:

```
✅ SSH Session Created!
🆔 PID: 12345
🎯 Ready for use: interact_with_process(12345, "commands", timeout_ms=8000)
```

---

**This is as automated as possible given MCP architecture constraints!**
