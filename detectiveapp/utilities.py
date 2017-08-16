class Testimony(object):
    class TestimonyIterator(object):
        def __init__(self, raw_testimony):
            self.data = raw_testimony if raw_testimony else []
            self.pointer = 0

        def peek_next(self):
            if self.pointer + 1 >= len(self.data):
                return None
            return self.data[self.pointer + 1]

        def next(self):
            self.pointer += 1
            if self.pointer >= len(self.data):
                return None
            return self.data[self.pointer]

        def value(self):
            if self.pointer >= len(self.data):
                return None
            return self.data[self.pointer]

        def __iter__(self):
            self.pointer = 0
            return self

        def __next__(self):
            value = self.next()
            if not value:
                raise StopIteration
            return value

        def __str__(self):
            return '<Iterator @ {} over {}>'.format(self.pointer, self.data)

        __repr__ = __str__

    def __init__(self, testimony):
        self.data = testimony

    def get_iterator(self):
        return Testimony.TestimonyIterator(self.data)

    def __contains__(self, item):
        return item in self.data

    def __str__(self):
        return '<Testimony {}>'.format(self.data.__str__())

    __repr__ = __str__


class TestimonyGraph(object):
    def __init__(self):
        self.graph = {}
        self.vertexes = set()

    def get_starting_points(self):
        values = []
        for children in self.graph.values():
            for child in children:
                values.append(child)
        return [k for k in self.graph.keys() if k not in values]

    def to_array(self):
        def collect(pointer, graph):
            if not graph or not pointer:
                return []
            if pointer not in graph:
                return [[pointer]]

            return_collection = []
            for child in graph[pointer]:
                previous_values = collect(child, graph)
                for result in previous_values:
                    result.append(pointer)
                    return_collection.append(result)
            return return_collection

        results = []
        for starting_pointer in self.get_starting_points():
            results.extend(collect(starting_pointer, self.graph))
        return [r[::-1] for r in results]

    def has_vertex(self, vertex):
        return vertex in self.vertexes

    def __getitem__(self, key):
        return self.graph[key]

    def __setitem__(self, key, val):
        self.vertexes.add(key)
        self.vertexes.update(val)
        self.graph[key] = val

    def __contains__(self, item):
        return item in self.graph

    def __str__(self):
        return '<TestimonyGraph {}>'.format(self.graph.__str__())

    __repr__ = __str__
