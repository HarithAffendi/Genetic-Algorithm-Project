# 📅 Exam Scheduling – Genetic Algorithm (GA)

A Python implementation of a **Genetic Algorithm** to solve the exam scheduling problem. The algorithm evolves a population of schedules over multiple generations to minimize student clashes and seat overflows.

---

## 📁 Project Files

| File | Description |
|------|-------------|
| `exam_scheduling.py` | Original GA implementation (matrix-based chromosome) |
| `exam_scheduling copy.py` | Refactored GA implementation (flat genotype representation) |
| `courseData.json` | Input data – course codes, departments, durations, and enrolled students |
| `module.py` | `Course` class definition (standalone module) |

---

## ⚙️ Prerequisites

### 1. Install Python

Make sure you have **Python 3.10 or higher** installed.

- Download from: https://www.python.org/downloads/
- During installation on Windows, **check the box** that says **"Add Python to PATH"**

To verify your installation, open a terminal (Command Prompt or PowerShell) and run:

```bash
python --version
```

You should see something like `Python 3.10.x` or higher.

---

### 2. Install Required Libraries

This project uses the following Python libraries:

| Library | Purpose |
|---------|---------|
| `matplotlib` | Plotting the fitness graph |
| `json` | Reading course data (built-in, no install needed) |
| `random` | Randomisation for GA (built-in, no install needed) |
| `copy` | Deep copying chromosomes (built-in, no install needed) |

Install the external dependency by running:

```bash
pip install matplotlib
```

---

## 🚀 How to Run

### Step 1 – Navigate to the project folder

Open a terminal (Command Prompt or PowerShell) and navigate to the folder:

```bash
cd path\to\GA coding
```

### Step 2 – Run the script

Choose either version to run:

```bash
# Refactored version (recommended)
python "exam_scheduling copy.py"

# Original version
python exam_scheduling.py
```

### Step 3 – View the output

The program will:
1. Print the **best fitness score** for each generation in the terminal
2. Display a **matplotlib graph** showing the average and best fitness over all generations

Example terminal output:
```
Generation 1: Best Fitness = 1950
Generation 2: Best Fitness = 2100
...
Generation 50: Best Fitness = 2980
Best Fitness: 2980
```

---

## 🧠 How It Works

The GA optimises an **exam timetable** for 30 courses over 5 days (2 sessions/day, 3 courses/session).

| GA Component | Details |
|---|---|
| **Population size** | 50 chromosomes |
| **Generations** | 50 |
| **Crossover rate** | 70% |
| **Mutation rate** | 30% |
| **Selection** | Roulette wheel + Elitism (top 2 preserved) |
| **Crossover** | Single-point crossover with repair |
| **Mutation** | Random swap mutation |

### Fitness Function
- Starts at an **ideal score of 3000**
- **−100** penalty per student with a scheduling clash (two exams at the same time)
- **−10** penalty per student exceeding the 30-seat room limit

---

## 🛠️ Troubleshooting

**`ModuleNotFoundError: No module named 'matplotlib'`**
→ Run `pip install matplotlib` in your terminal.

**`FileNotFoundError: courseData.json`**
→ Make sure you are running the script **from inside the project folder**, not from a different directory.

**`python` command not found**
→ Python is not added to PATH. Reinstall Python and tick **"Add Python to PATH"** during setup, or use `python3` instead of `python`.

---

## 📦 Quick Setup Summary

```bash
# 1. Install Python 3.10+ from https://www.python.org/downloads/

# 2. Install matplotlib
pip install matplotlib

# 3. Run the program
python "exam_scheduling copy.py"
```
