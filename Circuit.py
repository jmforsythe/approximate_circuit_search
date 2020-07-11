import sys
import itertools

class Gate:
    evaluated = False
    input_gates = []
    output = 0
    
    def __init__(self, input_gates, function, position):
        self.input_gates = input_gates
        self.function = function
        self.position = position

    def __repr__(self):
        return str(self)
    def __str__(self):
        return str(self.position) + " = [" + str(self.input_gates[0].position) + " " + str(self.function.__name__) + " " + str(self.input_gates[1].position) + "]"

    def evaluate(self):
        function_inputs = []
        for gate in self.input_gates:
            if gate.evaluated == False:
                gate.evaluate()
                gate.evaluated = True
            function_inputs += [gate.get_output()]
        self.set_output(self.function(function_inputs))

    def set_output(self, output):
        self.output = output

    def get_output(self):
        return self.output

    def clear(self):
        self.evaluated = False

class Input(Gate):
    def __str__(self):
        return str(self.position) + " = [" + str(self.output) + "]"
    
    evaluated = True
    output = 0
    
    def __init__(self, position):
        self.position = position

    def clear(self):
        pass

    def evaluate(self):
        pass    


class Circuit:
    def __repr__(self):
        return str(self)
    def __str__(self):
        string = ""
        for gate in self.gates:
            string += str(gate) + "\n"
        string += "Outputs are: " + str(self.output_seed)
        return string
    
    #function_dict should be an object containing the functions and a dictionary mapping numbers to them
    def __init__(self, n_inputs, n_outputs, n_columns, n_rows, function_dict, seed):
        main_seed = seed[:-n_outputs]
        self.output_seed = seed[-n_outputs:]
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.n_columns = n_columns
        self.n_rows = n_rows
        self.function_dict = function_dict
        self.seed = seed

        self.gates = []
        for i in range(n_inputs):
            self.gates += [Input(i)]
        
        #If modified to take functions with different number of inputs, consider partitioning seed into each gate

        for column in range(n_columns):
            for row in range(n_rows):
                position = (n_rows * column) + row
                self.gates += [Gate([self.gates[seed[position * 3]], self.gates[seed[position * 3 + 1]]],
                                    function_dict.function_dict[seed[position * 3 + 2]], position + self.n_inputs)]


    def set_inputs(self, inputs):
        for i in range(len(inputs)):
            self.gates[i].set_output(inputs[i])

    def set_inputs_reversed(self, inputs):
        self.set_inputs(inputs[::-1])

    def get_inputs(self):
        inputs = []
        for i in range(self.n_inputs):
            inputs.append(self.gates[i])
        return inputs

    def execute(self):
        outputs = []
        for output_gate_index in self.output_seed:
            output_gate = self.gates[output_gate_index]
            output_gate.evaluate()
            #outputs += [output_gate.position]
            outputs += [output_gate.get_output()]
        self.clear()
        return outputs

    def clear(self):
        for gate in self.gates:
            gate.clear()


if __name__ == "__main__":
    class Function_dict:
        def AND(self, x):
            return int(x[0] and x[1])
        def OR(self, x):
            return int(x[0] or x[1])
        def NAND(self, x):
            return int(not x[0] and x[1])
        def NOR(self, x):
            return int(not x[0] or x[1])
        def XOR(self, x):
            return int(x[0] != x[1])
        def XNOR(self, x):
            return int(x[0] == x[1])
        def ANDONENEG(self, x):
            return int(x[0] and not x[1])

        def __init__(self):
            self.function_dict = {
                "AND;" : self.AND,
                "OR;"  : self.OR,
                "XOR;" : self.XOR,
                "NAND;": self.NAND,
                "NOR;" : self.NOR,
                "XNOR;": self.XNOR
            }

    n_inputs = 4
    n_outputs = 3
    n_columns = 3
    n_rows = 2

    seed = [0, 0, 'OR;', 1, 2, 'NAND;', 2, 2, 'AND;', 5, 2, 'NAND;', 0, 0, 'XOR;', 1, 3, 'NOR;', 1, 4, 5]
    function_dict = Function_dict()

    x = Circuit(n_inputs, n_outputs, n_columns, n_rows, function_dict, seed)

    print(str(x))

    ##input_list = [list(tup)[::-1] for tup in itertools.product([0, 1], repeat=4)]
    ##
    ##
    ##for i in input_list:
    ##    x.set_inputs(i)
    ##    print(str(i) + " --> " + str(x.execute()))

    num_inputs = 4

    for i in range(2**(num_inputs//2)):
        for j in range(2**(num_inputs//2)):
            input_a = [int(x) for x in list(format(i, "#0{0}b".format(2 + num_inputs//2))[2:])]
            input_b = [int(x) for x in list(format(j, "#0{0}b".format(2 + num_inputs//2))[2:])]
            inputs = input_a + input_b
            x.set_inputs(inputs)
            #print("    " + str(i) + " * " + str(j) + "    --> " + str(i*j))
            print(str(inputs) + " --> " + str(x.execute()))

