
import json



def match_pattern(pattern, char):
    if pattern == "reg[A-Za-z0-9_]":
        return char.isalpha() or char.isdigit() or char == "_"
    elif pattern == "reg[A-Za-z]":
        return char.isalpha()
    elif pattern == "reg[0-9]":
        return char.isdigit()
    elif pattern == "reg[^']":
        return char != "'" 
    else:
        return char == pattern 
        

def get_next_state(current_state, char, dfa_json):
    for t in dfa_json["transition_func"]:
        if t["from"] == current_state and match_pattern(t["input"], char):
            return t["to"]
    return None 

def check_keyword(stringValue, list_tok):
     for item in dfa["reserved_word"]:
        lexeme = item["lexeme"]
        tipe = item["token"]
        if(lexeme == stringValue):
            print("masuk 1")
            list_tok.append(f"{tipe}({value})")
            return True



dfa= None
list_tokens = []


with open("src\DFA2.2.json", "r") as f:
    dfa = json.load(f)


with open("src\coba.pas", "r") as file:
    current_state = "q0"
    value = ""
    while True:
        pointerPos = file.tell()
        ch = file.read(1)   
        print(ch)  

        
        temp = get_next_state(current_state, ch, dfa)

        #DEBUGGER STUFF
        print("to state "+ str(temp))
        print("from state " + str(current_state))

        if not ch:  
            if current_state in dfa["final_state"] and value:
                list_tokens.append(f"{current_state}({value})")
            break

        if ch.isspace() and current_state not in dfa["LITERAL_STATES"]:
            if(check_keyword(value, list_tokens)):
                value = ""
                current_state = "q0"

            elif current_state in dfa["final_state"] and value:
                print("masuk 2")
                list_tokens.append(f"{current_state}({value})")

            value = ""
            current_state = "q0"
            continue



        if temp == None:
            if(check_keyword(value, list_tokens)):
                #move seek pointer to pointer pos
                file.seek(pointerPos)

            elif current_state in dfa["final_state"]:
                print("seharusnya masuk none ini value " + value)
                list_tokens.append(f"{current_state}({value})")

                #move seek pointer to pointer pos
                file.seek(pointerPos)
                print(pointerPos)


            else:
                #invalid
                list_tokens.append(f"<ERROR>({ch})")
                
            current_state = "q0"
            value = ""
        else:
            #reset
            current_state = temp
            value += ch


for token in list_tokens:
    print(token)



            
    
