import obd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import os.path
from os import path


def main():
    print("live_plot.py main")
    live_plot1 = LivePlot(obd.commands.RPM, 50)
    live_plot2 = LivePlot(obd.commands.SPEED, 50)
    live_plot3 = LivePlot(samples=50)
    plt.show()


class LivePlot:

    def __init__(self, cmd=obd.commands.ELM_VOLTAGE, samples=25, running_average=10, f_dir="/tmp/",
                 f_extension="obd_elm_data"):
        print('Initializing new Live Plot for ' + cmd.name)
        self.cmd = cmd
        self.data_file = f_dir + cmd.name + "." + f_extension
        self.samples = samples
        self.running_average = running_average
        self.running_averages = []
        self.averages = []
        self.f_dir = f_dir
        self.f_extension = f_extension
        self.data_file_exists = True
        style.use('fivethirtyeight')
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1, 1, 1)

        self.ani2 = animation.FuncAnimation(self.fig, self.animate,
                                            fargs=(self.data_file, self.samples, self.running_average), interval=1000)

    def animate(self, i, data_file, samples=25, running_average=10):
        xs = []
        ys = []
        i = 0
        max_val_index = 0
        min_val_index = 0
        if path.exists(data_file):
            if not self.data_file_exists:
                print("New Data File Found: " + data_file)
                self.data_file_exists = True
            with open(data_file) as file:
                for line in (file.readlines()[-samples:]):
                    # print(line, end='')
                    xs.append(int(i))
                    ys.append(float(line.strip()))
                    i += 1
            file.close()
            # print(xs)
            # print(ys)
            average = sum(ys) / len(ys)
            self.averages.append(average)
            if len(self.averages) > len(ys):
                self.averages = self.averages[-len(ys):]
            # averages = [average] * len(ys)
            running_average_val = 0
            if len(ys) > self.running_average:
                samples_to_average = ys[-running_average:]
                running_average_val = sum(samples_to_average) / len(samples_to_average)
                self.running_averages.append(running_average_val)
                if len(self.running_averages) > len(ys):
                    self.running_averages = self.running_averages[-len(ys):]

            max_val = max(ys)
            min_val = min(ys)
            # print("average = " + str(average) + ", min = " + str(min_val) + ", max = " + str(max_val))
            self.ax1.clear()

            self.ax1.plot(ys, label="Data")
            self.ax1.annotate(str(ys[-1]), xy=(len(ys)-1, ys[-1]))

            self.ax1.plot(self.averages, label="Average")
            self.ax1.annotate(str(average), xy=(len(self.averages)-1, average))

            if len(ys) >= self.running_average:
                self.ax1.plot(self.running_averages, label="Running Average: " + str(self.running_average))
                self.ax1.annotate(str(running_average_val), xy=(len(self.running_averages)-1, running_average_val))

            self.ax1.set_title(str(self.cmd.name))
            self.ax1.legend(loc="upper left")


        else:
            print("Data File Not Found: " + data_file)
            self.data_file_exists = False


if __name__ == '__main__':
    main()
