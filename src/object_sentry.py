import json
import platform
import time
from dataclasses import dataclass
from typing import List

@dataclass
class HardwareAccelerator:
    name: str
    latency: float

def detect_hardware_accelerators() -> List[HardwareAccelerator]:
    """Detect available hardware accelerators"""
    accelerators = []
    if platform.system() == 'Linux':
        # Simulate detection of GPUs, TPUs, and CPU resources
        accelerators.append(HardwareAccelerator('GPU', 0.1))
        accelerators.append(HardwareAccelerator('TPU', 0.05))
        accelerators.append(HardwareAccelerator('CPU', 1.0))
    return accelerators

def select_optimal_accelerator(accelerators: List[HardwareAccelerator]) -> HardwareAccelerator:
    """Select the fastest hardware accelerator"""
    return min(accelerators, key=lambda x: x.latency)

def benchmark_accelerator(accelerator: HardwareAccelerator) -> float:
    """Benchmark the selected hardware accelerator"""
    # Simulate benchmarking
    time.sleep(accelerator.latency)
    return accelerator.latency

def fallback_to_cpu() -> HardwareAccelerator:
    """Fallback to CPU inference when no accelerator is present"""
    return HardwareAccelerator('CPU', 1.0)
