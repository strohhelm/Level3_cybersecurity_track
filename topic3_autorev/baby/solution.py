import angr
import claripy

#load the binary into the program
proj = angr.Project('./rev_spookylicence/spookylicence')

#found requred lengts in the asm code as strlen compared with 0xa => 32
arg_len = 32

#get a bitvector with 32 bytes referenced by the name "sym_arg"
sym_arg = claripy.BVS("sym_arg", 8 * arg_len)

#add a nullbyte to end of argument bitvector
null = claripy.BVV(0, 8)
argv1 = claripy.Concat(sym_arg, null)

#tell the symbolic execution to start here passing self assembled argv to the execution
state = proj.factory.full_init_state(args=[proj.filename, argv1])


#add constrains to possible input to printale characters
for b in sym_arg.chop(8):
	state.solver.add(b >= 0x20)
	state.solver.add(b <= 0x7e)

# simulate the execution from the assembled state 
simgr = proj.factory.simulation_manager(state)


target_addr = 0x40183b #found in angr-management as the addres to get the correct licence
# explore all execution paths until this address is reached
simgr.explore(find=target_addr)

# print win condition
if simgr.found:
	found = simgr.found[0]
	solution = found.solver.eval(sym_arg, cast_to=bytes)
	print(f"[+] Found input: {solution}")
else:
	print(f"[-] No solution found")

