# -*- coding: utf-8 -*-
# flake8: noqa


# WARNING: This file is automatically generated by a script. No not modify it by hand!

# Original files are "chap-2.json" and "chap-2.m"


NAPINI = IRN + PIR - IRANT * 1 - INDTXMIN * 1 - INDTXMOY + min(0, IRN + PIR - IRANT) * INDTXMIN + INDTXMOY + max(0, IRN + PIR - IRANT) * INDTXMIN * positif(IAVIMBIS - NAPCRPAVIM - SEUIL_61) + INDTXMOY * positif(IAVIMO - NAPCRPAVIM - SEUIL_61) + RASAR * V_CR2


RC1INI = positif(NAPINI + 1 - SEUIL_12)

NAPTOT = IRCUM + TAXACUM + PCAPCUM + TAXLOYCUM + HAUTREVCUM - RECUMIR

NAPTOTA = V_IRPSANT - V_ANTRE


NAPTOTAIR = V_TOTIRANT - V_ANTREIR


TOTCRA = V_ANTCR


TOTIRPSANT = V_IRPSANT - V_NONMERANT + V_NONRESTANT - V_ANTRE

IRNIN = IRN - IRANT * positif(IRN - IRANT)

ISF4BASE = ISF4BIS * positif_ou_nul(ISF4BIS - SEUIL_12)


ISFIN = ISF4BASE

IRNIN_INR = max(0, IRN - IRANT - IR9YI) * positif(IRN - IRANT)


CSBASE_INR = max(0, CSG - CSGIM - CS9YP)


RDBASE_INR = max(0, RDSN - CRDSIM - RD9YP)


PSBASE_INR = max(0, PRS - PRSPROV - PS9YP)


CVNBASE_INR = max(0, CVNSALC - COD8YT - CVN9YP)


CDISBASE_INR = max(0, CDIS - CDISPROV - CDIS9YP)


GLOBASE_INR = max(0, CGLOA - COD8YL - GLO9YP)


REGVBASE_INR = max(0, BREGV - REGV9YP)


RSE1BASE_INR = max(0, RSE1N - CSPROVYD - RSE19YP)


RSE2BASE_INR = max(0, max(0, RSE8TV - CIRSE8TV - CSPROVYF) + max(0, RSE8SA - CIRSE8SA - CSPROVYN) - RSE29YP)


RSE3BASE_INR = max(0, RSE3N - CSPROVYG - RSE39YP)


RSE4BASE_INR = max(0, max(0, RSE8TX - CIRSE8TX - CSPROVYH) + max(0, RSE8SB - CIRSE8SB - CSPROVYP) - RSE49YP)


RSE5BASE_INR = max(0, RSE5N - CSPROVYE - RSE59YP)


TAXABASE_INR = arr(max(TAXASSUR - TAXA9YI + min(0, IRN - IRANT), 0)) * positif(IAMD1 + 1 - SEUIL_61)


PCAPBASE_INR = arr(max(IPCAPTAXT - CAP9YI + min(0, IRN - IRANT + TAXASSUR), 0)) * positif(IAMD1 + 1 - SEUIL_61)


LOYBASE_INR = arr(max(TAXLOY - LOY9YI + min(0, IRN - IRANT + TAXASSUR + IPCAPTAXT), 0)) * positif(IAMD1 + 1 - SEUIL_61)


CHRBASE_INR = arr(max(IHAUTREVT - CHR9YI + min(0, IRN - IRANT + TAXASSUR + IPCAPTAXT + TAXLOY), 0)) * positif(IAMD1 + 1 - SEUIL_61)


CSBASE = CSG - CSGIM


RDBASE = RDSN - CRDSIM


PSBASE = PRS - PRSPROV


CVNBASE = CVNSALC - COD8YT


CDISBASE = CDIS - CDISPROV


GLOBASE = CGLOA - COD8YL


RSE1BASE = RSE1N - CSPROVYD


RSE2BASE = max(0, RSE8TV - CIRSE8TV - CSPROVYF) + max(0, RSE8SA - CIRSE8SA - CSPROVYN)


RSE3BASE = RSE3N - CSPROVYG


RSE4BASE = max(0, RSE8TX - CIRSE8TX - CSPROVYH) + max(0, RSE8SB - CIRSE8SB - CSPROVYP)


RSE5BASE = RSE5N - CSPROVYE


REGVBASE = BREGV


TAXABASE = arr(max(TAXASSUR + min(0, IRN - IRANT), 0)) * positif(IAMD1 + 1 - SEUIL_61)


PCAPBASE = arr(max(IPCAPTAXT + min(0, IRN - IRANT + TAXASSUR), 0)) * positif(IAMD1 + 1 - SEUIL_61)


LOYBASE = arr(max(TAXLOY + min(0, IRN - IRANT + TAXASSUR + IPCAPTAXT), 0)) * positif(IAMD1 + 1 - SEUIL_61)


CHRBASE = arr(max(IHAUTREVT + min(0, IRN - IRANT + TAXASSUR + IPCAPTAXT + TAXLOY), 0)) * positif(IAMD1 + 1 - SEUIL_61)


IRBASE_I = IRN - IRANT * positif(IRN + 1 - SEUIL_12)


