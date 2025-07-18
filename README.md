# Energy-Aware-Task-Scheduling

A Python-based real-time Energy-Aware Task Scheduler that implements and compares multiple scheduling algorithms — Round Robin, Priority-Based, Rate Monotonic Scheduling (RMS), and Earliest Deadline First (EDF) — by measuring energy consumption using the pyRAPL library.

📌 Project Description
This project simulates the behavior of various CPU scheduling algorithms and evaluates their energy efficiency and execution performance. It is particularly useful in embedded or low-power systems where energy consumption is critical.

Key components:

Task management with period, execution time, and deadlines.

Dynamic scheduling using Round Robin, Priority, RMS, and EDF.

Energy consumption tracking via the pyRAPL package.

Custom signal emitter for output reporting.

💡 Features
🔄 Round Robin Scheduling

⚡ Energy Measurement with RAPL counters (via pyRAPL)

⏱️ Execution Time and Power Calculation

🧠 Hybrid Scheduler class for easy algorithm testing

📊 Comparison Report showing the least energy-consuming algorithm

🛠️ Tech Stack
Language: Python 3.x

Libraries:

pyRAPL — for energy consumption measurement

time — for task timing
