import time
import pyRAPL

class EnergyMonitor:
    def __init__(self):
        self.total_energy = 0
        self.total_duration = 0
        self.task_energy = {}
        self.task_duration = {}  # Store task durations

        pyRAPL.setup()

    def start_task(self, task_name):
        self.task_energy[task_name] = {'start_time': time.time(), 'total_energy': 0}
        self.measurer = pyRAPL.Measurement(task_name)
        self.measurer.begin()

    def stop_task(self, task_name):
        if task_name in self.task_energy:
            task_data = self.task_energy[task_name]
            duration = time.time() - task_data['start_time']
            self.task_duration[task_name] = duration  # Store task duration
            self.measurer.end()

            energy_consumed = self.measurer.result.pkg[0] / 1_000_000  # Convert µJ to J
            task_data['total_energy'] += energy_consumed
            self.total_energy += energy_consumed
            self.total_duration += duration

            power = energy_consumed / duration
            print(
                f"Stopped task: {task_name}. Duration: {duration:.2f} seconds. "
                f"Energy consumed: {energy_consumed:.6f} Joules. Power: {power:.6f} Watts"
            )

    def get_task_power(self, task_name):
        if task_name in self.task_duration and self.task_duration[task_name] > 0:
            return self.task_energy[task_name]['total_energy'] / self.task_duration[task_name]
        return 0

    def get_total_power(self):
        return self.total_energy / self.total_duration if self.total_duration > 0 else 0

class Task:
    def __init__(self, name, period, execution_time, deadline=None):
        self.name = name
        self.period = period
        self.execution_time = execution_time
        self.deadline = deadline or period

class HybridScheduler:
    def __init__(self):
        self.energy_monitor = EnergyMonitor()
        self.tasks = []
        self.energy_consumption = {}

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Added task: {task.name}")

    def run_round_robin(self, duration, signal):
        print(f"Running round_robin algorithm for {duration} seconds")
        end_time = time.time() + duration
        while time.time() < end_time:
            for task in self.tasks:
                self.energy_monitor.start_task(task.name)
                time.sleep(task.execution_time)
                self.energy_monitor.stop_task(task.name)

                task_duration = self.energy_monitor.task_duration[task.name]
                task_energy = self.energy_monitor.task_energy[task.name]['total_energy']
                task_power = self.energy_monitor.get_task_power(task.name)

                signal.emit(
                    f"Stopped task: {task.name}. Duration: {task_duration:.2f} seconds. "
                    f"Energy consumed: {task_energy:.6f} Joules. Power: {task_power:.6f} Watts"
                )
            signal.emit("Completed one round of round robin scheduling.")
        self.energy_consumption['Round Robin'] = self.energy_monitor.total_energy

    def run_priority_based(self, duration, signal):
        print(f"Running priority algorithm for {duration} seconds")
        end_time = time.time() + duration
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        while time.time() < end_time:
            for task in sorted_tasks:
                self.energy_monitor.start_task(task.name)
                time.sleep(task.execution_time)
                self.energy_monitor.stop_task(task.name)

                task_duration = self.energy_monitor.task_duration[task.name]
                task_energy = self.energy_monitor.task_energy[task.name]['total_energy']
                task_power = self.energy_monitor.get_task_power(task.name)

                signal.emit(
                    f"Stopped task: {task.name}. Duration: {task_duration:.2f} seconds. "
                    f"Energy consumed: {task_energy:.6f} Joules. Power: {task_power:.6f} Watts"
                )
            signal.emit("Completed one round of priority algorithm scheduling.")
        self.energy_consumption['Priority Based'] = self.energy_monitor.total_energy

    def run_rms(self, duration, signal):
        print(f"Running RMS for {duration} seconds")
        end_time = time.time() + duration
        sorted_tasks = sorted(self.tasks, key=lambda t: t.period)
        while time.time() < end_time:
            for task in sorted_tasks:
                self.energy_monitor.start_task(task.name)
                time.sleep(task.execution_time)
                self.energy_monitor.stop_task(task.name)

                task_duration = self.energy_monitor.task_duration[task.name]
                task_energy = self.energy_monitor.task_energy[task.name]['total_energy']
                task_power = self.energy_monitor.get_task_power(task.name)

                signal.emit(
                    f"Stopped task: {task.name}. Duration: {task_duration:.2f} seconds. "
                    f"Energy consumed: {task_energy:.6f} Joules. Power: {task_power:.6f} Watts"
                )
            signal.emit("Completed one round of RMS scheduling.")
        self.energy_consumption['RMS'] = self.energy_monitor.total_energy

    def run_edf(self, duration, signal):
        print(f"Running EDF for {duration} seconds")
        end_time = time.time() + duration
        while time.time() < end_time:
            sorted_tasks = sorted(self.tasks, key=lambda t: t.deadline)
            for task in sorted_tasks:
                self.energy_monitor.start_task(task.name)
                time.sleep(task.execution_time)
                self.energy_monitor.stop_task(task.name)

                task_duration = self.energy_monitor.task_duration[task.name]
                task_energy = self.energy_monitor.task_energy[task.name]['total_energy']
                task_power = self.energy_monitor.get_task_power(task.name)

                signal.emit(
                    f"Stopped task: {task.name}. Duration: {task_duration:.2f} seconds. "
                    f"Energy consumed: {task_energy:.6f} Joules. Power: {task_power:.6f} Watts"
                )
            signal.emit("Completed one round of EDF scheduling.")
        self.energy_consumption['EDF'] = self.energy_monitor.total_energy

    def compare_algorithms(self, duration, signal):
        signal.emit("\n--- Running Comparison ---\n")

        algorithms = {
            'Round Robin': self.run_round_robin,
            'Priority Based': self.run_priority_based,
            'RMS': self.run_rms,
            'EDF': self.run_edf,
        }

        for name, method in algorithms.items():
            self.energy_monitor = EnergyMonitor()  # Reset monitor
            signal.emit(f"Measuring {name}...")
            method(duration, signal)

        least_energy_algo = min(self.energy_consumption, key=self.energy_consumption.get)
        signal.emit(f"\nLeast energy-consuming algorithm: {least_energy_algo}")
class Signal:
    def emit(self, message):
        print(message)
# Example Usage
if __name__ == "__main__":
    scheduler = HybridScheduler()
    scheduler.add_task(Task("Task A", period=10, execution_time=2))
    scheduler.add_task(Task("Task B", period=20, execution_time=3))
    signal = Signal()
    scheduler.compare_algorithms(10, signal)
