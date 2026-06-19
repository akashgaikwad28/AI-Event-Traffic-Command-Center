# DATASET INTELLIGENCE REPORT
**GridWise AI - Traffic Operations Command Center**

## 1. Structural Overview
- **Total Row Count:** 8,173
- **Total Column Count:** 46
- **Memory Usage:** ~14.9 MB
- **Duplicate Rows:** 0
- **Duplicate Event IDs:** 0 (Unique `id` count: 8,173)

## 2. Column Typology
- **Datetime Columns:** `start_datetime`, `resolved_datetime`, `closed_datetime`, `modified_datetime`, `end_datetime`, `created_date`
- **Categorical Columns (High Cardinality):** `address` (3,089), `description` (5,542), `veh_no` (4,212), `created_by_id` (1,898), `kgid` (1,853), `closed_by_id` (1,225)
- **Categorical Columns (Low Cardinality):** `event_type` (2), `status` (3), `priority` (2), `requires_road_closure` (2), `veh_type` (10), `event_cause` (17), `corridor` (22)
- **Numerical Columns (Coordinates):** `latitude`, `longitude`, `endlatitude`, `endlongitude`

## 3. Sparsity & Missing Data Profile
The dataset exhibits extreme sparsity in several critical operational fields, dictating a highly resilient imputation strategy.

### **100% Null (Useless metadata)**
- `map_file`, `comment`, `meta_data`

### **>95% Null (Dangerously Sparse)**
- `resolved_datetime` (99.09% null - **CRITICAL: Cannot be used for targets**)
- `direction` (99.47%)
- `cargo_material`, `reason_breakdown`, `age_of_truck` (96.62%)
- `assigned_to_police_id`, `citizen_accident_id` (98.43%)
- `route_path` (98.32%)

### **>50% Null (Operationally Incomplete)**
- `end_datetime` (94.00%)
- `end_address` (91.59%)
- `junction` (69.29%)
- `closed_by_id` (61.57%)
- `closed_datetime` (61.57% null - **Will be used as the primary duration target**)
- `zone` (57.86%)
- `gba_identifier` (57.86%)

### **Moderately Sparse (Requires Imputation)**
- `veh_type`, `veh_no` (40.21%)
- `description` (16.64%)

## 4. Geo-Spatial Discovery
A massive differentiator for the GridWise architecture is the discovery that categorical spatial labels (`zone`: 57% null, `junction`: 69% null) are highly unreliable. However, **raw coordinate completeness is near perfect** (`latitude`/`longitude` are 100% complete, minus invalid bounds outliers).

**Conclusion:** The architecture must pivot from "Category-Based Routing" to **"Coordinate-First Spatial Intelligence"**, relying heavily on unsupervised DBSCAN clustering to dynamically reconstruct missing zones and junctions.
