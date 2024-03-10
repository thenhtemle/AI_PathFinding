from Graph import Graph


try:
    graph = Graph(input("Enter the name of the input file: "))
    graph.run()
except Exception as e:
    print(repr(e))
