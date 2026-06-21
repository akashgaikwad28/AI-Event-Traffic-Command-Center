# Dataset Analysis and Geo-Sparsity Impact

Extensive analysis of the historical incident data revealed critical flaws in traditional data structures, leading to the adoption of our current spatial intelligence architecture.

## Flaws in the Original Dataset
The original dataset heavily relied on manually entered junction labels and rigid, static map zones.
- **Sparsity:** A significant percentage of incidents lacked accurate junction or zone labels.
- **Rigidity:** Static zones failed to adapt to actual, dynamic operational traffic hotspots. 
- **Predictive Bottleneck:** Machine learning models relying on these categorical features performed poorly when attempting to generalize to unseen or sparsely labeled areas.

## Geo-Sparsity Failure Impact
During our failure analysis (documented in `13_failure_analysis.ipynb`), we evaluated the impact of missing spatial context:
- We correlated prediction errors against the density of historical incidents.
- Incidents occurring in highly dense, recurring hotspots showed much lower prediction error.
- **Noise Clusters:** Incidents falling into sparse areas—classified as "noise" (`DBSCAN cluster ID -1`) by our unsupervised clustering algorithm—exhibited significantly higher prediction errors.

## Conclusion and Pivot
The dataset analysis clearly indicated that a reliance on text-based zones is a liability. The architecture was deliberately pivoted to a **Coordinate-First** approach.

By feeding raw `latitude` and `longitude` coordinates directly into a DBSCAN clustering module, we synthesize our own operational geography. This ensures that every incident, regardless of its manually entered labels, is situated accurately within the city's true historical risk topology.
