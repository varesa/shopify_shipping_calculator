#
# Project: Shopify shipping calculator
# Copyright 2014 - 2015 Esa Varemo <esa@kuivanto.fi>
# Unauthorized use or copying of this file is prohibited
#


from pyramid.view import view_config

from shipping.models import DBSession, ShippingCostIrtotavara


def string_to_float_or_zero(string):
    """
    Try to convert a string to an float, returns 0.0 on failure
    :param string: String to convert
    :type string: str
    :return: float value of the string or 0.0
    :rtype: float
    """
    try:
        return float(string)
    except ValueError:
        return 0


@view_config(route_name='data_costs', renderer='../../templates/data_costs.pt')
def view_data_costs(request):
    if len(request.POST):
        if len(DBSession.query(ShippingCostIrtotavara).all()):
            costs = DBSession.query(ShippingCostIrtotavara).first()
        else:
            costs = ShippingCostIrtotavara()
            DBSession.add(costs)

        costs.range1_cost = string_to_float_or_zero(request.POST['range1_cost'])
        costs.range1_end  = string_to_float_or_zero(request.POST['range1_end'])
        costs.range2_cost = string_to_float_or_zero(request.POST['range2_cost'])
        costs.range2_end  = string_to_float_or_zero(request.POST['range2_end'])
        costs.range3_cost = string_to_float_or_zero(request.POST['range3_cost'])

    return {
        'costs': DBSession.query(ShippingCostIrtotavara).first()
    }