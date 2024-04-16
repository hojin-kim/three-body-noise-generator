import numpy as np 

_GRAVITATION_CONSTANT = 1

class body:
    def __init__(self, mass, position, velocity, name=None):
        assert len(position) == 2 and len(velocity) == 2
        self.mass = mass
        self.position = np.array(position, dtype=np.float64)
        self.velocity = np.array(velocity, dtype=np.float64)
        self.name = str(name)
    
    def kinetic_energy(self):
        return 0.5 * self.mass * np.sum(self.velocity**2)

    def potential_energy(self, other):
        return - _GRAVITATION_CONSTANT * self.mass * other.mass / self.distance(other)

    def distance_squared(self, other):
        dist = (self.position[0] - other.position[0])**2 + (self.position[1] - other.position[1])**2
        if dist < 0.00003: ## Perhaps this might be adjusted
            raise ZeroDivisionError("Collision!")
        return dist
    
    def distance(self, other):
        return np.sqrt(self.distance_squared(other))

class three_body_system:
    def __init__(self, body1, body2, body3):
        assert isinstance(body1, body) and isinstance(body2, body) and isinstance(body3, body)

        positions = np.array([body1.position, body2.position, body3.position], dtype=np.float64)
        self.velocities = np.array([body1.velocity, body2.velocity, body3.velocity], dtype=np.float64)
        self.masses = np.array([body1.mass, body2.mass, body3.mass], dtype=np.float64)

        ## Translate the CoM of the system to the origin
        centor_of_mass = np.sum(positions * self.masses[:, np.newaxis], axis=0) / np.sum(self.masses)
        self.positions = positions-centor_of_mass
        
        self.timestamp = 0
        self.time = 0

        self.trajectory = self.positions.reshape(3,1,2)
        self.velocity_history = self.velocities.reshape(3,1,2)
        self.energy_history = np.array([body1.kinetic_energy() + body2.kinetic_energy() + body3.kinetic_energy(), body1.potential_energy(body2) + body1.potential_energy(body3) + body2.potential_energy(body3)], dtype=np.float64).reshape(1,2)

        self.total_mass = np.sum(self.masses)


    def acceleration(self):
        _epsilon = 1e-8
        diff_positions = self.positions[:, np.newaxis, :] - self.positions[np.newaxis, :, :]
        distances = np.linalg.norm(diff_positions, axis=-1)         

        force_vectors = _GRAVITATION_CONSTANT * diff_positions * ( self.masses[:, np.newaxis] * self.masses[np.newaxis, :] / (distances**3 + _epsilon))[:, :, np.newaxis]

        return - np.sum(force_vectors, axis=1) / self.masses[:, np.newaxis]
    
    
    def energies(self):
        
        ke = 0.5 * np.sum(self.masses * np.sum(self.velocities**2, axis=1))

        _pairs = [(0,1), (0,2), (1,2)]
        pe = 0 
        for i, j in _pairs:
            _dist = np.linalg.norm(self.positions[i] - self.positions[j])
            pe -= _GRAVITATION_CONSTANT * self.masses[i] * self.masses[j] / _dist

        return np.array([ke, pe], dtype=np.float64)


    def update(self, dt, method = "VV"):
        if method == "leapfrog" or method == "LF":
            accs = self.acceleration()
            self.velocities += 0.5 * accs * dt
            self.positions += self.velocities * dt
            self.velocities += 0.5 * self.acceleration() * dt
        
        else: ## Default to velocity verlet
            accs_prev = self.acceleration()
            self.positions += self.velocities * dt + 0.5 * accs_prev * dt**2
            self.velocities += 0.5 * (accs_prev + self.acceleration()) * dt

        ## translate the CoM of the system to the origin
        center_of_mass = np.sum(self.positions * self.masses[:, np.newaxis], axis=0) / np.sum(self.masses)
        self.positions -= center_of_mass

        self.time += dt
        self.timestamp += 1

        if self.timestamp >= self.trajectory.shape[1]:
            self.trajectory = np.concatenate(
                (self.trajectory, np.zeros_like(self.trajectory)), axis=1)
            self.velocity_history = np.concatenate(
                (self.velocity_history, np.zeros_like(self.velocity_history)), axis=1)
        
        self.trajectory[:, self.timestamp] = self.positions
        self.velocity_history[:, self.timestamp] = self.velocities

        if self.timestamp >= self.energy_history.shape[0]:
        # Double the size of the energy_history array if it's full
            self.energy_history = np.concatenate(
                (self.energy_history, np.zeros_like(self.energy_history)), axis=0)
        self.energy_history[self.timestamp] = self.energies()

    def trimmed_trajectory(self):
        return self.trajectory[:,:self.timestamp+1,:]
    

    def trimmed_energy_history(self):
        return self.energy_history[:self.timestamp+1]