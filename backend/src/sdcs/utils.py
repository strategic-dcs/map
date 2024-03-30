
def print_query(query):
    print(str(query.statement.compile(compile_kwargs={"literal_binds": True})))