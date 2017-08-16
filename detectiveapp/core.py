from .utilities import Testimony, TestimonyGraph


def merge_testimonies(testimonies):
    if not testimonies:
        return []
    graph = TestimonyGraph()
    for testimony in testimonies:
        merge_into_graph(graph, Testimony(testimony))

    results = graph.to_array()
    if len(results) == len(testimonies) and sorted(results) == sorted(testimonies):
        return testimonies
    return results


def merge_into_graph(g, testimony):
    t_iter = testimony.get_iterator()

    while t_iter.peek_next():
        next_in_g = g[t_iter.value()] if t_iter.value() in g else None
        current_testimony = t_iter.value()
        next_in_testimony = t_iter.peek_next()

        if current_testimony not in g:
            g[current_testimony] = [next_in_testimony]
        # If my successor is the same as the successor in the graph, move iterator forward and continue
        elif next_in_testimony in next_in_g:
            pass
        # If the next value is in testimony, this is the case where we have to merge
        elif next_in_g and any(neighbor in testimony for neighbor in next_in_g):
            # Move through the testimony until we hit the point we need to merge in at
            while current_testimony not in next_in_g:
                g[current_testimony] = [next_in_testimony]
                current_testimony = t_iter.next()
                next_in_testimony = t_iter.peek_next()
        else:
            # If the current value is in the graph, the next value isn't the same as the graph's, and
            # the graph's next value is not in the testimony, we have to create a fork at this node
            g[current_testimony].append(next_in_testimony)
        t_iter.next()
