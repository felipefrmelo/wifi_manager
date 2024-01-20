

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Device:
    ip_address: str = field(compare=True)
    mac_address: str = field(compare=True)
    owner: str = field(compare=False, default='unknown')
    blocked: bool = field(compare=False, default=False)
    name: Optional[str] = field(compare=False, default=None)

    def block(self):
        self.blocked = True

    def allow(self):
        self.blocked = False
