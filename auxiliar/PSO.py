import random
import math
import numpy as np

# Define Class Particles
class Particle:
    def __init__(self, position):
        self.position = position
        self.velocity = np.zeros_like(position)
        self.best_position = position
        self.best_fitness = float('inf')


def pso(page, temp, press, qe, temp_ref, obj_func, n_particles, max_iter, parameters, prog_bar):

    page.update()
    particles = []
    prog_bar.visible = True
    prog_bar.controls[1].value = 0
    prog_bar.controls[1].update()

    for i in range(n_particles):
        K3_init = 0
        if len(parameters) > 6:
            K3_init = parameters[6] + random.random() * (parameters[7] - parameters[6])
            np.insert(parameters, 3, K3_init)

        qmax_init = parameters[0] + random.random() * (parameters[1] - parameters[0])
        K1_init = parameters[2] + random.random() * (parameters[3] - parameters[2])
        K2_init = parameters[4] + random.random() * (parameters[5] - parameters[4])
        position = np.array([qmax_init, K1_init, K2_init, K3_init])
        particle = Particle(position)

        fitness = obj_func(position, temp, press, qe, temp_ref)

        if i == 0:
            swarm_best_position = position
            swarm_best_fitness = fitness

        particle.best_position = position
        particle.best_fitness = fitness

        if fitness < swarm_best_fitness:
            swarm_best_fitness = fitness
            swarm_best_position = position

        particles.append(particle)

    # PSO Main Loop
    for itr in range(max_iter):

        prog_bar.controls[0].value = "Progresso: "+str(int(((itr + 1) / max_iter)*100)) + "%"
        prog_bar.controls[1].value = ((itr+1) / max_iter)
        prog_bar.update()
        for particle in particles:

            # Update Velocity
            w = 0.8
            c1 = 1.2
            c2 = 1.2

            r1 = random.random()
            r2 = random.random()

            particle.velocity = w * particle.velocity + c1 * r1 * (
                    particle.best_position - particle.position) + c2 * r2 * (
                                        swarm_best_position - particle.position)

            particle.position = particle.position + particle.velocity
            fitness = obj_func(particle.position, temp, press, qe, temp_ref)

            if fitness < particle.best_fitness:
                particle.best_fitness = fitness
                particle.best_position = particle.position

            # Update GBest
            if fitness < swarm_best_fitness:
                swarm_best_fitness = fitness
                swarm_best_position = particle.position
    prog_bar.visible = False
    prog_bar.update()
    page.update()
    return swarm_best_position, swarm_best_fitness


