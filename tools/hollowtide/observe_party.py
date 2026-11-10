"""Read-only HGSS party observer for the CP05 test harness.

No code injection, RAM writes, save editing or replacement game data. Layouts
are from include/pokemon.h and include/{save.h,constants/save.h}; the fixed
save pointer is the existing IPKE symbol in rom.ld.
"""
import struct

SAVE_POINTER = 0x021D2228
ORDERS = ("ABCD","ABDC","ACBD","ADBC","ACDB","ADCB",
          "BACD","BADC","CABD","DABC","CADB","DACB",
          "BCAD","BDAC","CBAD","DBAC","CDAB","DCAB",
          "BCDA","BDCA","CBDA","DBCA","CDBA","DCBA")


def crypt(data, seed):
    words = struct.unpack('<'+'H'*(len(data)//2),data)
    out = []
    for word in words:
        seed = (seed*0x41C64E6D+0x6073)&0xFFFFFFFF
        out.append(word^(seed>>16))
    return struct.pack('<'+'H'*len(out),*out)


def decode_mon(raw):
    # ARM sizeof(PartyPokemon) is 240 in this engine; the old 0xEC header
    # comment predates its current capsule/alignment layout.
    assert len(raw) == 240
    pid,flags,checksum = struct.unpack_from('<IHH',raw)
    data = raw[8:136] if flags&2 else crypt(raw[8:136],checksum)
    assert sum(struct.unpack('<64H',data))&0xFFFF == checksum,"Pokemon checksum mismatch"
    order = ORDERS[((pid>>13)&31)%24]
    # Each row maps canonical A/B/C/D to physical slots, not the reverse.
    a_offset,b_offset = (ord(order[i])-ord('A') for i in (0,1))
    a = data[a_offset*32:a_offset*32+32]
    b = data[b_offset*32:b_offset*32+32]
    tail = raw[136:] if flags&1 else crypt(raw[136:],pid)
    return {"species":struct.unpack_from('<H',a)[0],"level":tail[4],
            "experience":struct.unpack_from('<I',a,8)[0]&0x1FFFFF,
            "ability":a[13]+(((struct.unpack_from('<I',a,8)[0]>>31)&1)<<8),
            "moves":list(struct.unpack_from('<4H',b)),
            "hp":struct.unpack_from('<H',tail,6)[0],
            "max_hp":struct.unpack_from('<H',tail,8)[0],"checksum_valid":True}


def snapshot(session):
    def read(address,size):
        assert 0x02000000 <= address and address+size <= 0x02400000
        result = session.send(read=[[address,size]])["memory"][hex(address)]
        return bytes(result)
    save = struct.unpack('<I',read(SAVE_POINTER,4))[0]
    header = read(save+0x2F014+2*16,16)
    ident,size,offset = struct.unpack_from('<III',header)
    assert ident == 2 and size == 1460,(ident,size,offset)
    party = save+16+offset
    maximum,count = struct.unpack('<ii',read(party,8))
    assert maximum == 6 and 0 <= count <= 6,(maximum,count)
    return {"count":count,"members":[decode_mon(read(party+8+240*i,240)) for i in range(count)]}


def dex_flags(session,species):
    """Expanded hg-engine registration bits, not a claim of Pokédex UI access.

    Save block 6 is confirmed by the native SaveData_GetDexPtr thunk in rom.ld;
    expanded size and bit offsets are defined in armips/asm/pokedex.s.
    """
    def read(address,size):
        assert 0x02000000 <= address and address+size <= 0x02400000
        return bytes(session.send(read=[[address,size]])["memory"][hex(address)])
    save = struct.unpack('<I',read(SAVE_POINTER,4))[0]
    ident,size,offset = struct.unpack_from('<III',read(save+0x2F014+6*16,16))
    # SaveArrayHeader size includes this block's four-byte CRC trailer.
    assert ident == 6 and size == 0x704,(ident,size)
    index = species-1;assert 0 <= index < 2048
    base = save+16+offset
    return {name:bool(read(base+flag_offset+index//8,1)[0]&(1<<(index%8)))
            for name,flag_offset in (("caught",4),("seen",0x400))}
