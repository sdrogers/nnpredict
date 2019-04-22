# nnpredict


## Shifts strategies

Location: shifts branch

Codes to run: 
- nnpredict/Code/Python/Shifts_vs_Conv.ipynb (shift vs conv experiment)
- nnpredict/Code/Python/Shifts_vs_NoShifts.ipynb (shifts vs no shifts in integer mass binning)

For shift vs conv experiment, first need to calculate baseline from dataset

Location: baselineAUC branch

Codes to run: 
- nnpredict/Code/Python/create_save_gnps35000.ipynb (process files)
- nnpredict/Code/Python/calculate_baselineAUC.ipynb (calculate score)


## Binning strategies

### Integer mass binning

Location: int_binning_strategies branch

Codes to run: 
- nnpredict/Code/Python/create_bins.ipynb (create all the necessary files for binning)
- nnpredict/Code/Python/load_bins_train_model.ipynb (load the files into bins and train model, including results)

### Tree binning

Location: new_tree_binning branch

Codes to run:
- nnpredict/Code/Python/Code/Python/process_trees_files.ipynb (extract fragments/losses from tree, appear >3 trees)
- nnpredict/Code/Python/Code/Python/tree_binning.ipynb (tree vs integer mass binning)
- nnpredict/Code/Python/Shifts_vs_NoShifts_in_tree_binning.ipynb (shifts vs no shifts in tree binning)


## Final solution (Tree-free model)

Location: new_tree_binning branch

### Comparison with Tree and Integer mass binning
Codes to run: 
- nnpredict/Code/Python/Code/Python/Final_vs_Int_Tree.ipynb (tree-free vs tree and integer mass binning)

### Comparison with CSI
Codes to run:
- nnpredict/Code/Python/Code/Python/process_ALL_GNPS.ipynb (process dataset for CSI:FingerID prediction)
- nnpredict/Code/Python/Code/Python/create_batches.py (create small batches for CSI to run)
- nnpredict/Code/Python/Code/Python/run_csi_script.py (run CSI:FingerID prediction on the small batches)
- nnpredict/Code/Python/Code/Python/Final_vs_CSI.ipynb (results for tree-free model against CSI)
