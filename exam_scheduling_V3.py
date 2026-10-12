class Course:
  course_code: str
  department_code: str
  duration_hours: int
  enrolled_students: set[str]

  def __init__(self, code: str, department: str, duration: int, students: set[str]):
    self.course_code = code
    self.department_code = department
    self.duration_hours = duration
    self.enrolled_students = students

  def __eq__(self, other):
    return isinstance(other, Course) and self.course_code == other.course_code

  def __hash__(self):
    return hash(self.course_code)

  def __str__(self):
    return f"{self.course_code}"

  def __repr__(self):
    return f"{self.course_code}"

import json

with open('courseData.json', 'r') as f:
  courseData = json.load(f)

coursePool: list[Course] = [
    Course(
      i["course_code"],
      i["department_code"],
      i["duration_hours"],
      set(i["enrolled_students"])
    ) for i in courseData
]

import random
import copy
import matplotlib.pyplot as plt

CHROMOSOME_LENGTH = 30 

POPULATION_SIZE = 50 # number of potential solution
GENERATIONS = 50 # the number of generation to run
CROSSOVER_RATE = 0.7 # the probability of two chromosome to undergo crossover
MUTATION_RATE = 0.10 # the probability of a gene to mutate

def generate_random_chromosome():
  # randomly genereate the flat chromosome
  init_chromosome = coursePool[:]
  random.shuffle(init_chromosome)

  return init_chromosome

def generate_initial_population():
  population = [generate_random_chromosome() for _ in range(POPULATION_SIZE)]
  return population

IDEAL_SCORE = 3000
TOTAL_SEAT_POOL = 30
PENALTY_CLASH = 100  # Massive penalty for a student having two exams at once
PENALTY_SEAT = 10     # Penalty per student over the 30-seat limit

def to_phenotype(flat_chromosome):
  chromosome = []
  while len(flat_chromosome) != 0:
    session1 = [flat_chromosome[0], flat_chromosome[1], flat_chromosome[2]]
    session2 = [flat_chromosome[3], flat_chromosome[4], flat_chromosome[5]]
    flat_chromosome = flat_chromosome[6:]
    day = [session1, session2]
    chromosome.append(day)
  return chromosome

def to_genotype(chromosome):
  flat_chromosome = []
  for day in chromosome:
    for session in day:
      flat_chromosome.extend(session)
  return flat_chromosome

def evaluate_chromosome_fitness(chromosome):
  seat_penalty_count = 0
  clash_penalty_count = 0

  chromosome = to_phenotype(chromosome)

  for day in chromosome:
    for session in day:

      all_students_in_session = []
      for course in session:
        all_students_in_session.extend(course.enrolled_students)

      # --- SEAT POOL PENALTY ---
      total_headcount = len(all_students_in_session)
      if total_headcount > TOTAL_SEAT_POOL:
        # calculate how many students exceed the limit
        oversheet_count = total_headcount - TOTAL_SEAT_POOL
        seat_penalty_count += oversheet_count * PENALTY_SEAT

      # --- CLASH PENALTY ---
      unique_students_in_session = set(all_students_in_session)
      duplicate_count = len(all_students_in_session) - len(unique_students_in_session)

      if duplicate_count > 0:
        clash_penalty_count += duplicate_count * PENALTY_CLASH
  fitness_score = IDEAL_SCORE - seat_penalty_count - clash_penalty_count
  return (max(1, fitness_score))

def evaluate_population(population):
  population_score = []

  for chromosome in population:
    score = evaluate_chromosome_fitness(chromosome)
    population_score.append(score)

  return population_score

def roulette_wheel_selection(population, population_fitness):
  total_fitness = sum(population_fitness)

  # catch if the entire feneration is heavily penalized
  if total_fitness <= len(population_fitness):
    return random.choice(population)

  # generate random spin value
  spin_wheel = random.uniform(0, total_fitness)
  running_sum = 0

  for chromosome, fitness_score in zip(population, population_fitness):
    running_sum += fitness_score
    if running_sum >= spin_wheel:
      return chromosome

  return population[-1] # boundart fallback

def selection_phase(population, population_fitness):
  # --- ELITISM ---
  sorted_indeces = sorted(range(len(population_fitness)), key=lambda i: population_fitness[i], reverse=True) 

  elite1 = copy.deepcopy(population[sorted_indeces[0]])
  elite2 = copy.deepcopy(population[sorted_indeces[1]])

  # --- ROULETTE SELECTION ---
  selected_parent_pool = []
  for _ in range(POPULATION_SIZE):
    parent = roulette_wheel_selection(population, population_fitness)
    selected_parent_pool.append(copy.deepcopy(parent))

  return elite1, elite2, selected_parent_pool

