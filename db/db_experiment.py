import sqlite3
from classes import experiment_class as ec


ns_exp = ec.NotSynchronizedExperiment
def __create_db_ns_experiment__(db_name, ns_exp):

    if ".exp" in db_name:
        new_db = sqlite3.connect(db_name)
    else:
        new_db = sqlite3.connect(db_name + '.exp')

    try:

        new_cursor = new_db.cursor()

        new_cursor.execute("DROP TABLE if exists temperature")
        new_cursor.execute("DROP TABLE if exists flow")
        new_cursor.execute("DROP TABLE if exists y")

        new_cursor.execute("CREATE TABLE temperature (temperature_t float, temperature float)")
        new_cursor.execute("CREATE TABLE flow (flow_t float, flow float)")
        new_cursor.execute("CREATE TABLE y (y_t float, y float)")

        for i in range(len(ns_exp.time_temperature_column)):
            new_cursor.execute("INSERT INTO temperature VALUES(" + str(ns_exp.time_temperature_column[i]) + ","
                               + str(ns_exp.temperature_column[i]) + ")")
        for i in range(len(ns_exp.time_flow_column)):
            new_cursor.execute("INSERT INTO flow VALUES(" + str(ns_exp.time_flow_column[i]) + ","
                               + str(ns_exp.flow_column[i]) + ")")
        for i in range(len(ns_exp.time_y_column)):
            new_cursor.execute("INSERT INTO y VALUES(" + str(ns_exp.time_y_column[i]) + ","
                               + str(ns_exp.y_column[i]) + ")")

        new_cursor.execute("DROP TABLE if exists constants")

        new_cursor.execute("CREATE TABLE constants ("
                           "inlet_temperature float, "
                           "inlet_flow float, "
                           "inlet_y float,"
                           "inlet_p float,"
                           "ads_mass float, "
                           "bed_length float, "
                           "bed_diameter float, "
                           "porosity float"
                           ")")

        new_cursor.execute("INSERT INTO constants VALUES("
                           + str(ns_exp.inlet_temperature) +
                           "," + str(ns_exp.inlet_flow) +
                           "," + str(ns_exp.inlet_y) +
                           "," + str(ns_exp.inlet_pressure) +
                           "," + str(ns_exp.adsorbent_mass) +
                           "," + str(ns_exp.bed_length) +
                           "," + str(ns_exp.bed_diameter) +
                           "," + str(ns_exp.porosity) +
                           ")")

    except:
        return print("Erro no banco de dados!!")
    else:
        new_db.commit()
    finally:
        new_db.close()


s_exp = ec.SynchronizedExperiment
def __create_db_experiment__(db_name, s_exp):

    new_db = sqlite3.connect(db_name + '.exp')

    try:
        new_cursor = new_db.cursor()

        new_cursor.execute("DROP TABLE if exists timet")
        new_cursor.execute("DROP TABLE if exists temperature")
        new_cursor.execute("DROP TABLE if exists flow")
        new_cursor.execute("DROP TABLE if exists y")


        new_cursor.execute("CREATE TABLE timet (timet float)")
        new_cursor.execute("CREATE TABLE temperature (temperature float)")
        new_cursor.execute("CREATE TABLE flow (flow float)")
        new_cursor.execute("CREATE TABLE y (y float)")


        for i in range(len(s_exp.time_column)):
            new_cursor.execute("INSERT INTO timet VALUES(" + str(s_exp.time_column[i]) + ")")
            new_cursor.execute("INSERT INTO temperature VALUES(" + str(s_exp.temperature_column[i]) + ")")
            new_cursor.execute("INSERT INTO flow VALUES(" + str(s_exp.flow_column[i]) + ")")
            new_cursor.execute("INSERT INTO y VALUES(" + str(s_exp.y_column[i]) + ")")


        new_cursor.execute("DROP TABLE if exists constants")

        new_cursor.execute("CREATE TABLE constants ("
                           "inlet_temperature float, "
                           "inlet_flow float, "
                           "inlet_y float,"
                           "inlet_p float,"
                           "ads_mass float, "
                           "bed_length float, "
                           "bed_diameter float, "
                           "porosity float, "
                           "q float, "
                           "t_init float, "
                           "t_final float, "
                           "n_partitions float"
                           ")")

        new_cursor.execute("INSERT INTO constants VALUES("
                           + str(s_exp.inlet_temperature) +
                           "," + str(s_exp.inlet_flow) +
                           "," + str(s_exp.inlet_y) +
                           "," + str(s_exp.inlet_pressure) +
                           "," + str(s_exp.adsorbent_mass) +
                           "," + str(s_exp.bed_length) +
                           "," + str(s_exp.bed_diameter) +
                           "," + str(s_exp.porosity) +
                           "," + str(s_exp.q) +
                           "," + str(s_exp.initial_t) +
                           "," + str(s_exp.final_t) +
                           "," + str(s_exp.n_partitions) +
                           ")")

    except:
        return print("Erro no banco de dados!!")
    else:
        new_db.commit()
    finally:
        new_db.close()


