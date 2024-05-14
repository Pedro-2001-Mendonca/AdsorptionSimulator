import numpy as np
from classes import experiment_class as ec


def synchronize(ns_class: ec.NotSynchronizedExperiment, initial_t, final_t, n_points):

    new_time = np.linspace(initial_t, final_t, n_points)
    poly_temperature = interpolation(ns_class.time_temperature_column, ns_class.temperature_column)
    poly_flow = interpolation(ns_class.time_flow_column, ns_class.flow_column)
    poly_y = interpolation(ns_class.time_y_column, ns_class.y_column)
    new_temperature = []
    new_flow = []
    new_y = []
    concentration = []
    f_out = []

    flow_qls = []
    gas_cte = 0.08314462
    for i in range(len(new_time)):
        if get_position(new_time[i], ns_class.time_temperature_column) < len(poly_temperature):
            new_temperature.append(poly_temperature[get_position(new_time[i], ns_class.time_temperature_column)](new_time[i]))
        else:
            new_temperature.append(poly_temperature[len(poly_temperature)-1](new_time[i]))

        if get_position(new_time[i], ns_class.time_flow_column) < len(poly_flow):
            new_flow.append(poly_flow[get_position(new_time[i], ns_class.time_flow_column)](new_time[i]))
        else:
            new_flow.append(poly_flow[len(poly_y)-1](new_time[i]))

        if get_position(new_time[i], ns_class.time_y_column) < len(poly_y):
            new_y.append(poly_y[get_position(new_time[i], ns_class.time_y_column)](new_time[i]))
        else:
            new_y.append(poly_y[len(poly_y)-1](new_time[i]))

        flow_qls.append(new_flow[i])
        concentration.append(new_y[i] * ns_class.inlet_pressure / (
                (new_temperature[i]) * gas_cte))
        f_out.append(concentration[i] * flow_qls[i])
    print('flowqls: ' + str(flow_qls))
    sClass = ec.SynchronizedExperiment(
        ns_class.experiment_name,
        ns_class.inlet_pressure,
        ns_class.inlet_flow,
        ns_class.inlet_temperature,
        ns_class.inlet_y,
        ns_class.adsorbent_mass,
        ns_class.bed_length,
        ns_class.bed_diameter,
        new_time,
        new_temperature,
        new_flow,
        new_y,
        ns_class.temperature_unit,
        ns_class.pressure_unit,
        ns_class.flow_unit,
        poly_flow,
        poly_temperature,
        poly_y,
        f_out,
        concentration,
        ns_class.porosity)

    return sClass


def interpolation(x, y):
    poly = []
    for i in range(len(x)-1):
        coef = np.polyfit([x[i], x[i+1]], [y[i], y[i+1]], 1)
        poly1d_fn = np.poly1d(coef)
        poly.append(poly1d_fn)
    return poly


def get_position(value, vector):

    for j in range(len(vector)):
        if vector[j] > value:
            return j-1
    return len(vector)-1



