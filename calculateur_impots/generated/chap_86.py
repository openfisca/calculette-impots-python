# -*- coding: utf-8 -*-
# flake8: noqa


# WARNING: This file is automatically generated by a script. No not modify it by hand!

# Original files are "chap-86.json" and "chap-86.m"


BNNSV = positif(BNHREV - BNHDEV * 1 - positif(ART1731BIS * PREM8_11)) * arr(BNHREV - BNHDEV * 1 - positif(ART1731BIS * PREM8_11) * MAJREV) + 1 - positif_ou_nul(BNHREV - BNHDEV * 1 - positif(ART1731BIS * PREM8_11)) * BNHREV - BNHDEV * 1 - positif(ART1731BIS * PREM8_11)


BNNSC = positif(BNHREC - BNHDEC * 1 - positif(ART1731BIS * PREM8_11)) * arr(BNHREC - BNHDEC * 1 - positif(ART1731BIS * PREM8_11) * MAJREV) + 1 - positif_ou_nul(BNHREC - BNHDEC * 1 - positif(ART1731BIS * PREM8_11)) * BNHREC - BNHDEC * 1 - positif(ART1731BIS * PREM8_11)


BNNSP = positif(BNHREP - BNHDEP * 1 - positif(ART1731BIS * PREM8_11)) * arr(BNHREP - BNHDEP * 1 - positif(ART1731BIS * PREM8_11) * MAJREV) + 1 - positif_ou_nul(BNHREP - BNHDEP * 1 - positif(ART1731BIS * PREM8_11)) * BNHREP - BNHDEP * 1 - positif(ART1731BIS * PREM8_11)


BNNAV = BNCREV - BNCDEV * 1 - positif(ART1731BIS * PREM8_11)


BNNAC = BNCREC - BNCDEC * 1 - positif(ART1731BIS * PREM8_11)


BNNAP = BNCREP - BNCDEP * 1 - positif(ART1731BIS * PREM8_11)


BNNAAV = BNCAABV - BNCAADV * 1 - positif(ART1731BIS * PREM8_11)


BNNAAC = BNCAABC - BNCAADC * 1 - positif(ART1731BIS * PREM8_11)


BNNAAP = BNCAABP - BNCAADP * 1 - positif(ART1731BIS * PREM8_11)

VARDNOCEPV = min(max(DNOCEP, max(DNOCEP_P, DNOCEPP2)), ANOCEP)


VARDNOCEPC = min(max(DNOCEPC, max(DNOCEPC_P, DNOCEPCP2)), ANOVEP)


VARDNOCEPP = min(max(DNOCEPP, max(DNOCEPP_P, DNOCEPPP2)), ANOPEP)


NOCEPV = ANOCEP - DNOCEP + BNCAABV - BNCAADV


NOCEPC = ANOVEP - DNOCEPC + BNCAABC - BNCAADC


NOCEPP = ANOPEP - DNOCEPP + BNCAABP - BNCAADP


NOCEPIMPV = positif(ANOCEP - DNOCEP * 1 - positif(ART1731BIS * PREM8_11)) * arr(ANOCEP - DNOCEP * 1 - positif(ART1731BIS * PREM8_11) * MAJREV) + positif_ou_nul(DNOCEP * 1 - positif(ART1731BIS * PREM8_11) - ANOCEP) * ANOCEP - DNOCEP * 1 - positif(ART1731BIS * PREM8_11) + BNNAAV


NOCEPIMPC = positif(ANOVEP - DNOCEPC * 1 - positif(ART1731BIS * PREM8_11)) * arr(ANOVEP - DNOCEPC * 1 - positif(ART1731BIS * PREM8_11) * MAJREV) + positif_ou_nul(DNOCEPC * 1 - positif(ART1731BIS * PREM8_11) - ANOVEP) * ANOVEP - DNOCEPC * 1 - positif(ART1731BIS * PREM8_11) + BNNAAC


NOCEPIMPP = positif(ANOPEP - DNOCEPP * 1 - positif(ART1731BIS * PREM8_11)) * arr(ANOPEP - DNOCEPP * 1 - positif(ART1731BIS * PREM8_11) * MAJREV) + positif_ou_nul(DNOCEPP * 1 - positif(ART1731BIS * PREM8_11) - ANOPEP) * ANOPEP - DNOCEPP * 1 - positif(ART1731BIS * PREM8_11) + BNNAAP