def __load_db_experiment__(db_name):
    new_exp = ec.SynchronizedExperiment
    new_db = sqlite3.connect(db_name)
    try:
        new_cursor = new_db.cursor()
        new_cursor.execute("SELECT timet FROM timet")
        timet_fetch = new_cursor.fetchall()
        time_column = [row[0] for row in timet_fetch]

        new_cursor.execute("SELECT temperature FROM temperature")
        temperatura_fetch = new_cursor.fetchall()
        temperature_column = [row[0] for row in temperatura_fetch]

        new_cursor.execute("SELECT flow FROM flow")
        flow_fetch = new_cursor.fetchall()
        flow_column = [row[0] for row in flow_fetch]

        new_cursor.execute("SELECT y FROM y")
        y_fetch = new_cursor.fetchall()
        y_column = [row[0] for row in y_fetch]

        new_cursor.execute("SELECT inlet_temperature FROM constants")
        inlet_temperature = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT inlet_flow FROM constants")
        inlet_flow = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT inlet_y FROM constants")
        inlet_y = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT inlet_p FROM constants")
        inlet_p = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT ads_mass FROM constants")
        ads_mass = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT bed_length FROM constants")
        bed_length = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT bed_diameter FROM constants")
        bed_diameter = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT porosity FROM constants")
        porosity = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT q FROM constants")
        q = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT t_init FROM constants")
        t_init = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT t_final FROM constants")
        t_final = new_cursor.fetchone()[0]

        new_cursor.execute("SELECT n_partitions FROM constants")
        n_partitions = new_cursor.fetchone()[0]

        new_exp.time_column = time_column
        new_exp.temperature_column = temperature_column
        new_exp.flow_column = flow_column
        new_exp.y_column = y_column
        new_exp.inlet_temperature = inlet_temperature
        new_exp.inlet_flow = inlet_flow
        new_exp.inlet_y = inlet_y
        new_exp.inlet_p = inlet_p
        new_exp.adsorbent_mass = ads_mass
        new_exp.bed_length = bed_length
        new_exp.bed_diameter = bed_diameter
        new_exp.porosity = porosity
        new_exp.q = q
        new_exp.t_init = t_init
        new_exp.t_final = t_final
        new_exp.n_partitions = n_partitions

    except:
        print("Erro no banco de dados!!")
    finally:
        new_db.close()

    return new_exp




def __load_db_pack_experiment__(db_name):

    new_db = sqlite3.connect(db_name)
    exp_result = []
    try:
        new_cursor = new_db.cursor()

        new_cursor.execute("SELECT inlet_temperature FROM constants")
        inlet_temperature = new_cursor.fetchone()[0]
        exp_result.insert(0, inlet_temperature)

        new_cursor.execute("SELECT inlet_p FROM constants")
        inlet_p = new_cursor.fetchone()[0]
        exp_result.insert(1, inlet_p)

        new_cursor.execute("SELECT q FROM constants")
        q = new_cursor.fetchone()[0]
        exp_result.insert(2, q)

    except:
        print("Erro no banco de dados!!")
    finally:
        new_db.close()

    return exp_result

