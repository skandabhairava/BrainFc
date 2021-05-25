import sys, getopt, os, time

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('bf.py -i <inputfile>\n')
        print('Optional commands :\n-o <outputfile>   -   to record the output')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('bf.py -i <inputfile>\n')
            print('Optional commands :\n-o <outputfile>   -   to record the output')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg
   #print('Input file is : ', inputfile)
   #print('Output file is : ', outputfile)
    if inputfile == '':
        print('bf.py -i <inputfile>\n')
        print('Optional commands :\n-o <outputfile>   -   to record the output')
        sys.exit()
    else:
        file_name_inp, file_extension_inp = os.path.splitext(inputfile)
        file_name_out, file_extension_out = os.path.splitext(outputfile)
        if file_extension_inp != '.bf':
            print("Input file should a .bf file")
            sys.exit()
        else:
            parse_ignore(inputfile, file_name_out)
    
def parse_ignore(inputfile, ouput):
    data = ""
    code = ""
    for_bracket_indexes = {}
    in_file = open(inputfile,mode="r")
    data = in_file.read()
    in_file.close()
    #parsing
    keywords=["+", "-", "<", ">", "[", "]", ".", ","]
    for char in data:
        if (len(list(filter (lambda x : x == char, keywords))) > 0) :
            code = code + char
    for_code = code
    #forloop [] detection
    while True:
        try:
            i = for_code.index("[")
            try:
                f = for_code[i+1:].index("]")
            except Exception as hh:
                print("Trying to enter loop, without exit\nLine : ", i)
                sys.exit()
        except Exception as e:
            break
        for_bracket_indexes[str(i)] = -5
        #for_code = for_code[i+1:]
        c=i+1
        bracket = 1
        while c < len(for_code):
            #print(for_code[c])
            if for_code[c] == "[":
                bracket += 1
                #print("bracket : ", bracket)
            elif for_code[c] == "]":
                bracket -= 1
                #print("bracket : ", bracket)
            if bracket == 0:
                #print("bracket : ", bracket)
                for_bracket_indexes[str(i)] = c
                for_code = for_code[:i] + "o" + for_code[i+1:]
                for_code = for_code[:c] + "c" + for_code[c+1:]
                break
            #time.sleep(4)
            c+=1
        if bracket != 0:
            print("Trying to enter loop, without exit\nLine : ", i)
            sys.exit()
        #print("finished going thru whole code, going back into forever")

    try:
        i = for_code.index("]")
        print("Trying to exit out of loop, without entry\nLine : ", i)
        sys.exit()
    except Exception as e:
        pass

    #print(code, for_code, for_bracket_indexes)

    #print(code)
    if ouput != '':
        compiler(code, ouput,for_loop_indexes=for_bracket_indexes)
    else:
        compiler(code,for_loop_indexes=for_bracket_indexes)

def extend_ma(arr):
    arr.append(0)
    return arr

def accept_input(save_location):
    try:
        inp = input()
        inp = inp[0]
        ascii = ord(inp)
    except Exception as e:
        print("An exception occurred : ", e)
        sys.exit()
    #print(inp, "  ", ascii)
    if save_location != '':
        save_location = save_location + ".log"
        try:
            out_file = open(save_location,mode="a")
            stt = "input : " + inp + "; ascii : " + str(ascii) + "\n"
            out_file.write(stt)
            out_file.close()
        except Exception as e:
            print("An exception occurred while saving log : ", e)
    return ascii

def output(cell_info,save_location=''):
    print(chr(cell_info),end='')
    if save_location != '':
        save_location = save_location + ".log"
        try:
            out_file = open(save_location,mode="a")
            stt = "ouput : " + chr(cell_info) + "\n"
            out_file.write(stt)
            out_file.close()
        except Exception as e:
            print("An exception occurred while saving log : ", e)

    
def compiler(code, save_location='', for_loop_indexes={}):
    start_time = time.time()
    main_stack = [0]
    current_cell_info = 0
    pointer_stack = 0
    pointer_code = 0
    i = 0 #pointer_code substitute, total executel lines
    loop_stack_count = []
    #loop
    while i < len(code):
        ptr_code = code[i]
        #temp
        #print(ptr_code)
        if ptr_code == '>':
            pointer_stack += 1
            try:
                current_cell_info = main_stack[pointer_stack]
            except Exception as e:
                main_stack = extend_ma(main_stack)
                try:
                    current_cell_info = main_stack[pointer_stack]
                except Exception as f:
                    print("An exception occurred : ", f)
                    print("Lines : ", pointer_code)
                    sys.exit()

        elif ptr_code == '<':
            pointer_stack -= 1
            if pointer_stack < 0:
                pointer_stack = 0
            try:
                current_cell_info = main_stack[pointer_stack]
            except Exception as f:
                print("An exception occurred : ", f)
                print("Lines : ", pointer_code)
                sys.exit()

        elif ptr_code == '.':
            try:
                output(current_cell_info,save_location)
                #print(current_cell_info)
            except Exception as e:
                print("An exception occurred : ", e)
                print("Lines : ", pointer_code)
                sys.exit()

        elif ptr_code == ',':
            try:
                main_stack[pointer_stack] = accept_input(save_location)
                if main_stack[pointer_stack] > 255:
                    main_stack[pointer_stack] = 255
                current_cell_info = main_stack[pointer_stack]
                #print(main_stack[pointer_stack])
            except Exception as e:
                print("An exception occurred : ", e)
                print("Lines : ", pointer_code)
                sys.exit()

        elif ptr_code == '+':
            try:
                main_stack[pointer_stack] += 1
                if main_stack[pointer_stack] > 255:
                    main_stack[pointer_stack] = 255
                current_cell_info = main_stack[pointer_stack]
                #print(main_stack[pointer_stack])
            except Exception as e:
                print("An exception occurred : ", e)
                print("Lines : ", pointer_code)
                sys.exit()

        elif ptr_code == '-':
            try:
                main_stack[pointer_stack] -= 1
                if main_stack[pointer_stack] < 0:
                    main_stack[pointer_stack] = 0
                current_cell_info = main_stack[pointer_stack]
                #print(main_stack[pointer_stack])
            except Exception as e:
                print("An exception occurred : ", e)
                print("Lines : ", pointer_code)
                sys.exit()

        elif ptr_code == '[':
            try:
                if current_cell_info == 0:
                    close_index = for_loop_indexes[str(i)]
                    i = close_index
            except Exception as e:
                print("An exception occurred : ", e)
                print("Lines : ", pointer_code)
                sys.exit()

        elif ptr_code == ']':
            try:
                if current_cell_info != 0:
                    spp = int(list(for_loop_indexes.keys())[list(for_loop_indexes.values()).index(i)])
                    i = spp
            except Exception as e:
                print("An exception occurred : ", e)
                print("Lines : ", pointer_code)
                sys.exit()

        #stay
        pointer_code += 1
        i += 1
    end_timer = time.time()
    #print(for_loop_indexes)
    if save_location != '':
        save_location = save_location + ".log"
        try:
            out_file = open(save_location,mode="a")
            stt = "\n----------\nTotal Lines : " + str(i) + "\nTotal Executed code : " + str(pointer_code) + "\nTotal execution(with input user delay) time : " + str(end_timer - start_time) + "\n--------------------\n\n\n"
            out_file.write(stt)
            out_file.close()
        except Exception as e:
            print("An exception occurred while saving log : ", e)

if __name__ == "__main__":
   main(sys.argv[1:])