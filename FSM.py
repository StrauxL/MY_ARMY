#----------------------------------------------------#
# TRUTH TABLE
#----------------------------------------------------#
from pyeda.inter import exprvars, truthtable, espresso_exprs

a, b, c = exprvars('a', 3)  # Creates a[2]=a, a[1]=b, a[0]=c
outputs = "".join(["1" if i in [0, 2, 4, 5, 6] else "0" for i in range(1 << 3)])
truthtable([c, b, a], outputs)

#----------------------------------------------------#
# COMBINATIONAL LOGIC
#----------------------------------------------------#
from sympy.logic import SOPform
from sympy import symbols


simplified_logic = SOPform(symbols(['a', 'b', 'c']), minterms=[0, 2, 4, 5, 6], dontcares = [])
sv_expression = str(simplified_logic)
sv_design = f"""
// ---------------------------------------------
// .sv DESIGN FILE
// ---------------------------------------------
module {"module_name"} (
    input logic {', '.join(['a', 'b', 'c'])},
    output logic y_out
);

    assign y_out = {sv_expression};

endmodule
// ---------------------------------------------
"""



#----------------------------------------------------#
# SEQUENTIAL LOGIC
#----------------------------------------------------#


