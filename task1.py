from typing import List, Dict, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


@dataclass
class PrintGroup:
    jobs: List[PrintJob]
    total_volume: float
    max_print_time: int


def create_print_job(job_dict: Dict) -> PrintJob:
    """Створює об'єкт PrintJob з словника"""
    return PrintJob(
        id=job_dict["id"],
        volume=job_dict["volume"],
        priority=job_dict["priority"],
        print_time=job_dict["print_time"]
    )


def create_printer_constraints(constraints_dict: Dict) -> PrinterConstraints:
    """Створює об'єкт PrinterConstraints з словника"""
    return PrinterConstraints(
        max_volume=constraints_dict["max_volume"],
        max_items=constraints_dict["max_items"]
    )


def can_add_to_group(group: PrintGroup, job: PrintJob, constraints: PrinterConstraints) -> bool:
    """Перевіряє, чи можна додати завдання до групи"""
    new_volume = group.total_volume + job.volume
    new_count = len(group.jobs) + 1
    return (new_volume <= constraints.max_volume and
            new_count <= constraints.max_items)


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """

    jobs = [create_print_job(job) for job in print_jobs]
    printer_constraints = create_printer_constraints(constraints)

    jobs.sort(key=lambda x: x.priority)

    print_order = []
    total_time = 0
    current_group = PrintGroup(jobs=[], total_volume=0, max_print_time=0)

    for job in jobs:
        if can_add_to_group(current_group, job, printer_constraints):
            current_group.jobs.append(job)
            current_group.total_volume += job.volume
            current_group.max_print_time = max(current_group.max_print_time, job.print_time)
            continue

        if current_group.jobs:
            print_order.extend([j.id for j in current_group.jobs])
            total_time += current_group.max_print_time

        current_group = PrintGroup(
            jobs=[job],
            total_volume=job.volume,
            max_print_time=job.print_time
        )

    if current_group.jobs:
        print_order.extend([j.id for j in current_group.jobs])
        total_time += current_group.max_print_time

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

if __name__ == "__main__":
    test_printing_optimization()

