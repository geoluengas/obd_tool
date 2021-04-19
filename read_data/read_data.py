import random
import os
import obd
import time
import threading
from obd.OBDResponse import Monitor
from obd.utils import BitArray


def main():
    time.strftime('%X %x %Z')
    # obd.logger.setLevel(obd.logging.DEBUG)
    connection = obd.OBD("/dev/ttys001")  # auto-connects to USB or RF port
    reader = DataReader(connection)
    # t1 = threading.Thread(target=reader.read_cmds, args=(999, 1, True, 0.05))
    # t1.start()
    reader.read_cmds(5, 1, False, 1)


class DataReader():
    def __init__(self, connection, f_dir="/tmp/", f_extension="obd_elm_data"):
        for c in connection.supported_commands:
            print(c.name)
        self.connection = connection
        self.cmds = connection.supported_commands
        self.f_dir = f_dir
        self.f_extension = f_extension
        self.clean_files()

    def clean_files(self):
        test = os.listdir(self.f_dir)
        for item in test:
            if item.endswith(self.f_extension):
                print("Deleting existing file" + str(os.path.join(self.f_dir, item)))
                os.remove(os.path.join(self.f_dir, item))

    def write_file(self, file, line, max_lines=100):
        f = open(file, "a")
        f.write(str(line) + "\n")
        f.close()

        with open(file, 'r') as fin:
            data = fin.read().splitlines(True)
            # print("lines = " + str(len(data)))
        if len(data) >= max_lines:
            with open(file, 'w') as fout:
                fout.writelines(data[1:])

    def read_cmd(self, cmd, randomize=False, rand_perc=0.1):
        if self.connection.is_connected():
            response = self.connection.query(cmd)  # send the command, and parse the response
            value = "unknown"
            units = "unkown"
            print("### " + str(cmd.name) + ":\t" + str(response) + "\t[" + str(type(response)) + "]\t[" +
                  str(cmd.decode) + "]")
            if response.value is None:
                print("NONE!!")
                print(str(self.cmds))
                self.cmds.remove[str(cmd.name)]
            if isinstance(response.value, str):
                # print("STRING!")
                value = response.value
                units = "string"
            elif (response.value is None) \
                    or isinstance(response.value, BitArray) \
                    or isinstance(response.value, Monitor) \
                    or isinstance(response.value, list):
                # TODO handle these types
                # print("*** Unhandled Type : " + str(type(response.value)) + "***")
                # print(response.value)
                value = "unknown"
                units = "unkown"
            else:
                value = response.value.magnitude
                if randomize:
                    value = int(value)
                    value = random.randint(int(value - (value * rand_perc)), int(value + (value * rand_perc)))
                units = response.value.units
            r_response = {'value': value, 'units': units, 'command': response.command}
            # print(r_response)
            f_name = str(response.command.name + "." + self.f_extension)
            f_name = self.f_dir + f_name
            # print(f_name)
            self.write_file(f_name, value)
            return r_response
        else:
            print("No connection to " + str(self.connection))

    def read_cmds(self, iterations=999, interval=1, randomize=False, rand_perc=0.05):
        i = 0
        while i < iterations and self.connection.is_connected():
            # print("Run : " + str(i))
            for cmd in self.cmds:
                # print("CMD " + cmd.name)
                self.read_cmd(cmd, randomize, rand_perc)
            i += 1
            time.sleep(interval)


if __name__ == '__main__':
    main()