NOCEPIMP = NOCEPIMPV + NOCEPIMPC + NOCEPIMPP


TOTDABNCNP = null(4 - V_IND_TRAIT) * DABNCNP6 + DABNCNP5 + DABNCNP4 + DABNCNP3 + DABNCNP2 + DABNCNP1 * 1 - positif(ART1731BIS * PREM8_11) + null(5 - V_IND_TRAIT) * max(0, min(DABNCNP6 + DABNCNP5 + DABNCNP4 + DABNCNP3 + DABNCNP2 + DABNCNP1, TOTDABNCNP1731 * ART1731BIS * 1 - PREM8_11 + DABNCNP6 + DABNCNP5 + DABNCNP4 + DABNCNP3 + DABNCNP2 + DABNCNP1 * 1 - positif(ART1731BIS * PREM8_11)))

BNN = somme((BNR(i) for i in ('V', 'C', 'P'))) + SPENETPF + max(0, SPENETNPF + NOCEPIMP - TOTDABNCNP) * 1 - ART1731BIS + somme((BNR(i) for i in ('V', 'C', 'P'))) + SPENETPF + max(0, SPENETNPF + NOCEPIMP - DIDABNCNP + DEFBNCNPF) * ART1731BIS * 1 - PREM8_11 + somme((BNR(i) for i in ('V', 'C', 'P'))) + SPENETPF + max(0, SPENETNPF + NOCEPIMP) * ART1731BIS * PREM8_11

def BNN(i):
    if i in ('V', 'C', 'P'):
        return BNR(i) + SPENET(i)
    else:
        raise NotImplementedError()

BNRTOT = BNRV + BNRC + BNRP


def BNR(i):
    if i in ('V', 'C', 'P'):
        return BNNS(i) + BNNA(i)
    else:
        raise NotImplementedError()

BN1 = somme((BN1(i) for i in ('V', 'C', 'P')))

def BN1(i):
    if i in ('V', 'C', 'P'):
        return BN1A(i) + PVIN(i)E + INVENT(i)
    else:
        raise NotImplementedError()

def SPETOT(i):
    if i in ('V', 'C', 'P'):
        return BNCPRO(i) + BNCNP(i)
    else:
        raise NotImplementedError()

def SPEBASAB(i):
    if i in ('V', 'C', 'P'):
        return SPETOT(i)
    else:
        raise NotImplementedError()


def SPEAB(i):
    if i in ('V', 'C', 'P'):
        return arr(max(MIN_SPEBNC, SPEBASAB(i) * SPETXAB / 100) * positif_ou_nul(SPETOT(i) - MIN_SPEBNC)) + arr(min(MIN_SPEBNC, SPEBASAB(i)) * positif(MIN_SPEBNC - SPETOT(i)))
    else:
        raise NotImplementedError()

def SPEABNP(i):
    if i in ('V', 'C', 'P'):
        return SPEAB(i) - SPEABP(i)
    else:
        raise NotImplementedError()


def SPEABP(i):
    if i in ('V', 'C', 'P'):
        return arr(SPEAB(i) * BNCPRO(i) / SPETOT(i))
    else:
        raise NotImplementedError()

SPENET = somme((SPENET(i) for i in ('V', 'C', 'P')))


def SPENETNP(i):
    if i in ('V', 'C', 'P'):
        return max(0, BNCNP(i) - SPEABNP(i))
    else:
        raise NotImplementedError()


def SPENETP(i):
    if i in ('V', 'C', 'P'):
        return max(0, BNCPRO(i) - SPEABP(i))
    else:
        raise NotImplementedError()


def SPENET(i):
    if i in ('V', 'C', 'P'):
        return SPENETP(i) + SPENETNP(i)
    else:
        raise NotImplementedError()

SPENETCT = BNCPROPVV + BNCPROPVC + BNCPROPVP - BNCPMVCTV - BNCPMVCTC - BNCPMVCTP


