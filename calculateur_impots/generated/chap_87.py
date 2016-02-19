# -*- coding: utf-8 -*-
# flake8: noqa


# WARNING: This file is automatically generated by a script. No not modify it by hand!

# Original files are "chap-87.json" and "chap-87.m"


XFORFAIT = somme((FEX(i) for i in ('V', 'C', 'P')))

XACCESS = somme((XACCESS(i) for i in ('V', 'C', 'P')))

def XBNNP(i):
    if i in ('V', 'P', 'C'):
        return BNCNPREX(i) + BNCNPREXAA(i)
    else:
        raise NotImplementedError()


def XBIP(i):
    if i in ('V', 'P', 'C'):
        return BIHEX(i) + BICEX(i)
    else:
        raise NotImplementedError()


def XBINP(i):
    if i in ('V', 'P', 'C'):
        return BICNPHEX(i) + BICNPEX(i)
    else:
        raise NotImplementedError()


def XBN(i):
    if i in ('V', 'P', 'C'):
        return BNHEX(i) + BNCEX(i)
    else:
        raise NotImplementedError()


def XBA(i):
    if i in ('V', 'P', 'C'):
        return BAHEX(i) + BAEX(i)
    else:
        raise NotImplementedError()

def XBICS(i):
    if i in ('V', 'C', 'P'):
        return XBICNET(i) + BA1A(i)
    else:
        raise NotImplementedError()


def XBIS(i):
    if i in ('V', 'C', 'P'):
        return positif(max(0, XBICNET(i) + max(0, XBICNPNET(i)))) * BI2A(i) + BI1A(i)
    else:
        raise NotImplementedError()


def XBICHD(i):
    if i in ('V', 'C', 'P'):
        return BICEX(i) + BICNO(i)
    else:
        raise NotImplementedError()


def XBICNPNET(i):
    if i in ('V', 'C', 'P'):
        return XBICNPHD(i) - min(BICDE(i), BICDE(i)1731 + 0) * positif(ART1731BIS) + BICDE(i) * 1 - ART1731BIS
    else:
        raise NotImplementedError()


def XBICNET(i):
    if i in ('V', 'C', 'P'):
        return XBICHD(i) - BICDN(i) * 1 - positif(ART1731BIS)
    else:
        raise NotImplementedError()


def XBICIMP(i):
    if i in ('V', 'C', 'P'):
        return XBICHD(i) + XBICNPHD(i)
    else:
        raise NotImplementedError()


def XBIT(i):
    if i in ('V', 'C', 'P'):
        return max(0, XBICNET(i) + max(0, XBICNPNET(i)))
    else:
        raise NotImplementedError()


def XBICNPHD(i):
    if i in ('V', 'C', 'P'):
        return BICNPEX(i) + BICRE(i)
    else:
        raise NotImplementedError()


def XBICNPS(i):
    if i in ('V', 'C', 'P'):
        return XBICNPNET(i) + BI2A(i)
    else:
        raise NotImplementedError()

def XEXTS(i):
    if i in ('V', 'C'):
        return XTSB(i) + CARTS(i) + REMPLA(i)
    elif i in (1, 2, 3, 4):
        return XTSB(i) + CARTSP(i) + REMPLAP(i)
    else:
        raise NotImplementedError()


def XTSB(i):
    if i in ('V', 'C'):
        return somme((GLD(x)(i) for x in interval(1, 3))) + TSBN(i) + BPCOSA(i) + TSASSU(i) + XETRAN(i) + EXOCET(i) + GLDGRAT(i)
    elif i in (1, 2, 3, 4):
        return TSBN(i)
    else:
        raise NotImplementedError()

def XTPS10(i):
    if i in (1, 2, 3, 4, 'V', 'C'):
        return arr(XEXTS(i) * TX_DEDFORFTS / 100)
    else:
        raise NotImplementedError()


def XDFN(i):
    if i in (1, 2, 3, 4, 'V', 'C'):
        return min(PLAF_DEDFORFTS, XTPS10(i))
    else:
        raise NotImplementedError()

def XIND_10(i):
    if i in (1, 2, 3, 4, 'V', 'C'):
        return positif_ou_nul(X10MINS(i) - FRN(i))
    else:
        raise NotImplementedError()


def XFPT(i):
    if i in (1, 2, 3, 4, 'V', 'C'):
        return XDF(i) * XIND_10(i) + FRD(i) * 1 - XIND_10(i)
    else:
        raise NotImplementedError()


