from typing import List, Tuple

import numpy as np
from cbr858.constants import RiskTypes, risk_1_2_correlation_matrix, \
    risk_type_correlation_matrix


def rk(r : List[float]) -> float:
    """
    Раздел 6.5, показатель РК определяется по формуле

    :math:`РК = \sqrt{\sum_{i,j} corr_{ij} \\times R_i \\times R_j}`

    где i,j - индексы суммирования, принимающие значение 1 или 2

    :param r:
    :return:
    """
    assert len(r) == 2
    rk2 = 0
    for i in [1,2]:
        for j in [1,2]:
            corr = risk_1_2_correlation_matrix(i,j)
            ri = r[i-1]
            rj = r[j-1]
            rk2 = rk2 + corr * ri * rj
    return np.sqrt(rk2)

def r1(r : List[Tuple[RiskTypes, float]]):
    """
    Оценка риска 1, 6.5.1

    :param r:
    :return:
    """
    r1_2 = 0
    for (i, risk_i) in r:
        for (j, risk_j) in r:
            corr_ij = risk_type_correlation_matrix(i,j)
            r1_2 = r1_2 + corr_ij * risk_i * risk_j
    return np.sqrt(r1_2)


def conc_re(e, k_re, assets):
    """
    Суммарная оценка концентрационного риска на перестраховщика определяемая по формуле

    :math:`Conc_{Re} = max (0, \sum_{i=1}^R E_i - k_{Re} \\times Assets \\right)`

    Ei :
    R : количество перестраховщиков которым переданы в перестрахование обязательства по страховой выплате
    k_Re : коэффициент
        равный 20 % - страховые имеющие лицензию на ДМС
        равный 60 % - иные страховые

    :return:
    """
    assert k_re in [20,60]
    k_re = k_re / 100
    return max(0, np.sum(e) - k_re * assets)

def conc_star(e_star, assets):
    """
    Суммарная оценка концентрационного риска на обыкновенные акции, включенные в состав активов страховой
    организации в соответстви си подпунктом 1.4.6, не соответствуюшие требованию абзаца второго в 3.1.2

    :math:`Conr^* = max(0, E_i^* - 0.15 * Assets)`

    где :math:`E_i^*` совокупная стоимость всех обыкновенных акций
    :param e_star:
    :param assets:
    :return:
    """
    c_star = max(0, e_star - 0.15 * assets)
    return c_star

def r1conc(e, ct, assets, oac, conc_re, conc_star):
    """
    Приложение 1.1

    :math:`R_{1conc} = \sqrt{\sum_{ij} corr_{ij} \\times Conc_i \\times Conc_j} + Conc_{Re} + Conc^*`

    где :math:`corr_{ij}=1`
    :return:
    """

    assert len(e) == len(ct)
    assert len(ct) == len(assets)
    assert len(assets) == len(oac)


    def corr(i,j):
        return 1

    def conc_i(ii):
        return max(0, e[i] - ct[i] * assets[i] * oac[i])

    n = len(e)
    r1conc_squared = 0
    for ii in range(n):
        for jj in range(n):
            cij = corr(ii,jj)
            r1conc_squared = r1conc_squared + cij * conc_i(ii) * conc_i(jj)

    r1_conc = np.sqrt(r1conc_squared) + conc_re + conc_star