import re
p1 = re.compile("^[w|W]ho (is|was) .*")
print p1.match("Who is Ishmael an Moby Dick ?")
