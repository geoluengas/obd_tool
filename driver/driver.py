import read_data.read_data as rd
import plot_data.live_plot as pd
import time
import obd
import threading
import matplotlib.pyplot as plt


def main():
    time.strftime('%X %x %Z')
    # obd.logger.setLevel(obd.logging.DEBUG)
    connection = obd.OBD("/dev/ttys002")  # auto-connects to USB or RF port
    # cmds = {obd.commands.SPEED}
    # cmds = connection.supported_commands
    reader = rd.DataReader(connection)
    t1 = threading.Thread(target=reader.read_cmds, args=(999, 1, False, 0.05))
    t1.start()
    live_plot1 = pd.LivePlot(obd.commands.RPM, samples)
    live_plot2 = pd.LivePlot(obd.commands.SPEED, samples)
    live_plot3 = pd.LivePlot(samples=samples)
    plt.show()

    t1.join()


if __name__ == '__main__':
    main()
