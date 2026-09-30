# notebooks/

Exploratory ML notebooks: feature exploration, training experiments logged
to MLflow, evaluation analysis. Notebooks are not part of the shipped
application and must not be imported from `src/aiseo`.

Any code that becomes production inference logic belongs in
`src/aiseo/adapters/ml/` behind the `ModelProvider` port, not here.