def X10MINS(i):
    if i in (1, 2, 3, 4, 'V', 'C'):
        return max(min(XTSB(i), DEDMIN(i)), XDFN(i))
    else:
        raise NotImplementedError()


def XDF(i):
    if i in (1, 2, 3, 4, 'V', 'C'):
        return X10MINS(i)
    else:
        raise NotImplementedError()


def XTSNT(i):
    if i in (1, 2, 3, 4, 'V', 'C'):
        return XEXTS(i) - XFPT(i)
    else:
        raise NotImplementedError()

def XTSN(i):
    if i in (1, 2, 3, 4, 'V', 'C'):
        return positif(XTSNT(i)) * min(0, XTSNT(i)) + positif_ou_nul(XTSNT(i)) * XTSNT(i)
    else:
        raise NotImplementedError()

XEXOCET = somme((XEXOCET(i) for i in ('V', 'C')))


def XEXOCET(i):
    if i in ('V', 'C'):
        return arr(positif(XTSN(i)) * XTSN(i) * EXOCET(i) / XEXTS(i)) * XIND_10(i) + 1 - XIND_10(i) * EXOCET(i)
    else:
        raise NotImplementedError()


def XTSNN(i):
    if i in ('V', 'C'):
        return arr(positif(XTSN(i)) * XTSN(i) * TSASSU(i) / XEXTS(i)) * XIND_10(i) + 1 - XIND_10(i) * TSASSU(i)
    else:
        raise NotImplementedError()


def XTS(i):
    if i in ('V', 'C'):
        return XTSN(i) - somme((max(0, GLD(x)(i) - ABGL(x)(i)) for x in interval(1, 3)))
    else:
        raise NotImplementedError()


def XETSNN(i):
    if i in ('V', 'C'):
        return arr(positif(XTSN(i)) * XTSN(i) * XETRAN(i) / XEXTS(i)) * XIND_10(i) + 1 - XIND_10(i) * XETRAN(i)
    else:
        raise NotImplementedError()

XELU = ELURASC + ELURASV

PVTAUX = BPVSJ + BPVSK + BPV18V + BPV18C + BPCOPTV + BPCOPTC + BPV40V + BPV40C + PEA + GAINPEA

GLN2NET = arr(GLN2 * GL2 / REV2)


GLN3NET = arr(GLN3 * GL3 / REV3)


QUOKIRE = TEGL1 + TEGL2 + TEGL3 + RPQ4 + somme((TERPQPRR(x) + TERPQPRRZ(x) + TEGLF(x) + TERPQTS(x) + TERPQTSREMP(x) + TERPQPALIM(x) for x in ('V', 'C') or x in interval(1, 4))) + TERPQRF1 + TEGLRF2 + TERPQRCMDC + TERPQRCMFU + TERPQRCMCH + TERPQRCMTS + TERPQRCMGO + TERPQRCMTR + TERPQRVO + TERPQRVO5 + TERPQRVO6 + TERPQRVO7

VARREVKIRE = BPCAPTAXV + BPCAPTAXC + somme((XBA(i) + XBIP(i) + XBINP(i) + XBN(i) + XBNNP(i) for i in ('V', 'C', 'P'))) + somme((MIBEX(i) + MIBNPEX(i) + BNCPROEX(i) + XSPENP(i) for i in ('V', 'C', 'P'))) + somme((BNCCR(i) for i in ('V', 'C', 'P'))) + somme((BNCCRF(i) for i in ('V', 'C', 'P'))) + somme((XETSNN(i) for i in ('V', 'C'))) + somme((XEXOCET(i) for i in ('V', 'C'))) + somme((XTSNN(i) for i in ('V', 'C'))) + somme((XTSNNTY(i) for i in ('V', 'C'))) + somme((XHSUPTSNN(i) for i in (1, 2, 3, 4, 'V', 'C'))) + XFORFAIT + XACCESS + RCMLIB + PPLIB + GAINABDET + RCMEXCREF + RCM2FA + XELU + RCMIMPAT + PVIMMO + PVMOBNR + PVTITRESOC + BTP3A + 1 - positif(IPVLOC) * 1 - positif(present(TAX1649) + present(RE168)) * PVTAUX


PVTXEFF2 = max(0, BPVRCM + COD3SG + COD3SL + ABDETPLUS + ABIMPPV - DPVRCM + COD3SH + COD3SM + ABDETMOINS + ABIMPMV)


PVTXEFF = PVTAXSB + BPVRCM - PVTXEFF2 * positif(present(IPTEFN) + present(IPTEFP))


