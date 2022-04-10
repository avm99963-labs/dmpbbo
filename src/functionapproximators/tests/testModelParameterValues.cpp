/**
 * \file testModelParameterValues.cpp
 * \author Freek Stulp
 *
 * This file is part of DmpBbo, a set of libraries and programs for the 
 * black-box optimization of dynamical movement primitives.
 * Copyright (C) 2014 Freek Stulp, ENSTA-ParisTech
 * 
 * DmpBbo is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 2 of the License, or
 * (at your option) any later version.
 * 
 * DmpBbo is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License
 * along with DmpBbo.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <iostream>
#include <string>
#include <set>


#include "functionapproximators/ModelParametersLWR.hpp"

using namespace std;
using namespace Eigen;
using namespace DmpBbo;

int main(int n_args, char** args)
{
  int n_basis_functions = 3; 
  //int n_dims = 1;
  
  vector<ModelParameters*> model_parameters;
  
  // LWR
  VectorXd centers = VectorXd::LinSpaced(n_basis_functions,30,50);
  VectorXd widths  = VectorXd::Zero(n_basis_functions);
  VectorXd offsets = (100.0*VectorXd::Random(n_basis_functions)).cast<int>().cast<double>().array().abs();
  VectorXd slopes  = VectorXd::Ones(n_basis_functions);
  
  model_parameters.push_back(new ModelParametersLWR(centers, widths, slopes, offsets));
  
  for (unsigned int mm=0; mm<model_parameters.size(); mm++)
  {
    ModelParameters* mp = model_parameters[mm];
    
    cout << "____________________________________________________________________" << endl;
    cout << *mp << endl << endl;
    
    set<string> selected_labels;  
    
    // LWR (also GMR partially)
    //selected_labels.insert("widths");
    //selected_labels.insert("offsets");
    selected_labels.insert("slopes");
    selected_labels.insert("centers");
    
    mp->setSelectedParameters(selected_labels);
    
    cout << "vector size (all     ) = " << mp->getParameterVectorAllSize() << endl;
    cout << "vector size (selected) = " <<  mp->getParameterVectorSelectedSize() << endl;
    
    VectorXi selected_mask;
    mp->getParameterVectorMask(selected_labels,selected_mask);
    cout << "mask = " << selected_mask.transpose() << endl << endl;
    
    VectorXd values, min_values, max_values, values_normalized;
    
    mp->getParameterVectorAll(values);
    //mp->getParameterVectorAllMinMax(min_values,max_values);
  
    cout << "values     (all     ): " << values.transpose() << endl;
    //cout << "min_values (all     ): " << min_values.transpose() << endl;
    //cout << "max_values (all     ): " << max_values.transpose() << endl << endl;
    
    mp->getParameterVectorSelected(values);
    mp->getParameterVectorSelectedMinMax(min_values,max_values);
    mp->getParameterVectorSelectedNormalized(values_normalized);
    cout << "values     (selected): " << values.transpose() << endl;
    cout << "min_values (selected): " << min_values.transpose() << endl;
    cout << "max_values (selected): " << max_values.transpose() << endl ;
    cout << "values_norm(selected): " << values_normalized.transpose() << endl << endl;
    
    VectorXd new_values = VectorXd::LinSpaced(mp->getParameterVectorSelectedSize(),2,20);
    mp->setParameterVectorSelected(new_values);
  
    mp->getParameterVectorAll(values);
    //mp->getParameterVectorAllMinMax(min_values,max_values);
  
    cout << "values     (all     ): " << values.transpose() << endl;
    //cout << "min_values (all     ): " << min_values.transpose() << endl;
    //cout << "max_values (all     ): " << max_values.transpose() << endl << endl;
    
    mp->getParameterVectorSelected(values);
    mp->getParameterVectorSelectedMinMax(min_values,max_values);
    mp->getParameterVectorSelectedNormalized(values_normalized);
    cout << "values     (selected): " << values.transpose() << endl;
    cout << "min_values (selected): " << min_values.transpose() << endl;
    cout << "max_values (selected): " << max_values.transpose() << endl;
    cout << "values_norm(selected): " << values_normalized.transpose() << endl << endl;
    
    new_values = VectorXd::LinSpaced(mp->getParameterVectorSelectedSize(),0.49,0.51);
    mp->setParameterVectorSelectedNormalized(new_values);
  
    mp->getParameterVectorAll(values);
    //mp->getParameterVectorAllMinMax(min_values,max_values);
  
    cout << "values     (all     ): " << values.transpose() << endl;
    //cout << "min_values (all     ): " << min_values.transpose() << endl;
    //cout << "max_values (all     ): " << max_values.transpose() << endl << endl;
    
    mp->getParameterVectorSelected(values);
    mp->getParameterVectorSelectedMinMax(min_values,max_values);
    mp->getParameterVectorSelectedNormalized(values_normalized);
    cout << "values     (selected): " << values.transpose() << endl;
    cout << "min_values (selected): " << min_values.transpose() << endl;
    cout << "max_values (selected): " << max_values.transpose() << endl;
    cout << "values_norm(selected): " << values_normalized.transpose() << endl << endl;
  }
  
  
  return 0;
}