def PSOmulti(T1, P1, qe1, T2, P2, qe2, Tref, ObjF, Pop_Size, max_iter):
    particles1 = []
    particles2 = []
    # Position Initialization
    for i in range(Pop_Size):

        position1 = np.array(
            [100 * abs(random.random()), abs(random.random()), 1000 * abs(random.random()),
             0.1 + 10 * abs(random.random())])
        particle1 = Particle(position1)

        position2 = np.array(
            [100 * abs(random.random()), 10 * abs(random.random()), 10000 * abs(random.random()),
             10 * abs(random.random())])
        particle2 = Particle(position2)

        # Fitness Update
        fitness1 = ObjF(position1, T1, P1, qe1, Tref) + abs(position1[0] * position1[3] - position2[0] * position2[3])
        fitness2 = ObjF(position2, T2, P2, qe2, Tref) + abs(position1[0] * position1[3] - position2[0] * position2[3])

        if i == 0:
            swarm_best_position1 = position1
            swarm_best_fitness1 = fitness1
            swarm_best_position2 = position2
            swarm_best_fitness2 = fitness2

        particle1.best_position = position1
        particle1.best_fitness = fitness1
        particle2.best_position = position2
        particle2.best_fitness = fitness2

        if fitness1 < swarm_best_fitness1:
            swarm_best_fitness1 = fitness1
            swarm_best_position1 = position1

        if fitness2 < swarm_best_fitness2:
            swarm_best_fitness2 = fitness2
            swarm_best_position2 = position2

        particles1.append(particle1)
        particles2.append(particle2)

    for itr in range(max_iter):
        for index in range(len(particles1)):
            w = 0.8
            c1 = 1.2
            c2 = 1.2
            r1 = random.random()
            r2 = random.random()
            particles1[index].velocity = w * particles1[index].velocity + c1 * r1 * (
                    particles1[index].best_position - particles1[index].position) + c2 * r2 * (
                                                 swarm_best_position1 - particles1[index].position)
            particles1[index].position = particles1[index].position + particles1[index].velocity

            particles2[index].velocity = w * particles2[index].velocity + c1 * r1 * (
                    particles2[index].best_position - particles2[index].position) + c2 * r2 * (
                                                 swarm_best_position2 - particles2[index].position)
            particles2[index].position = particles2[index].position + particles2[index].velocity
            extra = 0.1 * abs(
                particles1[index].position[0] * particles1[index].position[3] - particles2[index].position[0] *
                particles2[index].position[3])
            fitness1 = ObjF(particles1[index].position, T1, P1, qe1, Tref) + extra
            fitness2 = ObjF(particles2[index].position, T2, P2, qe2, Tref) + extra
            if fitness1 < particles1[index].best_fitness:
                particles1[index].best_fitness = fitness1
                particles1[index].best_position = particles1[index].position
            if fitness1 < swarm_best_fitness1:
                swarm_best_fitness1 = fitness1
                swarm_best_position1 = particles1[index].position
            if fitness2 < particles2[index].best_fitness:
                particles2[index].best_fitness = fitness2
                particles2[index].best_position = particles2[index].position
            if fitness2 < swarm_best_fitness2:
                swarm_best_fitness2 = fitness2
                swarm_best_position2 = particles2[index].position
        # print(swarm_best_fitness1)
        # print(swarm_best_fitness2)
    return swarm_best_position1, swarm_best_fitness1, swarm_best_position2, swarm_best_fitness2


def langmuir(x, T, P, qe, Tref):
    result = 0
    for i in range(len(P)):
        try:
            np.seterr(all='ignore')
            conta = (x[0] * x[1] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * P[i]) / (
                    1 + x[1] * math.exp(x[2] * (1 / T[i] - 1 / Tref)) * P[i])
            result = result + (qe[i] - conta) ** 2

        except:
            result += 100000000

    return result


def langmuir_multi(x, T, P, qe, Tref):
    result = 0
    for i in range(len(P)):
        try:
            np.seterr(all='ignore')
            # conta = x[0] * x[1] * P[i] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * ((1 - (qe[i] / x[0])) ** x[3])
            x0 = 0
            result = result + (qe[i] - newton(x, x0, T[i], P[i], Tref)) ** 2
        except:
            result += 100000000

    return result


def funcao_langmuir(x, x0, Ti, Pi, Tref):
    return x0 - x[0] * x[1] * Pi * math.exp(x[2] * ((1 / Ti) - (1 / Tref))) * ((1 - (x0 / x[0])) ** x[3])


def derivada_langmuir(x, x0, Ti, Pi, Tref):
    return 1 + x[0] * x[1] * Pi * math.exp(x[2] * ((1 / Ti) - (1 / Tref))) * x[3] * ((1 - (x0 / x[0])) ** (x[3] - 1)) / \
        x[0]


def newton(x, x0, Ti, Pi, Tref):
    for i in range(10):
        x0 = x0 - funcao_langmuir(x, x0, Ti, Pi, Tref) / derivada_langmuir(x, x0, Ti, Pi, Tref)
    return x0


def sips(x, T, P, qe, Tref):
    result = 0
    for i in range(len(P)):
        try:
            np.seterr(all='ignore')
            conta = (x[0] * (math.exp(x[2] * ((1 / T[i]) - (1 / Tref))) * x[1] * P[i]) ** (1 / x[3])) / (
                    1 + (math.exp(x[2] * (1 / T[i] - 1 / Tref)) * x[1] * P[i]) ** (1 / x[3]))
            result = result + (qe[i] - conta) ** 2

        except:
            result += 100000000

    return result


