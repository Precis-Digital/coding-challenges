def parse_instructions(s):
    return list(map(int, s.split(',')))

def run_program(instructions: list[int]):
    for i in range(0, len(instructions), 4):
        if instructions[i] == 99:
            break
        [op_code, input_pos_1, input_pos_2, output_pos] = instructions[i:(i + 4)]
        if op_code == 1:
            instructions[output_pos] = instructions[input_pos_1] + instructions[input_pos_2]
        elif op_code == 2:
            instructions[output_pos] = instructions[input_pos_1] * instructions[input_pos_2]


def day_2_1():
    input_1 = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,5,19,23,1,6,23,27,1,27,10,31,1,31,5,35,2,10,35,39,1,9,39,43,1,43,5,47,1,47,6,51,2,51,6,55,1,13,55,59,2,6,59,63,1,63,5,67,2,10,67,71,1,9,71,75,1,75,13,79,1,10,79,83,2,83,13,87,1,87,6,91,1,5,91,95,2,95,9,99,1,5,99,103,1,103,6,107,2,107,13,111,1,111,10,115,2,10,115,119,1,9,119,123,1,123,9,127,1,13,127,131,2,10,131,135,1,135,5,139,1,2,139,143,1,143,5,0,99,2,0,14,0"
    instructions = parse_instructions(input_1)
    instructions[1] = 12
    instructions[2] = 2
    run_program(instructions=instructions)
    return instructions[0]

def day_2_2():
    input_1 = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,5,19,23,1,6,23,27,1,27,10,31,1,31,5,35,2,10,35,39,1,9,39,43,1,43,5,47,1,47,6,51,2,51,6,55,1,13,55,59,2,6,59,63,1,63,5,67,2,10,67,71,1,9,71,75,1,75,13,79,1,10,79,83,2,83,13,87,1,87,6,91,1,5,91,95,2,95,9,99,1,5,99,103,1,103,6,107,2,107,13,111,1,111,10,115,2,10,115,119,1,9,119,123,1,123,9,127,1,13,127,131,2,10,131,135,1,135,5,139,1,2,139,143,1,143,5,0,99,2,0,14,0"
    instructions = parse_instructions(input_1)
    ctr = 0
    for i in range(0, len(instructions)):
        for j in range(0, len(instructions)):
            ctr += 1
            instructions_copy = instructions[:]
            instructions_copy[1] = i
            instructions_copy[2] = j
            run_program(instructions=instructions_copy)
            if instructions_copy[0] == 19690720:
                print(ctr)
                return 100 * i + j



if __name__ == "__main__":
    print(day_2_2())
