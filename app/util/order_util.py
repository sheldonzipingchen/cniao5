# -*- coding: UTF-8 -*-
from app.util.data_validate_util import DataValidate




validator = DataValidate();

def is_legal_product_type(product_type):

    if validator.isInteger(product_type)==False:
        return False

    product_types=[0,1,2,3]

    product_type = int(product_type)
    return product_type in product_types