IRBASE_N = IRN - IRANT * 1 - positif(IRN - IRANT + TAXABASE_IRECT + CAPBASE_IRECT + HRBASE_IRECT) + IAN - min(IAN, IRE) * positif(IRN - IRANT + TAXABASE_IRECT + CAPBASE_IRECT + HRBASE_IRECT)


TAXABASE_I = TAXASSUR * positif(IAMD1 + 1 - SEUIL_61)


TAXABASE_N = arr(max(TAXASSUR + min(0, IRN - IRANT), 0)) * positif(IAMD1 + 1 - SEUIL_61)


CAPBASE_I = IPCAPTAXT * positif(IAMD1 + 1 - SEUIL_61)


CAPBASE_N = arr(max(IPCAPTAXT + min(0, IRN - IRANT + TAXASSUR), 0)) * positif(IAMD1 + 1 - SEUIL_61)


LOYBASE_I = TAXLOY * positif(IAMD1 + 1 - SEUIL_61)


LOYBASE_N = arr(max(TAXLOY + min(0, IRN - IRANT + TAXASSUR + IPCAPTAXT), 0)) * positif(IAMD1 + 1 - SEUIL_61)


HRBASE_I = IHAUTREVT * positif(IAMD1 + 1 - SEUIL_61)


HRBASE_N = arr(max(IHAUTREVT + min(0, IRN - IRANT + TAXASSUR + IPCAPTAXT + TAXLOY), 0)) * positif(IAMD1 + 1 - SEUIL_61)


IRNN = IRNIN

PTOTIRCS = PIR + PTAXA + PTAXLOY + PHAUTREV + PPCAP + PPRS + PCSG + PRDS + PCDIS + PREGV + PCVN + PGLOA + PRSE1 + PRSE2 + PRSE3 + PRSE4 + PRSE5


TOTPENIR = PIR + PTAXA + PTAXLOY + PHAUTREV + PPCAP


TOTPENCS = PPRS + PCSG + PRDS + PCVN + PREGV + PCDIS + PGLOA + PRSE1 + PRSE2 + PRSE3 + PRSE4 + PRSE5


INCTOTIR = RETIR + RETTAXA + RETPCAP + RETLOY + RETHAUTREV


INCTOTCS = RETCS + RETRD + RETPS + RETCVN + RETREGV + RETCDIS + RETGLOA + RETRSE1 + RETRSE2 + RETRSE3 + RETRSE4 + RETRSE5


RETIRCSTOT = INCTOTIR + INCTOTCS

PIR = PTOIR * positif_ou_nul(IAMD1 - SEUIL_61)


PPRS = PTOPRS


PCSG = PTOCSG


PRSE1 = PTORSE1


PRSE2 = PTORSE2


PRSE3 = PTORSE3


PRSE4 = PTORSE4


PRSE5 = PTORSE5


PREGV = PTOREGV


PRDS = PTORDS


PTAXA = PTOTAXA


PPCAP = PTOTPCAP


PTAXLOY = PTOTLOY


PHAUTREV = PTOTCHR


PCVN = PTOCVN


PCDIS = PTOCDIS


PGLOA = PTOGLOA

PTOT = PIR

ILIIRNET = positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * max(0, IRCUM - PIR) + 1 - positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * TOTIRCUM - RECUMIR - TOTPENIR


PIRNETNEG = max(0, PIR - IRCUM)


ILITAXANET = positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * max(0, TAXACUM - PTAXA - PIRNETNEG) + 1 - positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * 0


PTAXANETNEG = max(0, PIR + PTAXA - IRCUM - TAXACUM)


ILICAPNET = positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * max(0, PCAPCUM - PPCAP - PTAXANETNEG) + 1 - positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * 0


PPCAPNETNEG = max(0, PIR + PTAXA + PPCAP - IRCUM - TAXACUM - PCAPCUM)


ILILOYNET = positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * max(0, TAXLOYCUM - PTAXLOY - PPCAPNETNEG) + 1 - positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * 0


PTAXLOYNETNEG = max(0, PIR + PTAXA + PPCAP + PTAXLOY - IRCUM - TAXACUM - PCAPCUM - TAXLOYCUM)


ILICHRNET = positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * max(0, HAUTREVCUM - PHAUTREV - PTAXLOYNETNEG) + 1 - positif_ou_nul(TOTIRCUM - RECUMIR - TOTPENIR) * 0


ILITOTIRNET = ILIIRNET + ILITAXANET + ILICAPNET + ILILOYNET + ILICHRNET


ILITOTPSNET = max(0, NAPCR61 - TOTPENCS)


TOTIRE = IREP - ITRED - IRE - INE


TOTTP = TTPVQ + REVTP

MAJOTOT28IR = NMAJ1 + NMAJTAXA1 + NMAJPCAP1 + NMAJLOY1 + NMAJCHR1


MAJOTOT28PS = NMAJC1 + NMAJR1 + NMAJP1 + NMAJCVN1 + NMAJREGV1 + NMAJCDIS1 + NMAJGLO1 + NMAJRSE11 + NMAJRSE21 + NMAJRSE31 + NMAJRSE41 + NMAJRSE51


MAJO1728TOT = MAJOTOT28IR + MAJOTOT28PS
