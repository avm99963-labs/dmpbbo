# This file is part of DmpBbo, a set of libraries and programs for the
# black-box optimization of dynamical movement primitives.
# Copyright (C) 2018 Freek Stulp
#
# DmpBbo is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# DmpBbo is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DmpBbo.  If not, see <http://www.gnu.org/licenses/>.


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, sys


from dmpbbo.dmp.Dmp import *
from dmpbbo.functionapproximators.FunctionApproximatorRBFN import *

if __name__ == "__main__":

    tau = 0.5
    n_dims = 2
    n_time_steps = 51

    y_init = np.linspace(0.0, 0.7, n_dims)
    y_attr = np.linspace(0.4, 0.5, n_dims)

    ts = np.linspace(0, tau, n_time_steps)
    y_yd_ydd_viapoint = np.array([-0.2, 0.4, 0.0, 0.0, 0, 0])
    viapoint_time = 0.4 * ts[-1]
    traj = Trajectory.from_viapoint_polynomial(
        ts, y_init, y_yd_ydd_viapoint, viapoint_time, y_attr
    )

    function_apps = [FunctionApproximatorRBFN(10, 0.7) for i_dim in range(n_dims)]
    # dmp_type='IJSPEERT_2002_MOVEMENT'
    dmp_type = "KULVICIUS_2012_JOINING"
    # dmp_type='COUNTDOWN_2013'
    dmp = Dmp.from_traj(traj, function_apps, dmp_type)

    tau_exec = 0.7
    n_time_steps = 71
    ts = np.linspace(0, tau_exec, n_time_steps)

    (xs_ana, xds_ana, forcing_terms_ana, fa_outputs_ana) = dmp.analyticalSolution(ts)

    dt = ts[1]
    xs_step = np.zeros([n_time_steps, dmp._dim_x])
    xds_step = np.zeros([n_time_steps, dmp._dim_x])

    (x, xd) = dmp.integrateStart()
    xs_step[0, :] = x
    xds_step[0, :] = xd
    for tt in range(1, n_time_steps):
        (xs_step[tt, :], xds_step[tt, :]) = dmp.integrateStep(dt, xs_step[tt - 1, :])

    print("Plotting")

    Dmp.plotStatic(
        tau,
        ts,
        xs_ana,
        xds_ana,
        forcing_terms=forcing_terms_ana,
        fa_output=fa_outputs_ana,
    )
    plt.gcf().canvas.set_window_title("Analytical integration")

    Dmp.plotStatic(tau, ts, xs_step, xds_step)
    plt.gcf().canvas.set_window_title("Step-by-step integration")

    lines, axs = traj.plot()
    plt.setp(lines, linestyle="-", linewidth=4, color=(0.8, 0.8, 0.8))
    plt.setp(lines, label="demonstration")

    traj_reproduced = dmp.statesAsTrajectory(ts, xs_step, xds_step)
    lines, axs = traj_reproduced.plot(axs)
    plt.setp(lines, linestyle="--", linewidth=2, color=(0.0, 0.0, 0.5))
    plt.setp(lines, label="reproduced")

    plt.legend()
    plt.gcf().canvas.set_window_title("Comparison between demonstration and reproduced")

    plt.show()