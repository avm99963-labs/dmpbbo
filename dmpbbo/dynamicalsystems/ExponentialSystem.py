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
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with DmpBbo.  If not, see <http://www.gnu.org/licenses/>.
#
""" Module for the ExponentialSystem class. """

import numpy as np

from dmpbbo.dynamicalsystems.DynamicalSystem import DynamicalSystem


class ExponentialSystem(DynamicalSystem):
    """ A dynamical system representing exponential decay.
    """

    def __init__(self, tau, x_init, x_attr, alpha):
        """ Initialize an ExponentialSystem.

        @param tau: Time constant
        @param x_init: Initial state
        @param x_attr: Attractor state
        @param alpha: Decay constant
        """
        super().__init__(1, tau, x_init)
        self._x_attr = x_attr
        self.alpha = alpha

    @property
    def y_attr(self):
        """ Return the y part of the attractor state.

        Note that for an ExponentialSystem y is equivalent to x.
        """
        return self._x_attr

    @y_attr.setter
    def y_attr(self, y):
        """ Set the y part of the attractor state.

        Note that for an ExponentialSystem y is equivalent to x.
        """
        if y.size != self._dim_y:
            raise ValueError(f"y_attr must have size {self._dim_y}")
        self._x_attr = np.atleast_1d(y)

    @property
    def x_attr(self):
        """ Get the y part of the attractor state.

        Note that for an ExponentialSystem y is equivalent to x.
        """
        return self._x_attr

    @x_attr.setter
    def x_attr(self, x):
        """ Set the attractor state.

        Note that for an ExponentialSystem y is equivalent to x.
        """
        if x.size != self._dim_x:
            raise ValueError(f"y_attr must have size {self._dim_x}")
        self._x_attr = np.atleast_1d(x)

    def differential_equation(self, x):
        """ The differential equation which defines the system.

        It relates state values to rates of change of those state values.

        @param x: current state
        @return: xd - rate of change in state
        """
        xd = self.alpha * (self._x_attr - x) / self._tau
        return xd

    def analytical_solution(self, ts):
        """
         Return analytical solution of the system at certain times.

         @param ts: A vector of times for which to compute the analytical solutions
         @return: (xs, xds) - Sequence of states and their rates of change.
        """
        n_ts = ts.size

        exp_term = np.exp(-self.alpha * ts / self._tau)
        pos_scale = exp_term
        vel_scale = -(self.alpha / self._tau) * exp_term

        val_range = self._x_init - self._x_attr
        val_range_repeat = np.repeat(np.atleast_2d(val_range), n_ts, axis=0)
        pos_scale_repeat = np.repeat(np.atleast_2d(pos_scale), self._dim_x, axis=0)
        xs = np.multiply(val_range_repeat, pos_scale_repeat.T)

        xs = xs + np.repeat(np.atleast_2d(self._x_attr), n_ts, axis=0)

        vel_scale_repeat = np.repeat(np.atleast_2d(vel_scale), self._dim_x, axis=0)
        xds = np.multiply(val_range_repeat, vel_scale_repeat.T)

        return xs, xds
