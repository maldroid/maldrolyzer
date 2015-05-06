from templates import Plugin

class Androrat(Plugin):
    NAME = 'Androrat'

    def recon(self):
        for cls in self.dvm.get_classes():
            if 'Lmy/app/client/ProcessCommand;'.lower() in cls.get_name().lower():
                self.process_class = cls
                return True
        return False

    def extract(self):
        c2Found = False
        portFound = False
        c2 = ""
        port = ""
        string = None
        for method in self.process_class.get_methods():
            if method.name == 'loadPreferences':
                for inst in method.get_instructions():
                    if inst.get_name() == 'const-string':
                        string = inst.get_output().split(',')[-1].strip(" '")
                        if c2Found == True:
                            c2 = string
                            c2Found = False
                        if string == 'ip':
                            c2Found = True
                        if string == 'port':
                            portFound = True
                    if inst.get_name() == 'const/16':
                        if portFound == True:
                            string = inst.get_output().split(',')[-1].strip(" '")
                            port = string
                    if c2 and port:
                        break

        server = ""
        if port:
            server = "{0}:{1}".format(c2, str(port))
        else:
            server = c2

        return {'c2': [server]}

