import obd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import os.path
from os import path


def main():
    print("live_plot.py main")
    #    live_plot1 = LivePlot(obd.commands.RPM, 50)
    #   live_plot2 = LivePlot(obd.commands.SPEED, 50)
    #    live_plot3 = LivePlot(samples=50)
    lp = LivePlot(['SPEED', 'RPM', 'MAF'], 50)
    plt.show()


class DataSet:
    def __init__(self, cmd, i, samples=25, running_average=10, f_dir="/tmp/", f_extension="obd_elm_data"):
        print("Initializing new " + str(cmd) + " dataset")
        style.use('fivethirtyeight')
        self.cmd = obd.commands[cmd]
        self.data_file = f_dir + cmd + "." + f_extension
        self.running_average = running_average
        self.running_averages = []
        self.averages = []
        self.f_dir = f_dir
        self.f_extension = f_extension
        self.data_file_exists = True
        self.fig = plt.figure(i)
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ani = animation.FuncAnimation(self.fig, animate, fargs=(i, self, samples, running_average))


class LivePlot:

    def __init__(self, cmds=['ELM_VOLTAGE'], samples=25, running_average=10):
        print('Initializing new Live Plot for ' + str(cmds))
        print('Plot Samples = ' + str(samples))
        print('Running Average = ' + str(running_average))
        self.samples = samples
        self.running_average = running_average
        self.data_sets = []
        i = 0
        for cmd in cmds:
            ds = DataSet(cmd, i, samples, running_average)
            self.data_sets.append(ds)
            i += 1


def animate(self, i, ds, samples=25, running_average=10):
    xs = []
    ys = []
    i = 0
    max_val_index = 0
    min_val_index = 0
    if path.exists(ds.data_file):
        if not ds.data_file_exists:
            print("New Data File Found: " + ds.data_file)
            ds.data_file_exists = True
        with open(ds.data_file) as file:
            for line in (file.readlines()[-samples:]):
                # print(line, end='')
                xs.append(int(i))
                ys.append(float(line.strip()))
                i += 1
        file.close()
        # print(xs)
        # print(ys)
        average = sum(ys) / len(ys)
        ds.averages.append(average)
        if len(ds.averages) > len(ys):
            ds.averages = ds.averages[-len(ys):]
        # averages = [average] * len(ys)
        running_average_val = 0
        if len(ys) > ds.running_average:
            samples_to_average = ys[-running_average:]
            running_average_val = sum(samples_to_average) / len(samples_to_average)
            ds.running_averages.append(running_average_val)
            if len(ds.running_averages) > len(ys):
                ds.running_averages = ds.running_averages[-len(ys):]

        max_val = max(ys)
        min_val = min(ys)
        # print("average = " + str(average) + ", min = " + str(min_val) + ", max = " + str(max_val))
        ds.ax.clear()

        ds.ax.plot(ys, label="Data")
        ds.ax.annotate(str(ys[-1]), xy=(len(ys) - 1, ys[-1]))

        ds.ax.plot(ds.averages, label="Average")
        ds.ax.annotate(str(average), xy=(len(ds.averages) - 1, average))

        if len(ys) >= ds.running_average:
            ds.ax.plot(ds.running_averages, label="Running Average: " + str(ds.running_average))
            ds.ax.annotate(str(running_average_val), xy=(len(ds.running_averages) - 1, running_average_val))

        ds.ax.set_title(str(ds.cmd.name))
        ds.ax.legend(loc="upper left")


    else:
        print("Data File Not Found: " + ds.data_file)
        ds.data_file_exists = False


if __name__ == '__main__':
    main()
