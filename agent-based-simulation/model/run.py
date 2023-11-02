from evacuation_model import EvacuationModel
import numpy as np
import seaborn as sns

model = EvacuationModel(5, 5, 2, 20, 0.5)
for i in range(20):
    model.step()