def matrix_to_flat(chromosome):
  flat_chromosome = []
  for day in chromosome:
    for session in day:
      flat_chromosome.extend(session)
  return flat_chromosome

def flat_to_matrix(flat_chromosome):
  chromosome = []
  while len(flat_chromosome) != 0:
    session1 = [flat_chromosome[0], flat_chromosome[1], flat_chromosome[2]]
    session2 = [flat_chromosome[3], flat_chromosome[4], flat_chromosome[5]]
    flat_chromosome = flat_chromosome[6:]
    day = [session1, session2]
    chromosome.append(day)
  return chromosome

def repair_child(flat_child, coursePool):
  course_count = {course: 0 for course in coursePool}
  duplicate_index = []
  
  for course, i in zip(flat_child, range(len(flat_child))):
    course_count[course] += 1
  
    if course_count[course] > 1:
      duplicate_index.append(i)
  
  missing_courses = []
  for course in coursePool:
    if course_count[course] == 0:
      missing_courses.append(course)
  
  random.shuffle(missing_courses)

  for i in duplicate_index:
    flat_child[i] = missing_courses.pop()
  
  return flat_child

def singlepoint_crossover(parent1, parent2):
  # check if the crossover occours
  if random.random() > CROSSOVER_RATE:
    return parent1, parent2

  num_of_slot = len(parent1)

  crossover_point = random.randint(0, num_of_slot - 1)
  child1 = parent1[:crossover_point] + parent2[crossover_point:]
  child2 = parent2[:crossover_point] + parent1[crossover_point:]

  # repair operation
  child1 = repair_child(child1, coursePool)
  child2 = repair_child(child2, coursePool)

  return child1, child2

def mutation(chromosome):
  if random.random() > MUTATION_RATE:
    return chromosome

  point1 = random.randint(0, len(chromosome) - 1)
  point2 = random.randint(0, len(chromosome) - 1)

  chromosome[point1], chromosome[point2] = chromosome[point2], chromosome[point1]

  return chromosome

import matplotlib.pyplot as plt

def plot_fitness_history(avg_history, best_history):
  generations = range(1, len(avg_history) + 1)

  plt.plot(generations, avg_history, label='Average Fitness', color='blue', linewidth=2)

  plt.plot(generations, best_history, label='Best Fitness', color='green', linestyle='--', linewidth=2)

  plt.xlabel('Generation')
  plt.ylabel('Fitness Score')
  plt.title('Genetic Algorithm Performance over Generations')
  plt.legend(loc='lower right')
  plt.grid(True, linestyle=':', alpha=0.6)

  plt.tight_layout()
  
  return plt.show()


def genetic_algorithm():
  population = generate_initial_population()
  
  # --- Track progress history ---
  avg_fitness_history = []
  best_fitness_history = []
  
  for generation in range(GENERATIONS):
    fitness_values = evaluate_population(population)

    # --- Record progress ---
    avg_fitness_history.append(sum(fitness_values) / POPULATION_SIZE)
    best_fitness = max(fitness_values)
    best_fitness_history.append(best_fitness)

    elite1, elite2, selected_parent_pool = selection_phase(population, fitness_values)

    new_population = [elite1, elite2]
    while len(new_population) < POPULATION_SIZE:
      parent1 = random.choice(selected_parent_pool)
      parent2 = random.choice(selected_parent_pool)
      child1, child2 = singlepoint_crossover(parent1, parent2)
      child1 = mutation(child1)
      child2 = mutation(child2)
      new_population.extend([child1, child2])

    population = new_population

    fitness_values = evaluate_population(population)
    best_fitness = max(fitness_values)
    best_chromosome = population[fitness_values.index(best_fitness)]
    print(f"Generation {generation + 1}: Best Fitness = {best_fitness}")
  
  best_index = fitness_values.index(max(fitness_values))
  best_chromosome = population[best_index]
  print(f"Best Chromosome: {to_phenotype(best_chromosome)}")
  print(f"Best Fitness: {max(fitness_values)}")

  return avg_fitness_history, best_fitness_history


if __name__ == "__main__":
  avg_hist, best_hist = genetic_algorithm()

  plot_fitness_history(avg_hist, best_hist)