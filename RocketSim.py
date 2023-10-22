import RocketSimLib as rocket
import os.path as p
from pathlib import Path
from math import pi

def_dir = "C:\\Users\\amurr\\OneDrive\\Documents\\My Programs\\Python\\Rocket Simulator"

def main():
    exp_name = str(input("Name of experiment: "))
    num_of_trials = posIntOK("Number of trials: ")
    init_mass = posFloatOK("Initial mass: ")
    feul_mass = posFloatOK("Fuel mass: ")
    thrust = posFloatOK("Thrust Force: ")
    timeMECO = posFloatOK("MECO time: ")
    coeff = posFloatOK("Drag coefficient: ")
    area = posFloatOK("Front view area: ")
    samples_ps = float(posIntOK("Samples per second: "))

    exp_path = def_dir + "\\experiments\\" + exp_name
    if not p.exists(exp_path):
        Path(exp_path).mkdir(parents=True, exist_ok=True)

    exp_info_file = open(exp_path + "\\parameters.txt", 'w', encoding='utf-8')
    exp_info_file.write("Parameters")
    exp_info_file.write("\nNumber of trials: " + str(num_of_trials))
    exp_info_file.write("\nInitial mass: " + str(init_mass))
    exp_info_file.write("\nFuel mass: " + str(feul_mass))
    exp_info_file.write("\nThrust Force: " + str(thrust))
    exp_info_file.write("\nMECO time: " + str(timeMECO))
    exp_info_file.write("\nDrag coefficient: " + str(coeff))
    exp_info_file.write("\nFront view area: " + str(area))
    exp_info_file.write("\nSamples per second: " + str(samples_ps))

    trials = []
    for trial in range(num_of_trials):
        angle = trial * ((pi / 2) / (num_of_trials - 1))
        trial_folder_path = exp_path + "/trials/trial" + str(trial)
        if not p.exists(trial_folder_path):
            Path(trial_folder_path).mkdir(parents=True, exist_ok=True)
        trials.append(rocket.Rocket(trial_folder_path, init_mass, \
                      feul_mass, thrust, timeMECO, angle, coeff, area, samples_ps))

    data_file_path = exp_path + "\\data"
    if not p.exists(data_file_path):
        Path(data_file_path).mkdir(parents=True, exist_ok=True)
    init_angle_file = open(p.join(data_file_path, "initAngle.txt"), 'w', \
                    encoding='utf-8')
    max_dist_file = open(p.join(data_file_path, "maxDist.txt"), 'w', \
                    encoding='utf-8')
    total_time_file = open(p.join(data_file_path, "totalTime.txt"), 'w', \
                    encoding='utf-8')
    max_alt_file = open(p.join(data_file_path, "maxAlt.txt"), 'w', \
                    encoding='utf-8')
    apo_time_file = open(p.join(data_file_path, "apoTime.txt"), 'w', \
                    encoding='utf-8')

    for trial in trials:
        init_angle_file.write(str(trial.getInitAngle()) + '\n')
        max_dist_file.write(str(trial.getMaxDist()) + '\n')
        total_time_file.write(str(trial.getTotalTime()) + '\n')
        max_alt_file.write(str(trial.getMaxAlt()) + '\n')
        apo_time_file.write(str(trial.getApoTime()) + '\n')

def posIntOK(promt):
    while True:
        try:
            value = int(input(promt))
        except(ValueError):
            print("Error. Input must be a positive integer. \n")
        else:
            if value <= 0:
                print("Error. Input must be a positive integer. \n")
            else:
                break
    return value

def posFloatOK(promt):
    while True:
        try:
            value = float(input(promt))
        except(ValueError):
            print("Error. Input must be a positive float. \n")
        else:
            if value <= 0:
                print("Error. Input must be a positive float. \n")
            else:
                break
    return value

if __name__ == '__main__': 
    main()