# Adult Census Income Prediction Using Neural Networks

## 1. Project Overview

This project uses deep learning to predict whether an individual's annual income exceeds $50,000 using demographic and employment-related features from the Adult Census dataset.

The project focuses on building and comparing neural network architectures, experimenting with optimisers and learning rates, tracking experiments using MLflow, and evaluating model performance.

## 2. Project Objectives

- Prepare the dataset for neural network training.
- Handle missing values and encode categorical variables.
- Scale numerical features.
- Split the data into training, validation, and test sets.
- Build and compare at least three neural network models.
- Experiment with different optimisers and learning rates.
- Use MLflow to track parameters, metrics, and model artefacts.
- Investigate overfitting and apply techniques to improve generalisation.
- Select the best model using validation metrics and evaluate it on the test set.

## 3. Dataset and Preprocessing

**Dataset:** Adult Census Income Dataset

The preprocessing steps include:

- Inspecting the dataset and analysing missing values.
- Encoding categorical variables into numerical representations.
- Scaling numerical features where appropriate.
- Separating input features from the target variable.
- Splitting the data into training, validation, and test sets.

The validation set is used for model selection and hyperparameter tuning. The test set is reserved for final evaluation.

## 4. Neural Network Architectures

Three neural network architectures were developed and compared.

### Model 1: Baseline MLP

A baseline Multilayer Perceptron containing two hidden layers with ReLU activation and a sigmoid output layer.

### Model 2: Deeper DNN

A deeper neural network with additional hidden layers to investigate whether increased model capacity improves predictive performance.

### Model 3: Regularised DNN

A neural network incorporating dropout and batch normalisation to help control overfitting and improve generalisation.

All models use a sigmoid output for binary classification and binary cross-entropy as the loss function.

## 5. Model Training and Evaluation

The models are trained using training data and monitored using validation data.

The following metrics are used to evaluate performance:

- **Accuracy:** Overall proportion of correct predictions.
- **Precision:** Proportion of positive predictions that are correct.
- **Recall:** Proportion of actual positive cases correctly identified.
- **F1-score:** Harmonic mean of precision and recall.
- **ROC-AUC:** Ability to distinguish between the two classes across classification thresholds.

F1-score is used as the primary model-selection metric, with ROC-AUC and the other metrics used for additional comparison.

Early stopping monitors validation loss and restores the model weights from the best validation-loss epoch.

## 6. Hyperparameter Experiments

Experiments investigate the effects of different optimisers and learning rates on model performance.

The planned optimiser experiments compare Adam and SGD using learning rates of 0.1, 0.01, and 0.001. The architecture experiments also compare network depth, layer sizes, dropout, and other relevant settings.

The results are compared using validation metrics and training/validation loss curves. Only experiments that were actually run should be reported as completed.

## 7. MLflow Experiment Tracking

MLflow is used to record and compare neural network experiments.

The experiment is named **Adult Census - Week 2 Neural Networks**.

The tracked information includes:

- Model architecture and layer configuration.
- Optimiser and learning rate.
- Batch size and training epochs.
- Training and validation loss.
- Accuracy, precision, recall, F1-score, and ROC-AUC, where logged.
- Relevant model artefacts, such as loss curves and saved models.

MLflow's experiment comparison interface helps identify the most promising model and understand how architecture and hyperparameter changes affect performance.

## 8. Overfitting Investigation

Training and validation loss curves were analysed for all three architectures.

The initial experiments showed signs of overfitting: training loss continued to decrease while validation loss stopped improving or increased slightly.

To investigate this, the Deeper DNN was modified by reducing the number of neurons, introducing dropout, and lowering the learning rate from 0.001 to 0.0005. Early stopping was also used to restore the weights from the best validation-loss epoch.

The updated model's best validation loss was approximately 0.3183, compared with 0.3178 for the original Deeper DNN. Therefore, the changes did not improve minimum validation loss, although the updated validation-loss curve was relatively stable.

This demonstrates that regularisation and reduced model complexity do not necessarily improve every evaluation metric. The models must be compared using validation performance rather than relying on loss curves alone.

## 9. Results and Model Selection

The validation results from the architecture comparison were:

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Baseline MLP | 0.8509 | 0.7183 | 0.6267 | 0.6694 | 0.9069 |
| Regularised DNN | 0.8528 | 0.7325 | 0.6122 | 0.6670 | 0.9067 |
| Deeper DNN | 0.8499 | 0.7191 | 0.6182 | 0.6648 | 0.9065 |

The Baseline MLP was selected as the provisional preferred model because it achieved the highest validation F1-score and ROC-AUC among the three architectures.

Although the Regularised DNN achieved the highest validation accuracy and precision, it did not outperform the Baseline MLP in F1-score or ROC-AUC. The Deeper DNN also did not demonstrate an improvement from its additional complexity.

The final model choice should be confirmed through evaluation on the held-out test set.

## 10. Project Structure

The repository is organised to keep the notebook, documentation, and supporting evidence together.

```text
week2/
└── <your-name>/
    ├── README.md
    ├── *.ipynb
    └── screenshots/
        ├── mlflow_experiments.png
        ├── model_comparison.png
        └── loss_curves.png
```

Adjust the filenames to match the actual files in your repository. Include only screenshots and artefacts that exist.

## 11. How to Run the Project

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies listed in `requirements.txt`, if provided.
4. Open the Jupyter Notebook.
5. Run the cells in order to prepare the data, train the models, and evaluate their performance.
6. Start the MLflow UI using the tracking configuration specified in the project.
7. Review the recorded experiments and compare the results.

## 12. Conclusion

This project demonstrates the application of neural networks to a binary classification problem, including data preprocessing, architecture design, hyperparameter experimentation, MLflow tracking, and model evaluation.

The experiments highlight the importance of validation-based model selection and show that increasing network complexity does not guarantee better performance. Overfitting was investigated using loss curves, early stopping, and regularisation techniques.

The final model is selected based on validation performance and should be evaluated on the held-out test set to assess its generalisation to unseen data.
