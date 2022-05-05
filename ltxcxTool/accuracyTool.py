import json
from ltxcxTool.preset import Preset


class CXTester:
    valid_cards = ['ddp', 'ovi', 'vi16', 'vi16b']


    def __init__(self, specFile):
        with open(specFile, 'r') as jf:
            self.tester = json.load(jf)
    

    def get_full_specs(self):
        return self.tester


    def ovi_calc_force_v(self, force_v, range_v):
        # print('+ Calculate OVI force V accuracy.')
        rv_index = None

        if range_v in self.tester['spec']['ovi']['fv']['range']:
            rv_index = self.tester['spec']['ovi']['fv']['range'].index(range_v)
            min_valid_val = -self.tester['spec']['ovi']['fv']['range_val'][rv_index]
            max_valid_val = self.tester['spec']['ovi']['fv']['range_val'][rv_index]

            if min_valid_val <= force_v <= max_valid_val:
                v_accuracy = self.tester['spec']['ovi']['fv']['value_accuracy']
                r_accuracy = self.tester['spec']['ovi']['fv']['range_accuracy']
                range_value = self.tester['spec']['ovi']['fv']['range_val'][rv_index]

                v_error = [force_v*i*0.01 for i in v_accuracy]
                r_error = [range_value*i*0.01 for i in r_accuracy]
                value = [force_v+v_error[0]+r_error[0], force_v+v_error[1]+r_error[1]]

                output = {
                    'voltage_error': v_error,
                    'range_error': r_error,
                    'value': value
                }
                return output
            else:
                return None
        else:
            return None


    def vi16_calc_force_v(self, force_v, range_v):
        # print('+ Calculate VI16 force V accuracy.')
        rv_index = None

        if range_v in self.tester['spec']['vi16']['fv']['range']:
            rv_index = self.tester['spec']['vi16']['fv']['range'].index(range_v)
            min_valid_val = -self.tester['spec']['vi16']['fv']['range_val'][rv_index]
            max_valid_val = self.tester['spec']['vi16']['fv']['range_val'][rv_index]

            if min_valid_val <= force_v <= max_valid_val:
                v_accuracy = self.tester['spec']['vi16']['fv']['value_accuracy']
                r_accuracy = self.tester['spec']['vi16']['fv']['range_accuracy']
                range_value = self.tester['spec']['vi16']['fv']['range_val'][rv_index]

                v_error = [force_v*i*0.01 for i in v_accuracy]
                r_error = [range_value*i*0.01 for i in r_accuracy]
                value = [force_v+v_error[0]+r_error[0], force_v+v_error[1]+r_error[1]]

                output = {
                    'voltage_error': v_error,
                    'range_error': r_error,
                    'value': value
                }
                return output
            else:
                return None
        else:
            return None


    def ovi_calc_measure_v(self, measure_v, range_v):
        # print('+ Calculate OVI measure V accuracy.')
        rv_index = None

        if range_v in self.tester['spec']['ovi']['mv']['range']:
            rv_index = self.tester['spec']['ovi']['mv']['range'].index(range_v)
            min_valid_val = -self.tester['spec']['ovi']['mv']['range_val'][rv_index]
            max_valid_val = self.tester['spec']['ovi']['mv']['range_val'][rv_index]

            if min_valid_val <= measure_v <= max_valid_val:
                v_accuracy = self.tester['spec']['ovi']['mv']['value_accuracy']
                r_accuracy = self.tester['spec']['ovi']['mv']['range_accuracy']
                range_value = self.tester['spec']['ovi']['mv']['range_val'][rv_index]

                v_error = [measure_v*i*0.01 for i in v_accuracy]
                r_error = [range_value*i*0.01 for i in r_accuracy]
                value = [measure_v+v_error[0]+r_error[0], measure_v+v_error[1]+r_error[1]]

                output = {
                    'voltage_error': v_error,
                    'range_error': r_error,
                    'value': value
                }
                return output
            else:
                return None
        else:
            return None


    def vi16_calc_measure_v(self, measure_v, range_v):
        # print('+ Calculate VI16 measure V accuracy.')
        rv_index = None

        if range_v in self.tester['spec']['vi16']['mv']['range']:
            rv_index = self.tester['spec']['vi16']['mv']['range'].index(range_v)
            min_valid_val = -self.tester['spec']['vi16']['mv']['range_val'][rv_index]
            max_valid_val = self.tester['spec']['vi16']['mv']['range_val'][rv_index]

            if min_valid_val <= measure_v <= max_valid_val:
                v_accuracy = self.tester['spec']['vi16']['mv']['value_accuracy']
                if range_v == '2V':
                    r_accuracy = self.tester['spec']['vi16']['mv']['range_accuracy_2v']
                else:
                    r_accuracy = self.tester['spec']['vi16']['mv']['range_accuracy']
                range_value = self.tester['spec']['vi16']['mv']['range_val'][rv_index]

                v_error = [measure_v*i*0.01 for i in v_accuracy]
                r_error = [range_value*i*0.01 for i in r_accuracy]
                value = [measure_v+v_error[0]+r_error[0], measure_v+v_error[1]+r_error[1]]

                output = {
                    'voltage_error': v_error,
                    'range_error': r_error,
                    'value': value
                }
                return output
            else:
                return None
        else:
            return None


    def ovi_calc_force_i(self, force_i, measure_v, range_i):
        # print('+ Calculate OVI force I accuracy.') 
        ri_index = None

        if range_i in self.tester['spec']['ovi']['fi']['range']:
            ri_index = self.tester['spec']['ovi']['fi']['range'].index(range_i)
            min_valid_val = -self.tester['spec']['ovi']['fi']['range_val'][ri_index]
            max_valid_val = self.tester['spec']['ovi']['fi']['range_val'][ri_index]

            if min_valid_val <= force_i <= max_valid_val:
                i_accuracy = self.tester['spec']['ovi']['fi']['value_accuracy'][f'{range_i}']
                r_accuracy = self.tester['spec']['ovi']['fi']['range_accuracy'][f'{range_i}']
                rpv_accuracy = self.tester['spec']['ovi']['fi']['range_pervolt_accuracy'][f'{range_i}']
                range_value = self.tester['spec']['ovi']['fi']['range_val'][ri_index]

                i_error = [force_i*i*0.01 for i in i_accuracy]
                r_error = [range_value*i*0.01 for i in r_accuracy]
                rpv_error = [measure_v*range_value*i*0.01 for i in rpv_accuracy]
                value = [force_i+i_error[0]+r_error[0]+rpv_error[0], force_i+i_error[1]+r_error[1]+rpv_error[1]]

                output = {
                    'current_error': i_error,
                    'range_error': r_error,
                    'range_pervolt_error': rpv_error,
                    'value': value
                }
                return output
            else:
                return None
        else:
            return None


    def vi16_calc_force_i(self, force_i, measure_v, range_i):
        # print('+ Calculate VI16 force I accuracy.') 
        ri_index = None

        if range_i in self.tester['spec']['vi16']['fi']['range']:
            ri_index = self.tester['spec']['vi16']['fi']['range'].index(range_i)
            min_valid_val = -self.tester['spec']['vi16']['fi']['range_val'][ri_index]
            max_valid_val = self.tester['spec']['vi16']['fi']['range_val'][ri_index]

            if min_valid_val <= force_i <= max_valid_val:
                i_accuracy = self.tester['spec']['vi16']['fi']['value_accuracy'][f'{range_i}']
                r_accuracy = self.tester['spec']['vi16']['fi']['range_accuracy'][f'{range_i}']
                rpv_accuracy = self.tester['spec']['vi16']['fi']['range_pervolt_accuracy'][f'{range_i}']
                range_value = self.tester['spec']['vi16']['fi']['range_val'][ri_index]

                i_error = [force_i*i*0.01 for i in i_accuracy]
                r_error = [range_value*i*0.01 for i in r_accuracy]
                rpv_error = [measure_v*range_value*i*0.01 for i in rpv_accuracy]
                value = [force_i+i_error[0]+r_error[0]+rpv_error[0], force_i+i_error[1]+r_error[1]+rpv_error[1]]

                output = {
                    'current_error': i_error,
                    'range_error': r_error,
                    'range_pervolt_error': rpv_error,
                    'value': value
                }
                return output
            else:
                return None
        else:
            return None


    def ovi_calc_measure_i(self, measure_i, force_v, range_i):
        # print('+ Calculate OVI measure I accuracy.')
        ri_index = None

        if range_i in self.tester['spec']['ovi']['fi']['range']:
            ri_index = self.tester['spec']['ovi']['fi']['range'].index(range_i)
            min_valid_val = -self.tester['spec']['ovi']['fi']['range_val'][ri_index]
            max_valid_val = self.tester['spec']['ovi']['fi']['range_val'][ri_index]

            if min_valid_val <= measure_i <= max_valid_val:
                i_accuracy = self.tester['spec']['ovi']['mi']['value_accuracy'][f'{range_i}']
                r_accuracy = self.tester['spec']['ovi']['mi']['range_accuracy'][f'{range_i}']
                rpv_accuracy = self.tester['spec']['ovi']['mi']['range_pervolt_accuracy'][f'{range_i}']
                range_value = self.tester['spec']['ovi']['mi']['range_val'][ri_index]

                i_error = [measure_i*i*0.01 for i in i_accuracy]
                r_error = [range_value*i*0.01 for i in r_accuracy]
                rpv_error = [force_v*range_value*i*0.01 for i in rpv_accuracy]
                value = [measure_i+i_error[0]+r_error[0]+rpv_error[0], measure_i+i_error[1]+r_error[1]+rpv_error[1]]

                output = {
                    'current_error': i_error,
                    'range_error': r_error,
                    'range_pervolt_error': rpv_error,
                    'value': value
                }
                return output
            else:
                return None
        else:
            return None


    def vi16_calc_measure_i(self, measure_i, force_v, range_i):
        # print('+ Calculate VI16 measure I accuracy.')
        ri_index = None

        if range_i in self.tester['spec']['vi16']['fi']['range']:
            ri_index = self.tester['spec']['vi16']['fi']['range'].index(range_i)
            min_valid_val = -self.tester['spec']['vi16']['fi']['range_val'][ri_index]
            max_valid_val = self.tester['spec']['vi16']['fi']['range_val'][ri_index]

            if min_valid_val <= measure_i <= max_valid_val:
                i_accuracy = self.tester['spec']['vi16']['mi']['value_accuracy'][f'{range_i}']
                r_accuracy = self.tester['spec']['vi16']['mi']['range_accuracy'][f'{range_i}']
                rpv_accuracy = self.tester['spec']['vi16']['mi']['range_pervolt_accuracy'][f'{range_i}']
                range_value = self.tester['spec']['vi16']['mi']['range_val'][ri_index]

                i_error = [measure_i*i*0.01 for i in i_accuracy]
                r_error = [range_value*i*0.01 for i in r_accuracy]
                rpv_error = [force_v*range_value*i*0.01 for i in rpv_accuracy]
                value = [measure_i+i_error[0]+r_error[0]+rpv_error[0], measure_i+i_error[1]+r_error[1]+rpv_error[1]]

                output = {
                    'current_error': i_error,
                    'range_error': r_error,
                    'range_pervolt_error': rpv_error,
                    'value': value
                }
                return output
            else:
                return None
        else:
            return None




# used for debug only
if __name__ == "__main__":
    cx_tester = CXTester()
    buf = cx_tester.get_full_specs()

    fv = 1.0        # force voltage value
    mv = 1.0        # measure voltage value
    rv = '16V'      # force voltage range

    fi = 100e-6     # force current value
    mi = 700e-6     # measure current value
    ri = '500uA'    # measure current range

    print('Resource: OVI')
    print(f'Force Voltage Value : {fv}')
    print(f'Force Voltage Value : {fv}')
    # print(f'Measure Current Value : {mi}')
    print(f'Measure Current Range : {ri}')
    
    # result = cx_tester.ovi_calc_force_v(fv, rv)
    result = cx_tester.ovi_calc_measure_v(mv, rv)
    # result = cx_tester.ovi_calc_force_i(fi, mv, ri)
    # result = cx_tester.ovi_calc_measure_i(mi, fv, ri)
    if result:
        for key in result:
            print(f'{key}: {result[key]}')
    else:
        print('Invalid arguments')

