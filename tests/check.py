from subprocess import run
from subprocess import PIPE
from xml.dom import minidom
from tabulate import tabulate


# executes a shell command
def execute(cmd=[], shell=False, timeout=10):
    return run(cmd, shell=shell, stdout=PIPE, stderr=PIPE, timeout=timeout)


# reads a file
def read(filename):
    f = open(filename, 'r')
    text = f.read()
    f.close()
    return text.strip()


# creates a pretty result report
def create_report(table):
    return tabulate(table, headers=['Exercise', 'Grade', 'Message'])


# checks ex0.circ
def check_ex0():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ex0.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip()
    expected = read('tests/expected/ex0')
    if output == expected:
        return (25, 'passed', '')
    else:
        return (0, 'failed', '')


# checks ex1.circ
def check_ex1():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ex1.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())

    # check used components
    tree = minidom.parse('ex1.circ')
    valid_gates = ['and gate', 'or gate', 'not gate', 'pin', 'text', 'splitter', 'tunnel', 'probe']
    for circuit in tree.getElementsByTagName('circuit'):
        for component in circuit.getElementsByTagName('comp'):
            name = component.getAttribute('name').lower()
            lib = component.getAttribute('lib')
            if name not in valid_gates and lib != '':
                return (0, 'do not use invalid gates', '')

    # parses logisim output
    def parse(txt):
        a = []
        b = []
        c = []
        d = []
        e = []
        for line in txt.split('\n'):
            line = line.split('\t')
            a.append(line[0][3])
            b.append(line[0][4])
            c.append(line[0][5])
            d.append(line[1][3])
            e.append(line[2][7])
        return (tuple(a), tuple(b), tuple(c), tuple(d), tuple(e))
    # compare
    output = parse(task.stdout.decode().strip())
    expected = parse(read('tests/expected/ex1'))
    lookup = {0: 'NAND', 1: 'NOR', 2: 'XOR', 3: '2-1 MUX', 4: '4-1 MUX'}
    wrong = []
    grade = 0
    for i, (o, e) in enumerate(zip(output, expected)):
        if o == e:
            grade += 5
        else:
            wrong.append(lookup[i])
    if len(wrong) == 0:
        return (grade, 'passed', '')
    elif len(wrong) == 5:
        return (0, 'failed', '')
    else:
        return (grade, 'failed: ' + ','.join(wrong), '')


# checks ex2.circ
def check_ex2():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ex2.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip()
    expected = read('tests/expected/ex2')
    if output == expected:
        return (25, 'passed', '')
    else:
        return (0, 'failed', '')


# checks ex3.circ
def check_ex3():
    task = execute(cmd=['java', '-jar', 'tests/logisim.jar', '-tty', 'table', 'tests/ex3.circ'])
    if task.returncode != 0:
        return (0, 'runtime error', task.stderr.decode().strip())
    output = task.stdout.decode().strip()
    expected = read('tests/expected/ex3')
    if output == expected:
        return (25, 'passed', '')
    else:
        return (0, 'failed', '')


# checks lab 5
def lab5_logisim():
    ex0_result = check_ex0()
    ex1_result = check_ex1()
    ex2_result = check_ex2()
    ex3_result = check_ex3()
    table = []
    table.append(('0. The basics (Warm-Up)', *ex0_result[0: 2]))
    table.append(('1. Sub-Circuits', *ex1_result[0: 2]))
    table.append(('2. Storing State', *ex2_result[0: 2]))
    table.append(('3. FSMs to Digital Logic', *ex3_result[0: 2]))
    errors = ex0_result[2]
    errors += '\n' + ex1_result[2]
    errors += '\n' + ex2_result[2]
    errors += '\n' + ex3_result[2]
    errors = errors.strip()
    grade = 0
    grade += ex0_result[0]
    grade += ex1_result[0]
    grade += ex2_result[0]
    grade += ex3_result[0]
    grade = min(grade, 100)
    report = create_report(table)
    if errors != '':
        report += '\n\nMore Info:\n\n' + errors
    print(report)
    print('\n=> Score: %d/100' % grade)


if __name__ == '__main__':
    lab5_logisim()
