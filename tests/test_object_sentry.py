import pytest
from object_sentry import detect_hardware_accelerators, select_optimal_accelerator, benchmark_accelerator, fallback_to_cpu

def test_detect_hardware_accelerators():
    accelerators = detect_hardware_accelerators()
    assert len(accelerators) == 3
    assert accelerators[0].name == 'GPU'
    assert accelerators[1].name == 'TPU'
    assert accelerators[2].name == 'CPU'

def test_select_optimal_accelerator():
    accelerators = detect_hardware_accelerators()
    optimal_accelerator = select_optimal_accelerator(accelerators)
    assert optimal_accelerator.name == 'TPU'
    assert optimal_accelerator.latency == 0.05

def test_benchmark_accelerator():
    accelerators = detect_hardware_accelerators()
    optimal_accelerator = select_optimal_accelerator(accelerators)
    latency = benchmark_accelerator(optimal_accelerator)
    assert latency == 0.05

def test_fallback_to_cpu():
    cpu_accelerator = fallback_to_cpu()
    assert cpu_accelerator.name == 'CPU'
    assert cpu_accelerator.latency == 1.0

def test_benchmark_suite():
    accelerators = detect_hardware_accelerators()
    optimal_accelerator = select_optimal_accelerator(accelerators)
    latency = benchmark_accelerator(optimal_accelerator)
    cpu_latency = benchmark_accelerator(fallback_to_cpu())
    assert (cpu_latency - latency) / cpu_latency >= 0.3
