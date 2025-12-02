import r2pipe

class R2ContextProvider:
    def __init__(self, firmware_path, base_addr):
        self.firmware_path = firmware_path
        self.base_addr = base_addr

    def analyze_function(self, func_address, mode="disasm"):
        r2 = r2pipe.open(self.firmware_path, flags=["-2", "-m", str(self.base_addr)])  # -2 suppresses warnings
        r2.cmd("e asm.arch=arm")
        r2.cmd("e asm.bits=16")
        r2.cmd(f"s {func_address}")
        r2.cmd("aa")

        if mode == "disasm":
            return r2.cmd("pdf")
        elif mode == "decomp":
            return r2.cmd("pdc")
        else:
            raise ValueError("Invalid mode. Use 'disasm' or 'decomp'.")


