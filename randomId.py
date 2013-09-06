## Script (Python) "randomId"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=num_bits=64
##title=
##
if num_bits < 1:
    raise RuntimeError, "randomID called with negative (or zero) number of bits"
if num_bits > 1024:
    raise RuntimeError, "randomID called with too many bits (> 1024)"

# create a num_bits string from random
tmp_id = 0L
for i in range(0, num_bits):
    tmp_id += long(random.randint(0,1)) << i
#rof

# the 2: removes the '0x' and :-1 removes the L
rnd_id = hex(tmp_id)[2:-1]

return(rnd_id)
