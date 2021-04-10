import Tokenizer

class Rules():
    def __init__(self, tokenizer : Tokenizer.PasTokenizer):
        self.tokenizer = tokenizer

    def is_id(self):
        token = self.tokenizer.get_next()
        #print("is_id {}".format(token))
        i = 0
        if token[i].isalpha():

            for i in token:
                if not i.isalnum():
                    raise Exception("Incorrect ID")
        else:
            raise Exception("Incorrect ID")
        return True

    def is_integer_constant(self):
        token = self.tokenizer.get_next()
        #print("is_integer_constant {}".format(token))
        i = 0
        if token in '+-':
            token = self.tokenizer.get_next()
        for i in token:
            if not i.isdigit():
                raise Exception("Incorrect integer_constant")


    def is_constant(self):
        token = self.tokenizer.read_next()
        if not token in ['true','false']:
            self.is_integer_constant()
        else:
            self.tokenizer.get_next()


    def is_read_statement(self):
        token = self.tokenizer.get_next()
        if token != 'read':
            raise Exception("Expceted 'read'")
        else:
            token = self.tokenizer.get_next()
            if token != '(':
                raise Exception("Expceted '('")
            else:
                while(True):
                    self.is_id()
                    token = self.tokenizer.get_next()
                    if not token == ',':
                        if token == ')':
                            break
                        else:
                            raise Exception("Expceted ')' or ','")


    def is_factor(self):
        token = self.tokenizer.read_next()
        if token in '+-' or token[0].isdigit() or token in  ['true','false']:
            self.is_constant()
        else:
            if token == '(':
                token = self.tokenizer.get_next()
                self.is_exspression()
                if self.tokenizer.read_next() != ')':
                    raise Exception("No closing bracket")
                else:
                    self.tokenizer.get_next()
            else:
                self.is_id()


    def is_term(self):
        self.is_factor()
        token = self.tokenizer.read_next()
        if self.tokenizer.read_next() in ['*','/']:
            self.tokenizer.get_next()
            while(True):
                self.is_factor()
                if not self.tokenizer.read_next() in ['*','/']:
                    break
                else:
                    self.tokenizer.get_next()


    def is_simple_expression(self):
        self.is_term()
        token = self.tokenizer.read_next()
        if self.tokenizer.read_next() in ['+','-']:
            self.tokenizer.get_next()
            while(True):
                self.is_term()
                token = self.tokenizer.read_next()
                if not self.tokenizer.read_next() in ['+','-']:
                    break
                else:
                    self.tokenizer.get_next()


    def is_exspression(self):
        self.is_simple_expression()
        token = self.tokenizer.read_next()
        if self.tokenizer.read_next() in ['>','<','>=','<=','=']:
            self.tokenizer.get_next()
            self.is_simple_expression()


    def is_variable_declaration(self):
        self.is_id()
        token = self.tokenizer.read_next()
        while token == ',':
            self.tokenizer.get_next()
            self.is_id()
            token = self.tokenizer.read_next()

        token = self.tokenizer.get_next()
        if token != ':':
            raise Exception(": expected")
        else:
            token = self.tokenizer.get_next()
            if token in ["Integer","Boolean"]:
                return
            else:
                raise Exception(f"Incorrect type {token}")


    def is_variable_declaration_part(self):
        token = self.tokenizer.get_next();
        if token != "var":
            raise Exception("var Expected")
        else:
            self.is_variable_declaration()
            token = self.tokenizer.read_next()
            while token == ";":
                self.tokenizer.get_next()

                chtoken = self.tokenizer.read_next()
                if chtoken in ["const","begin"]:
                    return

                self.is_variable_declaration()
                token = self.tokenizer.read_next()
                if token in ["const","begin"]:
                    raise Exception("; Expected, or whatnot")


    def is_const_declaration_part(self):
        token = self.tokenizer.get_next();
        if token != "const":
            raise Exception("var Expected")
        else:
            self.is_id()
            token = self.tokenizer.read_next()
            if token != "=":
                raise Exception("= Expected")
            else:
                self.tokenizer.get_next()
                self.is_constant()

            token = self.tokenizer.read_next()
            while(token == ";"):
                self.tokenizer.get_next()

                chtoken = self.tokenizer.read_next()
                if chtoken == "begin":
                    return

                self.is_id()
                token = self.tokenizer.read_next()
                if token != "=":
                    raise Exception("= Expected")
                else:
                    self.tokenizer.get_next()
                    self.is_constant()
                token = self.tokenizer.read_next()
                if token in ["const","begin"]:
                    raise Exception("; Expected, or whatnot")



    def is_assignment_statement(self):
        self.is_id()
        token = self.tokenizer.read_next()
        if token != ":=":
            raise Exception(":= excpected")
        else:
            token = self.tokenizer.get_next()
            self.is_exspression()


    def is_program(self):
        token = self.tokenizer.get_next()
        if token == "program":
            self.is_id()
            token = self.tokenizer.get_next()
            if token == ";":
                self.is_block()
                token = self.tokenizer.read_next()
                if token == '.':
                    self.tokenizer.get_next()
                    return True
                else:
                    raise Exception("Must end with .")
            else:
                raise Exception("; Excepted")


    def is_block(self):
        token = self.tokenizer.read_next()
        if token == "var":
            self.is_variable_declaration_part()
            token = self.tokenizer.read_next()
        if token == "const":
            self.is_const_declaration_part()
            token = self.tokenizer.read_next()
        self.is_statement_part()

    def is_statement_part(self):
        token = self.tokenizer.get_next()
        if token == "begin":
            self.is_statements()
        else:
            raise Exception("begin Excepted")
        token = self.tokenizer.get_next()
        if token != "end":
            raise Exception("end Expected")




    def is_write_statement(self):
        token = self.tokenizer.get_next()
        if token != 'write':
            raise Exception("Expceted 'write'")
        else:
            token = self.tokenizer.get_next()
            if token != '(':
                raise Exception("Expceted '('")
            else:
                while(True):
                    self.is_exspression()
                    token = self.tokenizer.get_next()
                    if not token == ',':
                        if token == ')':
                            break
                        else:
                            raise Exception("Expceted ')' or ','")


    def is_statement(self):
        token = self.tokenizer.read_next()
        if token == "write":
            self.is_write_statement()
        elif token == "read":
            self.is_read_statement();
        elif token == "for":
            self.is_for_statement();
            return
        elif token == "if":
            self.is_if_statement();
            return
        elif token == "begin":
            self.tokenizer.get_next()
            self.is_statements();
            tokench = self.tokenizer.get_next()
            if tokench != "end":
                raise Exception("end Expected")
        else:
            self.is_assignment_statement();

        tokench = self.tokenizer.get_next()
        if tokench != ";":
            raise Exception("Expected ;")

    def is_statements(self):
        token = self.tokenizer.read_next()
        while token != "end":
            self.is_statement()
            token = self.tokenizer.read_next()
        #token = self.tokenizer.get_next()



    def is_for_statement(self):
        token = self.tokenizer.get_next()
        if token != "for":
            raise Exception("for expected")
        else:
            self.is_id()

        token = self.tokenizer.get_next()

        if token != ":=":
            raise Exception(":= expected")

        self.is_constant()

        token = self.tokenizer.get_next()

        if token not in ['to','downto']:
            raise Exception("to/downto Expected")

        self.is_constant()

        token = self.tokenizer.get_next()

        if token != 'do':
            raise Exception("do Expected")

        self.is_statement()



    def is_if_statement(self):
        token = self.tokenizer.get_next()
        if token != "if":
            raise Exception("if expected")
        else:
            self.is_exspression()

        token = self.tokenizer.get_next()
        if token != "then":
            raise Exception("then expected")
        else:
            self.is_statement()




