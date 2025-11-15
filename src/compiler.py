import json
import sys
from parser import Parser
import os

def match_pattern(pattern, char):
    if pattern == "reg[A-Za-z0-9_]":
        return char.isalnum() or char == "_"
    elif pattern == "reg[A-Za-z0-9]":
        return char.isalnum()
    elif pattern == "reg[A-Za-z]":
        return char.isalpha()
    elif pattern == "reg[0-9]":
        return char.isdigit()
    elif pattern == "reg[^']":
        return char != "'"
    elif pattern == "reg[a-z^e]":
        return char.isalpha() and char != "e"
    else:
        return char == pattern

def get_next_state(current_state, char, dfa_json):
    for t in dfa_json["transition_func"]:
        if t["from"] == current_state and match_pattern(t["input"], char.lower()):
            return t["to"]
    return None

def check_keyword(stringValue, list_tok, dfa):
    for item in dfa["reserved_word"]:
        if item["lexeme"] == stringValue.lower():
            list_tok.append(f"{item['token']}({stringValue})")
            return True
    return False

dfa = None
list_tokens = []

try:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    json_path = os.path.join(script_dir, "DFA-id.json")
    with open(json_path, "r") as f:
        dfa = json.load(f)
except FileNotFoundError:
    print(f"Error: Could not find required file 'DFA-id.json'.")
    print(f"Make sure it is in the same directory as the script.")
    exit()
except Exception as e:
    print(f"Error loading 'DFA-id.json': {e}")
    exit()

try :
    filePath = sys.argv[1]

    if not filePath.endswith(".pas"):
        print("Error: Hanya file dengan ekstensi .pas yang diizinkan.")
        exit()

    with open(f"{filePath}", "r") as f:
        pass

except FileNotFoundError:
    print("File tidak ditemukan.")
    exit()
except IndexError:
    print("Error: Mohon berikan nama file sebagai argumen.")
    exit()

with open(f"{filePath}", "r") as f:
    current_state = "q0"
    value = ""
    while True:
        #simpan pointer pos untuk jaga-jaga bila ada 1 token yang pembacaannya sudah selesai yang ditandai dengan temp null
        pointerPos = f.tell()
        ch = f.read(1)

        temp = get_next_state(current_state, ch, dfa)

        if not ch:  # EOF
            if current_state in dfa["final_states"].keys() and value:
                token_type = dfa["final_states"][current_state]["type"]
                list_tokens.append(f"{token_type}({value})")
            break


        if ch.isspace():
            #memastikan spasi dalam string literal tidak di anggap sebagai pemisah antar state
            if temp is not None:
                value += ch
                continue 
            else:
                # jika spasi sebagai pemisah antar token
                if check_keyword(value, list_tokens, dfa):
                    value = ""
                    current_state = "q0"
                elif current_state in dfa["final_states"].keys() and value:
                    token_type = dfa["final_states"][current_state]["type"]
                    list_tokens.append(f"{token_type}({value})")
                elif value: 
                    list_tokens.append(f"<ERROR>({value})")
                value = ""
                current_state = "q0"
                continue



        #jika menemukan sebuah input char yang tidak menuju ke state manapun, maka akan dianggap pembacaan 1 token selesai
        if temp is None:
            if check_keyword(value, list_tokens, dfa):
                f.seek(pointerPos)
            elif current_state in dfa["final_states"].keys():
                token_type = dfa["final_states"][current_state]["type"]
                list_tokens.append(f"{token_type}({value})")
                f.seek(pointerPos)
            else:
                list_tokens.append(f"<ERROR>({ch})")

            #reset
            current_state = "q0"
            value = ""
        else:
            current_state = temp
            value += ch

for token in list_tokens:
    print(token)

print("============ Parse Output ============")
p = Parser(list_tokens)
p.parse()