
"""standard imports required for all ImageOperation"""
from core.image_operation import ImageOperation
from core.metadata import ImageMetadata, ParameterMetadata
from core.shape import Shape
from core.constants import DataPolicy

"""specific imports required for this function"""
import numpy as np
import skimage as ski
import math

version = "1.0.0"


class CalculateAutoThreshold(ImageOperation):
    
    def __init__(self):
        super().__init__(
            name="Calculate Auto Threshold",
            id="calculate_auto_treshold", 
            category="",
            version="",
            # An explanation to the user of what the function does and what its inputs are
            docs= "Calculates a threshold value from a single image (c=1, z=1) based on one of a number of auto thresholding methods.",
            alerts=None, 

            input_image_metadata={ "input":  ImageMetadata(dtype=DataPolicy.ImageInt, 
                                                  image_shape_constraints=Shape(c=1, z=1, y=-1, x=-1), 
                                                  image_map=Shape(c=0, z=1, y=2, x=3))},
            input_parameter_metadata={"method": ParameterMetadata(dtype=DataPolicy.ValueString, 
                                                                 user_input=True,
                                                                 ui_element="drop-down",
                                                                 ui_element_options={"options":["Sum intensity", "Mean intensity", "Min intensity", "Max intensity" ]})},
            output_parameter_metadata={ "threshold": ParameterMetadata(dtype=DataPolicy.ValueInt)},

            )
        
        self.test_input_parameters = {"method": "Triangle"} 
            
    def execute(self):
        """ get inputs from input dictionaries:"""
        input_image = self.input_image["input"]
        method = self.input_parameter["method"]

        """threshold method names and functions"""
        threshold_methods = {"Li": ski.filters.threshold_li, 
                             "Isodata": ski.filters.threshold_isodata,
                             "Max Entropy": self.MaxEntropy,
                             "Mean": ski.filters.threshold_mean, 
                             "Minimum": ski.filters.threshold_minimum,
                             "Triangle": ski.filters.threshold_triangle,
                             "Otsu": ski.filters.threshold_otsu,
                             "Yen": ski.filters.threshold_yen }
        
        """check method parameter is valid"""
        if method not in threshold_methods.keys():
            raise ValueError(f"invalid threshold method provided")

        threshold = threshold_methods[method](input_image[0][0]).astype(np.uint8)           

        self.output_parameter = {"threshold": threshold}

    def MaxEntropy(self, image):

        """A new method for gray-level picture thresholding using the entropy of the histogram N. Kapur, P.K. Sahoo, A.K.C. Wong"""
        #get N = sum of each histogram bin (should also equal number of pixels in image)
        #n = number of histogram bins (255)

        #for each grey level frequency fi, get pi = fi/N (i = 1 to 256)

        #calculate cumulative probabilities for each potential threshold (t = 1-256) (or 0 - 255?) for foreground (F[t]) and background (B[t]):
        # PB[t] = sum(pi[1 to t])
        # PF[t] = sum(pi[t+1 to n])

        # calculate entropy for foreground and background (only where there's data in the histogram to avoid divide by 0/natural log of 0)
        # EB[t] = - sum { (pi[i]/PB[t])*ln(pi[i]/PB[t])} where i = 1 to t
        # EF[t] = - sum { (pi[i]/PF[t])*ln(pi[i]/PF[t])} where i = t + 1 to 256

        # calculat total entropy 
        # E[t] = EB[t] + EF[t]

        # find the value of t with biggest E

        N = 0
        n = 256

        PI = np.zeros(n)

        PB = np.zeros(n)
        PF = np.zeros(n)

        EB = 0
        EF = 0

        E = 0

        threshold_bin = 0

        histogram, _ = np.histogram(image, bins = 256, range = (0, 256))

        N = histogram.sum()

        for t, bin in enumerate(histogram):
            PI[t] = bin/N

        PB[0] = PI[0]
        PF[0] = 1 - PB[0]


        for t in range(1, n):
            PB[t] = PB[t - 1] + PI[t]
            PF[t] = 1 - PB[t]

        for t in range(1, n):
            EB = 0
            for i in range (0, t):
                if histogram[i] != 0: EB += PI[i]/PB[t] * math.log(PI[i]/PB[t])
            EB = EB * -1

            EF = 0
            for i in range (t + 1, n):
                if histogram[i] != 0: EF += PI[i]/PF[t] * math.log(PI[i]/PF[t])
            EF = EF * -1

            if (EF + EB) > E:
                E = EF + EB
                threshold_bin = t

        return np.uint8(threshold_bin + 1)










