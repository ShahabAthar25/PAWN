from dataTypes.number import Number

def setGlobalSymbolTable(global_symbol_table):
    global_symbol_table.set("none", Number(0))
    global_symbol_table.set("null", Number(0))
    global_symbol_table.set("false", Number(0))
    global_symbol_table.set("true", Number(1))