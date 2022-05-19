db = [[{'a'}, {'a', 'b', 'c'}, {'a', 'c'}, {'d'}, {'c', 'f'}],
      [{'a', 'd'}, {'c'}, {'b', 'c'}, {'a', 'e'}],
      [{'e', 'f'}, {'a', 'b'}, {'d', 'f'}, {'c'}, {'b'}],
      [{'e', 'g'}, {'a', 'f'}, {'c'}, {'b'}, {'c'}],
      [{'a'}, {'g', 'h'}, {'f', 'e'}, {'b', 'c', 'e'}, {'a', 'b', 'c'}]
      ]
from multiprefixspan import prefixspan_multiple_items_one_event

pre_object = prefixspan_multiple_items_one_event(db, 2)
pre_object.exect()
print(pre_object.found_patterns[:10])
print(pre_object.exect())