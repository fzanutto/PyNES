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
    cycle = i[74:]

    neslog_line = neslog_file.readline()

    if neslog_line == "":
        print('OK')
        break

    diffs = []

    if opcode != neslog_line[0:5]:
        diffs.append("OPCODE - expected: {} - actual: {}\n".format(neslog_line[0:5], opcode))

    if bytes != neslog_line[6:15]:
        diffs.append("BYTES - expected: {} - actual: {}\n".format(neslog_line[6:15], bytes))

    if instruction_str != neslog_line[16:20]:
        diffs.append("INSTR - expected: {} - actual: {}\n".format(neslog_line[16:20], instruction_str))

    if regs != neslog_line[48:68]:
        diffs.append("REGS - expected: {} - actual: {}\n".format(neslog_line[48:68], regs))

    if cycle != neslog_line[86:]:
        diffs.append("CYCLE - expected: {} - actual: {}\n".format(neslog_line[86:], cycle))

    if len(diffs) > 0:
        print(*diffs)
        break
