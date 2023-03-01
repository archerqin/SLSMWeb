from lupa import LuaRuntime
lua = LuaRuntime(unpack_returned_tuples=True)

_ = lua.require("table")
luaRet, _ = lua.require("./testfile/testLuaConfig")

print(luaRet[2].data.typename)