def toth(x, T, P, qe, Tref):
    result = 0
    for i in range(len(P)):
        try:
            np.seterr(all='ignore')
            conta = (x[0] * math.exp(x[2] * ((1 / T[i]) - (1 / Tref)))
                     * x[1] * P[i]) / (math.pow(1 + math.pow(math.exp(x[2] * (1 / T[i] - 1 / Tref))
                                                             * x[1] * P[i], (x[3])), (1 / x[3])))
            result = result + math.pow(qe[i] - conta, 2)

        except:
            result += 100000000

    return result


TCH4 = [298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15,
        298.15, 298.15, 298.15, 298.15, 298.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15,
        308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15,
        323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15,
        323.15, 323.15, 323.15, 323.15]

XCH4 = [0, 0.0405, 0.1203, 0.191, 0.5515, 1.25, 1.65, 2.1, 3.06, 3.45, 4.25, 6.31, 8.19, 10.7, 11.8, 14.1, 17.2, 18.9,
        0, 0.0525, 0.1115, 0.204, 0.4007, 0.8516, 1.35, 1.9, 2.8, 3.1, 3.5, 4.45, 5.85, 6.95, 7.8, 8.75, 11.1, 14.8,
        0, 0.0603, 0.1215, 0.22, 0.3302, 0.4612, 0.5505, 0.801, 1.15, 1.65, 2.4, 3.4, 4, 5.1, 5.05, 6.35, 7.8, 8.65]

YCH4 = [0, 0.024, 0.089, 0.131, 0.326, 0.712, 0.877, 1.12, 1.474, 1.617, 1.83, 2.357, 2.726, 3.06, 3.26, 3.53, 3.834,
        3.991, 0, 0.022, 0.064, 0.109, 0.210, 0.415, 0.623, 0.823, 1.133, 1.232, 1.360, 1.618, 1.931, 2.154, 2.342,
        2.466, 2.792, 3.201, 0, 0.017, 0.052, 0.09, 0.14, 0.196, 0.227, 0.312, 0.432, 0.59, 0.731, 1.009, 1.193,
        1.423, 1.395, 1.653, 1.929, 2.077]

TCO2 = [298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15, 298.15,
        308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15, 308.15,
        323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15, 323.15]

XCO2 = [0, 0.0118, 0.061, 0.2905, 0.861, 1.6, 3.1, 5.25, 10.15, 14.45, 19.35, 22.8, 26.6, 32, 0, 0.0126, 0.0407, 0.0905,
        0.1325, 0.2007, 0.4515, 0.9503, 1.6, 2.2, 2.8, 3.7, 4.85, 5.7, 0, 0.0106, 0.0214, 0.0501, 0.0907, 0.2423, 0.422,
        0.7503, 1.45, 2.7, 3.9, 5.45, 7.05, 8.5]

YCO2 = [0, 1.147, 2.249, 3.659, 4.5, 5.06, 5.58, 6.04, 6.52, 6.92, 6.96, 7.09, 7.22, 7.372, 0, 0.825, 1.458, 2.06, 2.4,
        2.734, 3.38, 4.05, 4.49, 4.74, 4.96, 5.167, 5.315, 5.399, 0, 0.356, 0.529, 1.06, 1.43, 2.09, 2.49, 2.9, 3.4,
        3.915,
        4.1, 4.329, 4.532, 4.74]


def chama_pso(page, T, P, qe, Tref, model, pop_size, max_iter, parameters, prog_bar):
    if model == 0:
        return pso(page, T, P, qe, Tref, langmuir, pop_size, max_iter, parameters, prog_bar)
    if model == 1:
        return pso(page, T, P, qe, Tref, sips, pop_size, max_iter, parameters, prog_bar)
    if model == 2:
        return pso(page, T, P, qe, Tref, toth, pop_size, max_iter, parameters, prog_bar)
    if model == 3:
        return pso(page, T, P, qe, Tref, toth, pop_size, max_iter, parameters, prog_bar)

def chama_pso_multi(T1, P1, qe1, T2, P2, qe2, Tref, model, pop_size, max_iter):
    if model == 4:
        return PSOmulti(T1, P1, qe1, T2, P2, qe2, Tref, langmuir_multi, pop_size, max_iter)
