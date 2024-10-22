import dris
mydris = dris.init()
mydris.function = dris.PROTECTION_CHECK
mydris.flags = 0
ret_code = dris.DDProtCheck(mydris, 0)
print('mydris.sdsn', mydris.sdsn )
print('mydris.prodcode.decode()', mydris.prodcode.decode())
print('mydris.ret_code', mydris.ret_code)
