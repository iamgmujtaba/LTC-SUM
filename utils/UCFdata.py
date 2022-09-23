import csv, os.path
from config import parse_opts
config = parse_opts()

class UCFDataSet():

    def __init__(self):
        # Get the data.
        self.data = self.get_data()

        # Get the classes.
        self.classes = self.get_classes()

    @staticmethod
    def get_data():
        #Load our data from file.
        with open(os.path.join(config.dataset_path,'data_file.csv'), 'r') as fin:
            reader = csv.reader(fin)
            data = list(reader)
            #print(data)

        return data

    def get_classes(self):
        """Extract the classes from our data. If we want to limit them, only return the classes we need."""
        classes = []
        for item in self.data:
            if item[1] not in classes:
                classes.append(item[1])

        # Sort them.
        classes = sorted(classes)
       
        # Return.
        return classes
        