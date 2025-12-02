from argparse import ArgumentParser
import logging
from multiprocessing import Lock
import sys
import argparse

from halucinator import hal_log, hal_config
from halucinator.main import emulate_binary
from .pipeline.pipeline import Pipeline


log = logging.getLogger(__name__)
hal_log.setLogConfig()


def main():
    """
    HaLLM Main
    """
    parser = ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        action="append",
        required=True,
        help="Config file(s) used to run emulation files are "
        "appended to each other with later files taking precedence",
    )
    parser.add_argument(
        "-s",
        "--symbols",
        action="append",
        default=[],
        help="CSV file with each row having symbol, first_addr, last_addr",
    )
    parser.add_argument(
        "--log_blocks",
        default=False,
        const=True,
        nargs="?",
        help="Enables QEMU's logging of basic blocks, "
        "options [irq, regs, exec, trace, trace-nochain]",
    )
    parser.add_argument(
        "--singlestep",
        default=False,
        const=True,
        nargs="?",
        help="Enables QEMU single stepping instructions",
    )
    parser.add_argument(
        "-n",
        "--name",
        default="HALucinator",
        help="Name of target for avatar, used for logging",
    )
    parser.add_argument(
        "-r",
        "--rx_port",
        default=5555,
        type=int,
        help="Port number to receive zmq messages for IO on",
    )
    parser.add_argument(
        "-t",
        "--tx_port",
        default=5556,
        type=int,
        help="Port number to send IO messages via zmq",
    )
    parser.add_argument("-p", "--gdb_port", default=1234, type=int, help="GDB_Port")
    parser.add_argument(
        "-d",
        "--gdb_server_port",
        default=None,
        type=int,
        help="Port to run GDB Server port",
    )
    parser.add_argument(
        "-e", "--elf", default=None, help="Elf file, required to use recorder"
    )
    parser.add_argument(
        "--print_qemu_command",
        action="store_true",
        default=None,
        help="Just print the QEMU Command",
    )
    parser.add_argument(
        "-q",
        "--qemu_args",
        nargs=argparse.REMAINDER,
        default=[],
        help="Additional arguments for QEMU",
    )

    args = parser.parse_args()

    # Build configuration
    config = hal_config.HalucinatorConfig()
    for conf_file in args.config:
        log.info("Parsing config file: %s", conf_file)
        config.add_yaml(conf_file)

    for csv_file in args.symbols:
        log.info("Parsing csv symbol file: %s", csv_file)
        config.add_csv_symbols(csv_file)

    if not config.prepare_and_validate():
        log.error("Config invalid")
        sys.exit(-1)

    if config.elf_program is not None:
        args.qemu_args.append(f"-device loader,file={config.elf_program.elf_filename}")

    qemu_args = None
    if args.qemu_args:
        qemu_args = " ".join(args.qemu_args)

    # HaLLM Pipeline start
    hallm_pipeline = Pipeline(config)
    hallm_pipeline.run()

    '''
    emulate_binary(
        config,
        args.name,
        args.log_blocks,
        args.rx_port,
        args.tx_port,
        elf_file=args.elf,
        gdb_port=args.gdb_port,
        singlestep=args.singlestep,
        qemu_args=qemu_args,
        gdb_server_port=args.gdb_server_port,
        print_qemu_command=args.print_qemu_command,
    )
    '''


if __name__ == "__main__":
    main()
