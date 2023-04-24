from dataclasses import dataclass
from typing import Callable, Dict, List, Tuple
from sklearn import linear_model
from dependencies.constrained_linear_regression import ConstrainedLinearRegression
from individual_league.stats_player.base_stats_player import BaseStatsPlayer

def linear_regress(tup_xy: Tuple[List[List[int]], List[int]]) -> Callable[[float, float], float]:
    X = tup_xy[0]
    y = tup_xy[1]
    reg = linear_model.BayesianRidge(fit_intercept=True)
    reg.fit(X, y)

    return lambda b_stat, p_stat: reg.coef_[0] * b_stat + reg.coef_[1] * p_stat + reg.intercept_

def __arr_mult__(arr1: List[float], arr2: List[float]) -> float:
    s = 0.0
    for i in range(len(arr1)):
        s += arr1[i] * arr2[i]
    return s

def linear_regress_multi(tup_xy: Tuple[List[List[int]], List[int]]) -> Callable[[List[float]], float]:
    X = tup_xy[0]
    y = tup_xy[1]
    reg = linear_model.BayesianRidge(fit_intercept=True)
    reg.fit(X, y)

    return lambda arr: __arr_mult__(arr, reg.coef_) + reg.intercept_

def linear_regress_multi_pos(tup_xy: Tuple[List[List[int]], List[int]]) -> Callable[[List[float]], float]:
    X = tup_xy[0]
    y = tup_xy[1]
    reg = linear_model.Ridge(fit_intercept=True, positive=True)
    reg.fit(X, y)

    return lambda arr: __arr_mult__(arr, reg.coef_) + reg.intercept_

def linear_regress_constraints(tup_xy: Tuple[List[List[int]], List[int]], min_constraints: List[float], max_constraints: List[float]) -> Callable[[List[float]], float]:
    X = tup_xy[0]
    y = tup_xy[1]
    reg = ConstrainedLinearRegression(fit_intercept=True)
    reg.fit(X, y, min_coef=min_constraints, max_coef=max_constraints)

    return lambda arr: __arr_mult__(arr, reg.coef_) + reg.intercept_

# For bad regression stuff
import statsmodels.api as sm


@dataclass
class RegressionAnalysisModel:
    get_x: Callable[[BaseStatsPlayer], int]
    get_y_numerator: Callable[[BaseStatsPlayer], int]
    get_y_denominator: Callable[[BaseStatsPlayer], int]
    min_y_denom: int
    should_use_cooks_distance: bool

@dataclass
class RegressionAnalysis:
    slope: float
    intercept: float
    r_squared: float
    len_x: int

def __get_x_and_y__(
    players: List[BaseStatsPlayer],
    ram: RegressionAnalysisModel
) -> Tuple[List[int], List[int]]:
    x_to_y_info: Dict[int, Tuple[int, int]] = {}
    for player in players:
        x = ram.get_x(player)
        if x not in x_to_y_info:
            x_to_y_info[x] = [0, 0]
        y_info = x_to_y_info[x]
        x_to_y_info[x] = [y_info[0] + ram.get_y_numerator(player), y_info[1] + ram.get_y_denominator(player)]
    
    X: List[List[int]] = []
    y: List[int] = []
    for x in x_to_y_info.keys():
        y_info = x_to_y_info[x]
        if y_info[1] >= ram.min_y_denom and y_info[1] > 0:
            X.append([ x ])
            y.append(y_info[0] / y_info[1])
    return (X, y)

def perform_regression(
    players: List[BaseStatsPlayer],
    ram: RegressionAnalysisModel
) -> RegressionAnalysis:
    x, y = __get_x_and_y__(players, ram)

    results = sm.OLS(y, sm.add_constant(x)).fit()
    
    if ram.should_use_cooks_distance and len(x) > 2:
        x_2 = []
        y_2 = []

        cooks_distance = results.get_influence().cooks_distance[0]
        cutoff = 4.0 / (len(x) - 2)
        for i in range(len(x)):
            if cooks_distance[i] < cutoff:
                x_2.append(x[i])
                y_2.append(y[i])
        
        x = x_2
        y = y_2
        if len(x) > 2 and len(y) > 2:
            results = sm.OLS(y, sm.add_constant(x)).fit()

    return RegressionAnalysis(slope=results.params[1], intercept=results.params[0], r_squared=results.rsquared, len_x=len(x))

def __get_x_and_y_wts__(
    players: List[BaseStatsPlayer],
    ram: RegressionAnalysisModel
) -> Tuple[List[int], List[int], List[float]]:
    x_to_y_info: Dict[int, Tuple[int, int]] = {}
    for player in players:
        x = ram.get_x(player)
        if x not in x_to_y_info:
            x_to_y_info[x] = [0, 0]
        y_info = x_to_y_info[x]
        x_to_y_info[x] = [y_info[0] + ram.get_y_numerator(player), y_info[1] + ram.get_y_denominator(player)]
    
    X: List[List[int]] = []
    y: List[int] = []
    wts: List[int] = []
    for x in x_to_y_info.keys():
        y_info = x_to_y_info[x]
        if y_info[1] >= ram.min_y_denom and y_info[1] > 0:
            X.append([ x ])
            y.append(y_info[0] / y_info[1])
            wts.append(y_info[1])
    return (X, y, wts)

def perform_reg_regression(
    players: List[BaseStatsPlayer],
    ram: RegressionAnalysisModel,
    reg_type: str = "elastic_net"
) -> RegressionAnalysis:
    x, y, wts = __get_x_and_y_wts__(players, ram)

    results = sm.OLS(y, sm.add_constant(x)).fit_regularized(method=reg_type)

    return RegressionAnalysis(slope=results.params[1], intercept=results.params[0], r_squared=0.0, len_x=(len(x)))