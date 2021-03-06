import configparser
import getpass
import pymysql
import distro


class Decorators:
    # Question now is: Why would you use this decorator if you can just call the method?
    # It doesn't interact with the variables..
    @staticmethod
    def determine_environment(func):
        def wrapper(*args, **kwargs):
            sensitive_configuration = configparser.ConfigParser()
            try:
                sensitive_configuration.read("./settings/sensitive.ini")
                if not sensitive_configuration.sections():
                    print(
                        "Could not read sensitive configuration file. You need your own credentials to launch this program"
                    )
                else:
                    global_configuration = configparser.ConfigParser()
                    global_configuration.read("./settings/configuration.ini")
                    if (
                        getpass.getuser()
                        == sensitive_configuration["PRODUCTION"]["ServerUser"]
                    and distro.linux_distribution()[0] == sensitive_configuration['PRODUCTION']['Distribution']):
                        if (
                            global_configuration["DEFAULT"]["ActiveEnvironment"]
                            != "PRODUCTION"
                        ):
                            global_configuration["DEFAULT"][
                                "ActiveEnvironment"
                            ] = "PRODUCTION"
                            with open("./settings/configuration.ini", "w") as conf:
                                global_configuration.write(conf)
                            print("environment set to: PRODUCTION")
                    elif (
                        global_configuration["DEFAULT"]["ActiveEnvironment"] != "LOCAL"
                    ):
                        global_configuration["DEFAULT"]["ActiveEnvironment"] = "LOCAL"
                        with open("./settings/configuration.ini", "w") as conf:
                            global_configuration.write(conf)
                        print("environment set to: LOCAL")
            except Exception as ex:
                print("failed to determine environment")
                print(ex)
            return func(*args, **kwargs)

        return wrapper
