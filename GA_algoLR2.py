import streamlit as st
import random

# ------------------- Streamlit App -------------------
st.title("Genetic Algorithm: Bit Pattern Generator")

# GA Parameters (predefined)
POPULATION_SIZE = 300
CHROMOSOME_LENGTH = 80
TARGET_ONES = 50
MAX_VALUE = 80
GENERATIONS = 50
MUTATION_RATE = 0.01

# Fitness function
def fitness(chromosome):
    ones_count = sum(chromosome)
    return MAX_VALUE - abs(TARGET_ONES - ones_count)

# Create initial population
def create_population():
    return [[random.randint(0, 1) for _ in range(CHROMOSOME_LENGTH)] for _ in range(POPULATION_SIZE)]

# Selection (tournament)
def select(population):
    tournament = random.sample(population, 3)
    tournament.sort(key=fitness, reverse=True)
    return tournament[0]

# Crossover (single-point)
def crossover(parent1, parent2):
    point = random.randint(1, CHROMOSOME_LENGTH-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Mutation
def mutate(chromosome):
    return [bit if random.random() > MUTATION_RATE else 1-bit for bit in chromosome]

# Run GA when button is clicked
if st.button("Run Genetic Algorithm"):
    population = create_population()
    fitness_history = []

    for gen in range(GENERATIONS):
        new_population = []
        while len(new_population) < POPULATION_SIZE:
            parent1 = select(population)
            parent2 = select(population)
            child1, child2 = crossover(parent1, parent2)
            new_population.append(mutate(child1))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(mutate(child2))
        population = new_population

        # Track best solution
        best = max(population, key=fitness)
        fitness_history.append(fitness(best))

        st.write(f"Generation {gen+1}: Best Fitness = {fitness(best)}, Ones Count = {sum(best)}")

    # Final best chromosome
    best_chromosome = max(population, key=fitness)
    st.subheader("Best Bit Pattern Found")
    st.write(best_chromosome)
    st.write("Number of Ones:", sum(best_chromosome))
    st.write("Fitness Value:", fitness(best_chromosome))

    # Plot fitness over generations
    st.line_chart(fitness_history)
