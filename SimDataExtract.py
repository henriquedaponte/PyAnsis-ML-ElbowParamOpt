# Importing the PyFluent libraries required
import ansys.fluent.core as pyfluent
from ansys.fluent.core import examples
from ansys.fluent.visualization.pyvista import Graphics
import pandas as pd

# Downloading the mixing elbow sample .cas file from the repository
import_filename = examples.download_file('mixing_elbow.cas.h5', 'pyfluent/mixing_elbow')

# Starting the fluent session with a visible GUI
solver = pyfluent.launch_fluent(precision='double', processor_count=2, show_gui=True, mode='solver')

# Importing the mixing elbow sample .cas file
solver.file.read(file_type='case', file_name=import_filename)

# Configuring the turbulence model
solver.setup.models.viscous = {'model' : 'k-epsilon'}
solver.setup.models.viscous.near_wall_treatment.wall_function = 'standard-wall-fn'

# DataFrame to save results
results = pd.DataFrame(columns=['Hot_Inlet_Velocity', 'Cold_Inlet_Velocity', 'Outlet_Velocity'])

# Range of velocity magnitudes to iterate over
velocity_range = [i/10.0 for i in range(1, 11)]  # [0.1, 0.2, ..., 1.0]

# Run simulations for different velocity magnitudes
for hot_inlet_velocity in velocity_range:
    for cold_inlet_velocity in velocity_range:
        # Set the velocity magnitude for hot-inlet and cold-inlet
        solver.tui.define.boundary_conditions.set.velocity_inlet(
            "cold-inlet", (), "ke-spec", "no", "no", "no", "yes", "quit")
        solver.tui.define.boundary_conditions.set.velocity_inlet(
            "cold-inlet", (), "turb-intensity", cold_inlet_velocity, "quit")

        solver.tui.define.boundary_conditions.set.velocity_inlet(
            "hot-inlet", (), "ke-spec", "no", "no", "no", "yes", "quit")
        solver.tui.define.boundary_conditions.set.velocity_inlet(
            "hot-inlet", (), "turb-intensity", hot_inlet_velocity, "quit")
        
        
        # Initializing the Solution
        solver.solution.initialization.hybrid_initialize()

        # Running the Solver
        solver.solution.run_calculation.iterate(iter_count=100)

        field_data = solver.field_data

        # help(field_data.get_vector_field_data())

        # Get velocity magnitudes of hot-inlet, cold-inlet, and outlet
        hot_inlet_velocity_mag = field_data.get_vector_field_data(surface_name="hot-inlet", field_name="velocity")
        cold_inlet_velocity_mag = field_data.get_vector_field_data(surface_name="cold-inlet", field_name="velocity")
        outlet_velocity_mag = field_data.get_vector_field_data(surface_name="outlet", field_name="velocity")

        # Append result to DataFrame
        results = results.append({
            'Hot_Inlet_Velocity': hot_inlet_velocity_mag, 
            'Cold_Inlet_Velocity': cold_inlet_velocity_mag, 
            'Outlet_Velocity': outlet_velocity_mag
        }, ignore_index=True)

# Save DataFrame to CSV
results.to_csv('data.csv', index=False)

# Add an input prompt to keep the Python interpreter running
input("Success! Press enter to exit...")

