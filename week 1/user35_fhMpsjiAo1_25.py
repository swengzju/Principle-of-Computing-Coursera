"""
Cookie Clicker Simulator
"""

import simpleplot
import math
import random
# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    # Pylint warns you if you fail to use a leading underscore on class fields to indicate that they are private.
    """
    
    def __init__(self):
        self._totnum = 0.0
        self._curnum = 0.0
        self._curtime = 0.0
        self._cpsrate = 1.0
        self._history = list()
        self._history.append((0.0, None, 0.0, 0.0))
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Current status is "+str(self._totnum)+","+str(self._curnum)+","+str(self._curtime)+","+str(self._cpsrate)
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._curnum
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cpsrate
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._curtime
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies < 0:
            return 0.0
        elif cookies >= self._curnum:        
            return float(math.ceil((cookies - self._curnum)/self._cpsrate))
        elif cookies < self._curnum:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._curtime += time
            self._curnum += self._cpsrate*time
            self._totnum += self._cpsrate*time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._curnum >= cost:
            self._curnum -= cost
            self._cpsrate += additional_cps
            self._history.append((self._curtime, item_name, cost, self._totnum))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    build_info_clone = build_info.clone()
    new_state = ClickerState()
    stop = False
    # timeleft should in the while loop, it updates, because new_state.get_time() updates
    while duration>=new_state.get_time() and stop == False:
        timeleft = duration - new_state.get_time()
        item = strategy(new_state.get_cookies(), new_state.get_cps(), timeleft, build_info_clone)
        if item == None:
            new_state.wait(timeleft)
            stop = True
            break				# should break here
        elapse = new_state.time_until(build_info_clone.get_cost(item))
        if timeleft >= elapse:
            new_state.wait(elapse)
            new_state.buy_item(item, build_info_clone.get_cost(item), build_info_clone.get_cps(item))
            build_info_clone.update_item(item)
        elif timeleft < elapse:
            new_state.wait(timeleft)
            stop = True
    return new_state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    cheap
    """
    item_list = build_info.build_items()
    cost_list = list()
    for dummy_item in item_list:
        cost_list.append(build_info.get_cost(dummy_item))
    min_cost = min(cost_list)
    item_use = item_list[cost_list.index(min_cost)]
    if cps*time_left + cookies < min_cost:
        return None
    else:
        return item_use

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    # different from cheap, not to find the max in list, but to find the max in those can be used
    """
    item_list = build_info.build_items()
    cost_list = list()
    for dummy_item in item_list:
        cost_list.append(build_info.get_cost(dummy_item))
    max_cost = -float('inf')
    for dummy_item2 in cost_list:
        if cps*time_left + cookies >= dummy_item2:
            if dummy_item2 > max_cost:
                max_cost = dummy_item2
                item_use = item_list[cost_list.index(max_cost)]
    if max_cost == -float('inf'):
        return None
    else:
        return item_use
                

def strategy_best(cookies, cps, time_left, build_info):
    """
    random
    """
    item_list = build_info.build_items()
    return random.choice(item_list)
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_none)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()