REVKIRE = 1 - null(IND_TDR) * arr(max(0, 1 - positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + VARIPTEFN + PVTXEFF * present(IPTEFN) * positif(ART1731BIS) + IPTEFN + PVTXEFF * present(IPTEFN) * 1 - ART1731BIS + INDTEFF) * RI1RFR + positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + VARIPTEFN + PVTXEFF * present(IPTEFN) * positif(ART1731BIS) + IPTEFN + PVTXEFF * present(IPTEFN) * 1 - ART1731BIS + INDTEFF) * max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + VARIPTEFN + PVTXEFF * present(IPTEFN) * positif(ART1731BIS) + IPTEFN + PVTXEFF * present(IPTEFN) * 1 - ART1731BIS + INDTEFF) * positif(TEFFN - DRBG - RNIDF + APERPV + APERPC + APERPP * 1 - positif(null(2 - V_REGCO) + null(4 - V_REGCO)) + QUOKIRE) * APERPV + APERPC + APERPP * 1 - positif(null(2 - V_REGCO) + null(4 - V_REGCO)) + QUOKIRE + max(0, TEFFREVTOTRFR * INDTEFF) * 1 - positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS) * 1 - present(IND_TDR) + IND_TDR + 1 - positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + VARIPTEFN + PVTXEFF * present(IPTEFN) * positif(ART1731BIS) + IPTEFN + PVTXEFF * present(IPTEFN) * 1 - ART1731BIS + INDTEFF) * QUOKIRE + APERPV + APERPC + APERPP * 1 - positif(null(2 - V_REGCO) + null(4 - V_REGCO)) + VARREVKIRE))


QUOKIREHR = TGL1 + TGL2 + TGL3 + TGL4 + somme((TGLPRR(x) + TGLPRRZ(x) + TGLF(x) + TGLTS(x) + TGLTSREMP(x) + TGLPALIM(x) for x in ('V', 'C') or x in interval(1, 4))) + TGLRF1 + TGLRF2 + TGLRCMDC + TGLRCMFU + TGLRCMCH + TGLRCMTS + TGLRCMGO + TGLRCMTR + TGLRVO + TGLRVO5 + TGLRVO6 + TGLRVO7


REVKIREHR = 1 - null(IND_TDR) * arr(max(0, 1 - positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + VARIPTEFN + PVTXEFF * present(IPTEFN) * positif(ART1731BIS) + IPTEFN + PVTXEFF * present(IPTEFN) * 1 - ART1731BIS + INDTEFF) * RI1RFRHR + positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + VARIPTEFN + PVTXEFF * present(IPTEFN) * positif(ART1731BIS) + IPTEFN + PVTXEFF * present(IPTEFN) * 1 - ART1731BIS + INDTEFF) * max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + VARIPTEFN + PVTXEFF * present(IPTEFN) * positif(ART1731BIS) + IPTEFN + PVTXEFF * present(IPTEFN) * 1 - ART1731BIS + INDTEFF) * positif(TEFFN - DRBG - RNIDF + APERPV + APERPC + APERPP * 1 - positif(null(2 - V_REGCO) + null(4 - V_REGCO)) + QUOKIREHR) * APERPV + APERPC + APERPP * 1 - positif(null(2 - V_REGCO) + null(4 - V_REGCO)) + QUOKIREHR + max(0, TEFFREVTOTRFRHR * INDTEFF) * 1 - positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS) * 1 - present(IND_TDR) + IND_TDR + 1 - positif(max(0, VARIPTEFP - PVTXEFF) * positif(ART1731BIS) + max(0, IPTEFP - PVTXEFF) * 1 - ART1731BIS + VARIPTEFN + PVTXEFF * present(IPTEFN) * positif(ART1731BIS) + IPTEFN + PVTXEFF * present(IPTEFN) * 1 - ART1731BIS + INDTEFF) * QUOKIREHR + APERPV + APERPC + APERPP * 1 - positif(null(2 - V_REGCO) + null(4 - V_REGCO)) + VARREVKIRE)) * 1 - present(COD8YM) + COD8YM


def BNCCREA(i):
    if i in ('V', 'C', 'P'):
        return BNCCR(i) + BNCCRF(i)
    else:
        raise NotImplementedError()

CDEVDUR_NBJ = PPENBJ


CKIREDUR = arr(REVKIRE * 360 / CDEVDUR_NBJ)


REVKIREDUR2 = CKIREDUR
