"""
HAL function identifier and context extractor
"""
import logging
import sys
import inspect
import os
import importlib

from halucinator import hal_log as hal_log_conf
from halucinator import hal_config
from .r2_context_provider import R2ContextProvider

log = logging.getLogger(__name__)
hal_log = hal_log_conf.getHalLogger()

class HandlerClass:  
    def __init__(self, class_name: str, file_path: str):
        self.class_name = class_name
        self.file_path = file_path
        self.handler_functions = []

class HandlerFunction:
    def __init__(self, func_name: str, bp_list: list):
        self.func_name = func_name
        self.bp_list = bp_list

class FrameworkAbstractions:
    def __init__(self):
        self.handlers_classes = []
        self.models = []

class FuncContext:
    def __init__(self, name: str, addr: int):
        self.name = name
        self.addr = addr
        self.disasm_context = None
        self.decomp_context = None

class Extractor:
    def __init__(self, config: hal_config.HalucinatorConfig):
        self.config = config
        self.functions_context = None
        self.framework_abstractions = FrameworkAbstractions()
        mem = self.config.memories.get('flash')
        if mem is not None and hasattr(mem, "base_addr") and hasattr(mem, "file"):
            # Initialize Context Provider
            self.ctx_provider = R2ContextProvider(mem.file, mem.base_addr)
            log.info("Extractor initialized successfully")
        else:       
            log.error("Extractor: Cannot identify firmware information")
            sys.exit(-1)  

    def extract(self):
        self.init_functions_context()
        self.disassemble_functions(self.functions_context)
        self.decompile_functions(self.functions_context)
        self.discover_bp_handlers()
        self.print_handlers()


    def init_functions_context(self):
        self.functions_context = [FuncContext(sym.name, sym.addr) for sym in self.config.symbols]        

    def disassemble_functions(self, func: FuncContext):
        for func in self.functions_context:
            func.disasm_context = self.ctx_provider.analyze_function(func.addr)

    def decompile_functions(self, func: FuncContext):
        for func in self.functions_context:
            func.decomp_context = self.ctx_provider.analyze_function(func.addr, mode="decomp")

    def print_functions_context(self):
        for func in self.functions_context:
            print(f"Function: {func.name} @ 0x{func.addr:x}")
            print("Disassembly Context:")
            print(func.disasm_context)
            print("Decompilation Context:")
            print(func.decomp_context)
            print("--------------------------------------------------")

    def discover_bp_handlers(self):
        handler_root = "src/halucinator/bp_handlers"
        for root, dirs, files in os.walk(handler_root):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    rel_path = os.path.relpath(os.path.join(root, file), "src").replace(os.sep, ".")[:-3]
                    module = importlib.import_module(rel_path)
                    for name, cls in inspect.getmembers(module, inspect.isclass):
                        if 'BPHandler' in [b.__name__ for b in cls.__bases__]:
                            self.framework_abstractions.handlers_classes.append(
                                HandlerClass(name, os.path.join(root, file))
                            )
                            for func_name, func in inspect.getmembers(cls, inspect.isfunction):
                                if hasattr(func, "bp_func_list"):
                                    self.framework_abstractions.handlers_classes[-1].handler_functions.append(
                                        HandlerFunction(func_name, func.bp_func_list)
                                    )
                                elif hasattr(func, "is_bp_handler"):
                                    self.framework_abstractions.handlers_classes[-1].handler_functions.append(
                                        HandlerFunction(func_name, [])
                                    )   

    def print_handlers(self):
        for handler_class in self.framework_abstractions.handlers_classes:
            print(f"Handler Class: {handler_class.class_name} in {handler_class.file_path}")
            for handler_func in handler_class.handler_functions:
                print(f"  Function: {handler_func.func_name} handles breakpoints: {handler_func.bp_list}")                                