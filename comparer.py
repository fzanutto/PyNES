neslog_file = open('nestest.log.txt')
out_file = open('out.txt', 'r')

ind = 0
while True:
    i = out_file.readline()

    ind += 1
    opcode = i[0:5]
    bytes = i[6:15]
    instruction_str = i[16:20]
    regs = i[48:68]

    neslog_line = neslog_file.readline()

    if neslog_line == "":
        print('OK')
        break

    v1 = opcode != neslog_line[0:5]
    v2 = bytes != neslog_line[6:15]
    v3 = instruction_str != neslog_line[16:20]
    v4 = regs != neslog_line[48:68]

    if v1 or v2 or v3 or v4:
        print(ind, v1, v2, v3, v4)
        break
