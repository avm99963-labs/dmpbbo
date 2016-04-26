import numpy as np
import math
import os
import sys
import matplotlib.pyplot as plt

lib_path = os.path.abspath('../../python/')
sys.path.append(lib_path)

from rollout import Rollout

from bbo.bbo_plotting import plotUpdate, plotCurve, saveUpdate, saveCurve
from dmp_bbo.dmp_bbo_plotting import saveUpdateRollouts, setColor
  
  
def runOptimizationTask(task, task_solver, initial_distribution, updater, n_updates, n_samples_per_update,fig=None,directory=None):
    
    distribution = initial_distribution
  
    learning_curve = np.zeros((n_updates, 3))
    
    if fig:
        ax_space   = fig.add_subplot(141)
        ax_rollout = fig.add_subplot(142)

    # Optimization loop
    update_summaries = []
    for i_update in range(n_updates): 
        
        # 0. Get cost of current distribution mean
        cost_vars_eval = task_solver.performRollout(distribution.mean)
        cost_eval = task.evaluateRollout(cost_vars_eval)
        rollout_eval = Rollout(distribution.mean,cost_vars_eval,cost_eval)
        
        # 1. Sample from distribution
        samples = distribution.generateSamples(n_samples_per_update)
    
        rollouts = []
        costs = np.full(n_samples_per_update,0.0)
        for i_sample in range(n_samples_per_update):
            
            # 2A. Perform the rollouts
            cost_vars = task_solver.performRollout(samples[i_sample,:])
      
            # 2B. Evaluate the rollouts
            cur_costs = task.evaluateRollout(cost_vars)
            costs[i_sample] = cur_costs[0]

            rollouts.append(Rollout(samples[i_sample,:],cost_vars,cur_costs))

      
        # 3. Update parameters
        distribution_new, weights = updater.updateDistribution(distribution, samples, costs)
          
        # Bookkeeping and plotting
        
        # Update learning curve 
        # How many samples so far?  
        learning_curve[i_update,0] = i_update*n_samples_per_update
        # Cost of evaluation
        learning_curve[i_update,1] = cost_eval[0]
        # Exploration magnitude
        learning_curve[i_update,2] = np.sqrt(distribution.maxEigenValue()); 
        
        # Plot summary of this update
        if fig:
            highlight = (i_update==0)
            plotUpdate(distribution,cost_eval,samples,costs,weights,distribution_new,ax_space,highlight)
            h = task_solver.plotRollout(rollout_eval.cost_vars,ax_rollout)
            setColor(h,i_update,n_updates)
            
        if directory:
            saveUpdateRollouts(directory, i_update, distribution, rollout_eval, rollouts, weights, distribution_new)
                
        # Distribution is new distribution
        distribution = distribution_new
        
    # Plot learning curve
    if fig:
        axs = [ fig.add_subplot(143), fig.add_subplot(144)]
        plotCurve(learning_curve,axs)

    # Save learning curve to file, if necessary
    if directory:
        saveCurve(directory,learning_curve)
    
    
    return learning_curve



