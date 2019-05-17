import atexit
import subprocess
from subprocess import DEVNULL
from tempfile import NamedTemporaryFile
from typing import Tuple

from pypacker import interceptor

from scapy.layers.inet import IP

from Controller import Controller
from PacketSub.Packet import Packet
from scapy.all import raw

def verdict_callback(ll_data, ll_proto_id, data: bytes, Controller) -> Tuple[bytes, int]:
    iptable = IPTable()
    if iptable.isInterceptorOn():
        print(IP(data).show(dump=True))
        h = IP(data)

        Packet(h, iptable.frame, Controller, False)
        iptable.frame += 1

        return data, interceptor.NF_ACCEPT
    else:
        return data, interceptor.NF_ACCEPT


class _IPTable:
    _instance = None

    def __init__(self):
        self.proxy_on = False
        self.interceptor_on = False
        self.interceptor = interceptor.Interceptor()

        # Running this ensures iptables-save returns the correct output
        subprocess.run(['iptables', '-L'], stdout=DEVNULL, stderr=DEVNULL)

    def toggleProxy(self, controller: Controller):
        """
        Toggles proxy on or off. Can only be toggled off if the interceptor is
        off. Restores previous iptables config when toggled off.

        @requires (* Called only from the GUI *)
        @requires not self.isInterceptorOn()

        @ensures self.isProxyOn() is not \\old(self.isProxyOn())
        @ensures (* When turning on the proxy, the \\old(iptables config) is
            backed up *)
        @ensures (* When turning off the proxy, the iptables config is restored
            with previously backed up rules *)
        """
        if not self.proxy_on:
            # Create temporary file to store iptables rules.
            self.iptables_rules = NamedTemporaryFile(
                suffix='iptables.rules.old'
            )

            # Save rules in temporary file
            subprocess.run(['iptables-save'], stdout=self.iptables_rules)

            # Add NFQUEUE iptables rule
            subprocess.run(
                [
                    "iptables",
                    "-I", "OUTPUT", "1",  # Insert rule  at beginning of INPUT
                    "-j", "NFQUEUE",  # Send input to NFQUEUE
                ]
            )

            # Start interceptor
            self.interceptor.start(verdict_callback, queue_ids=[0], ctx=controller)
            self.frame = 1

        else:
            # Seek to beginning of temporary file to read saved rules
            self.iptables_rules.seek(0)

            # Restore iptables rules to previous state
            subprocess.run(['iptables-restore'], stdin=self.iptables_rules)

            # Close and delete temporary file and delete its reference
            self.iptables_rules.close()
            del self.iptables_rules

            # Stop interceptor
            self.interceptor.stop()

        # Toggle proxy state
        self.proxy_on = not self.proxy_on

    def isProxyOn(self) -> bool:
        """
        Returns current proxy state.

        @ensures (* If NFQueue is proxying or intercepting packets, returns
            True *)
        @ensures (* if self.toggleProxy() has never been called,
            returns False *)
        """
        return self.proxy_on

    def toggleInterceptor(self) -> bool:
        """
        Toggles interceptor on or off. Can only be toggled off if the proxy is
        on.

        @requires (* Called only from the GUI *)
        @requires self.isProxyOn()

        @ensures self.isInterceptorOn() is not \\old(self.isInterceptorOn())
        @ensures (* When turning on the interceptor, packets are no longer
            being automatically forwarded. Instead, incoming packets will
            be added to the PacketList *)
        @ensures (* When turning off the interceptor, packets are automatically
            forwarded *)
        """
        # TODO: Implement packet interception
        self.interceptor_on = not self.interceptor_on

    def isInterceptorOn(self) -> bool:
        """
        Returns current interceptor state.

        @ensures (* If NFQueue intercepting packets, returns True *)
        @ensures (* if self.toggleInterceptor() has never been called,
            returns False *)
        """
        return self.interceptor_on


def IPTable() -> _IPTable:
    """
    Returns IPTable as a singleton
    """
    if _IPTable._instance == None:
        _IPTable._instance = _IPTable()
    return _IPTable._instance


def restore_proxy():
    """
    Callback so that when NTPS exits early, proxy is disabled and iptables
    rules are restored
    """
    iptable = IPTable()
    if iptable.isInterceptorOn():
        iptable.toggleInterceptor()
    if iptable.isProxyOn():
        iptable.toggleProxy(None)

# Runs callback at end
atexit.register(restore_proxy)


if __name__ == '__main__':
    def print_iptables_state():
        iptable = IPTable()
        print(
            f"###### proxy = {iptable.isProxyOn()}",
            f"iceptor = {iptable.isInterceptorOn()} ######",
            sep='\t',
        )
        subprocess.run(['iptables', '-L'])
        print('\n')

    # A simple "tester"
    iptable = IPTable()
    print_iptables_state()

    iptable.toggleProxy(None)
    print_iptables_state()

    iptable.toggleInterceptor()
    print_iptables_state()

    iptable.toggleInterceptor()
    print_iptables_state()

    iptable.toggleProxy(None)
    print_iptables_state()
