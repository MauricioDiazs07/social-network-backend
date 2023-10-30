from copy import copy
from typing import List


def simpleOneHot(categories:List, elements:List) -> List:   
    """Docstring.""" 
    # Create a vector initialized with zeros
    one_hot_vector = [0] * len(categories)
    
    # Create empty list to save oneHot encoders
    oneHotEncoders = []
    
    # Get OneHot over each element
    for element in elements:
        #Copy one_hot_vactor
        one_hot = copy(one_hot_vector)
        # Set the corresponding positions to 1 based on the element
        for word in element:
            if word in categories:
                index = categories.index(word)
                one_hot[index] = 1
        #Save on hot
        oneHotEncoders.append(one_hot)
    return oneHotEncoders