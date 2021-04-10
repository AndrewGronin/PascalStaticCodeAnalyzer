import Tokenizer
import Rules

with open('pascal_sample_code/test.pas') as f:
    lines = [line.rstrip() for line in f]

tokenizer = Tokenizer.PasTokenizer(lines)

rules = Rules.Rules(tokenizer)

try:
    IsRight = rules.is_program()
    IsEnded = tokenizer.is_ended()
    if IsRight and IsEnded:
        print("Success!!!")
except Exception as e:
    if len(str(e)) <= 20:
        print(e)
    else:
        print("Program is incorrect")