SPENETNPCT = BNCNPPVV + BNCNPPVC + BNCNPPVP - BNCNPDCT

SPENETPF = somme((SPENETP(i) for i in ('V', 'C', 'P'))) + SPENETCT


SPENETNPF = somme((SPENETNP(i) for i in ('V', 'C', 'P'))) + SPENETNPCT


BNCNPTOT = SPENETPF + SPENETNPF

SPEPV = somme((max(0, SPEPVP(i) + SPEPVNP(i)) for i in ('V', 'C', 'P')))


def SPEPVP(i):
    if i in ('V', 'C', 'P'):
        return BNCPRO1A(i) - BNCPRODE(i)
    else:
        raise NotImplementedError()


def SPEPVNP(i):
    if i in ('V', 'C', 'P'):
        return BNCNP1A(i) - BNCNPDE(i)
    else:
        raise NotImplementedError()

DCTSPE = positif_ou_nul(BNRTOT + SPENETPF) * BNCPMVCTV + 1 - positif_ou_nul(BNRTOT + SPENETPF) * BNCPMVCTV - abs(BNRTOT + SPENETPF) + 1 - positif_ou_nul(BNRTOT + SPENETPF) * null(BNCPMVCTV - abs(BNRTOT + SPENETPF)) * BNCPMVCTV


DCTSPENP = positif_ou_nul(NOCEPIMP + SPENETNPF) * BNCNPDCT + 1 - positif_ou_nul(NOCEPIMP + SPENETNPF) * BNCNPDCT - abs(NOCEPIMP + SPENETNPF) + 1 - positif_ou_nul(NOCEPIMP + SPENETNPF) * null(BNCNPDCT - abs(NOCEPIMP + SPENETNPF)) * BNCNPDCT

BNCDF1 = 1 - positif_ou_nul(NOCEPIMP + SPENETNPF) * abs(NOCEPIMP + SPENETNPF) + positif_ou_nul(NOCEPIMP + SPENETNPF) * positif_ou_nul(DABNCNP5 + DABNCNP4 + DABNCNP3 + DABNCNP2 + DABNCNP1 - NOCEPIMP - SPENETNPF) * DABNCNP5 + DABNCNP4 + DABNCNP3 + DABNCNP2 + DABNCNP1 - NOCEPIMP - SPENETNPF * null(BNCDF6 + BNCDF5 + BNCDF4 + BNCDF3 + BNCDF2) * 1 - positif(ART1731BIS) + DEFBNCNPF * positif(ART1731BIS * 1 - PREM8_11) + DNOCEP + DNOCEPC + DNOCEPP + BNCAADV + BNCAADC + BNCAADP * positif(ART1731BIS * PREM8_11)

BNCDF2 = 1 - positif_ou_nul(NOCEPIMP + SPENETNPF) * DABNCNP1 + positif_ou_nul(NOCEPIMP + SPENETNPF) * min(max(NOCEPIMP + SPENETNPF - DABNCNP6 - DABNCNP5 - DABNCNP4 - DABNCNP3 - DABNCNP2, 0) - DABNCNP1, DABNCNP1) * -1 * positif_ou_nul(DABNCNP1 - max(NOCEPIMP + SPENETNPF - DABNCNP6 - DABNCNP5 - DABNCNP4 - DABNCNP3 - DABNCNP2, 0)) * 1 - positif(ART1731BIS) + min(DABNCNP1, DABNCNP - DIDABNCNP) * positif(ART1731BIS * 1 - positif(PREM8_11 + null(8 - CMAJ) + null(11 - CMAJ))) + DABNCNP1 * positif(positif(ART1731BIS * PREM8_11) + null(8 - CMAJ) + null(11 - CMAJ))

