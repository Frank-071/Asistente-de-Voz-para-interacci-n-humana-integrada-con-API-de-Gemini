import win32com.client as win32
cat = win32.Dispatch("SAPI.SpObjectTokenCategory")
cat.SetId(r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\AudioOutput", False)
print("Salidas de audio SAPI:")
for t in cat.EnumerateTokens():
    print("-", t.GetDescription())