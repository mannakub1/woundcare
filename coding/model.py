from cntk.ops.functions import load_model

class Model :

    def load(self, path) :
        return load_model(path)