BNCDF3 = 1 - positif_ou_nul(NOCEPIMP + SPENETNPF) * DABNCNP2 + positif_ou_nul(NOCEPIMP + SPENETNPF) * min(max(NOCEPIMP + SPENETNPF - DABNCNP6 - DABNCNP5 - DABNCNP4 - DABNCNP3, 0) - DABNCNP2, DABNCNP2) * -1 * positif_ou_nul(DABNCNP2 - max(NOCEPIMP + SPENETNPF - DABNCNP6 - DABNCNP5 - DABNCNP4 - DABNCNP3, 0)) * 1 - positif(ART1731BIS) + min(DABNCNP2, DABNCNP - DIDABNCNP - BNCDF2) * positif(ART1731BIS * 1 - positif(PREM8_11 + null(8 - CMAJ) + null(11 - CMAJ))) + DABNCNP2 * positif(positif(ART1731BIS * PREM8_11) + null(8 - CMAJ) + null(11 - CMAJ))

BNCDF4 = 1 - positif_ou_nul(NOCEPIMP + SPENETNPF) * DABNCNP3 + positif_ou_nul(NOCEPIMP + SPENETNPF) * min(max(NOCEPIMP + SPENETNPF - DABNCNP6 - DABNCNP5 - DABNCNP4, 0) - DABNCNP3, DABNCNP3) * -1 * positif_ou_nul(DABNCNP3 - max(NOCEPIMP + SPENETNPF - DABNCNP6 - DABNCNP5 - DABNCNP4, 0)) * 1 - positif(ART1731BIS) + min(DABNCNP3, DABNCNP - DIDABNCNP - BNCDF2 - BNCDF3) * positif(ART1731BIS * 1 - positif(PREM8_11 + null(8 - CMAJ) + null(11 - CMAJ))) + DABNCNP3 * positif(positif(ART1731BIS * PREM8_11) + null(8 - CMAJ) + null(11 - CMAJ))

BNCDF5 = 1 - positif_ou_nul(NOCEPIMP + SPENETNPF) * DABNCNP4 + positif_ou_nul(NOCEPIMP + SPENETNPF) * min(max(NOCEPIMP + SPENETNPF - DABNCNP6 - DABNCNP5, 0) - DABNCNP4, DABNCNP4) * -1 * positif_ou_nul(DABNCNP4 - max(NOCEPIMP + SPENETNPF - DABNCNP6 - DABNCNP5, 0)) * 1 - positif(ART1731BIS) + min(DABNCNP4, DABNCNP - DIDABNCNP - BNCDF2 - BNCDF3 - BNCDF4) * positif(ART1731BIS * 1 - positif(PREM8_11 + null(8 - CMAJ) + null(11 - CMAJ))) + DABNCNP4 * positif(positif(ART1731BIS * PREM8_11) + null(8 - CMAJ) + null(11 - CMAJ))

BNCDF6 = 1 - positif_ou_nul(NOCEPIMP + SPENETNPF) * DABNCNP5 + positif_ou_nul(NOCEPIMP + SPENETNPF) * min(max(NOCEPIMP + SPENETNPF - DABNCNP6, 0) - DABNCNP5, DABNCNP5) * -1 * positif_ou_nul(DABNCNP5 - max(NOCEPIMP + SPENETNPF - DABNCNP6, 0)) * 1 - positif(ART1731BIS) + min(DABNCNP5, DABNCNP - DIDABNCNP - BNCDF2 - BNCDF3 - BNCDF4 - BNCDF5) * positif(ART1731BIS * 1 - positif(PREM8_11 + null(8 - CMAJ) + null(11 - CMAJ))) + DABNCNP5 * positif(positif(ART1731BIS * PREM8_11) + null(8 - CMAJ) + null(11 - CMAJ))

DABNCNP = DABNCNP1 + DABNCNP2 + DABNCNP3 + DABNCNP4 + DABNCNP5 + DABNCNP6


VAREDABNCNP = min(DABNCNP, SPENETNPF + NOCEPIMP)


DEFBNCNP = NOCEPIMP + SPENETNPF + DIDABNCNP + DNOCEP + DNOCEPC + DNOCEPP + BNCAADV + BNCAADC + BNCAADP


DEFBNCNPF = DEFRIBNC * 1 - PREM8_11 * max(0, min(DNOCEP + DNOCEPC + DNOCEPP + BNCAADV + BNCAADC + BNCAADP, max(DEFBNCNP1731, max(DEFBNCNP_P, DEFBNCNPP2)) - DNOCEP - DNOCEPC - DNOCEPP - BNCAADV - BNCAADC - BNCAADP))
