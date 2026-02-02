#!/usr/bin/env python3
# ---------------------------------------------------------------
#  确认缺失单词：已知前10个词 + 一个占位符 “__missing__”
#  目标：生成的以太坊地址 (m/44'/60'/0'/0/0) 的最后 6 位 hex 为 700f80
# ---------------------------------------------------------------
import sys
from bip_utils import Bip44, Bip44Coins, Bip44Changes, Bip39SeedGenerator
from mnemonic import Mnemonic

known = [
    "ankle", "assume", "estate", "permit", "__missing__",
    "eye", "fancy", "spring", "demand", "dial", "awkward", "hole"
]
missing_word_index = known.index("__missing__")

suffix = "700f80"
addrs_pre_seed = 20
passpharase = ""

m = Mnemonic("english")
for word in m.wordlist:
    words = known[:]
    words[missing_word_index] = word
    phrase = " ".join(words)
    if not m.check(phrase):
        continue
    seed = Bip39SeedGenerator(phrase).Generate(passpharase)
    ctx = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    change = ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
    for i in range(addrs_pre_seed):
        addr = change.AddressIndex(i).PublicKey().ToAddress()
        if addr.lower().endswith(suffix):
            print(i)
            print(f"Found matching phrase: {phrase}")
            print(f"Address: {addr}")

