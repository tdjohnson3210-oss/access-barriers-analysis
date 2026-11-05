# Project Lab Notebook
## Washington State Civil Filings Forecasting Dashboard

### Purpose
This notebook serves as a chronological record of project changes, decisions, and outcomes. It complements the GitHub repository by documenting the reasoning behind key decisions and providing context that may not be fully captured in commit histories.

---

### Week 2: Literature Review and Problem Refinement

- Conducted a review of access-to-justice, transportation, and civil court participation literature.
- Identified transportation as a potential access barrier that has received limited attention within access-to-justice research.
- Refined the research question to focus on whether transportation barriers are associated with differences in civil filing activity.

### Week 3: Dataset Identification and Initial Project Design

- Identified public ACS and RUCA datasets capable of supporting transportation and community-level barrier analysis.
- Located Court Statistics Project (CSP) data to provide a national-level civil court component.
- Developed an initial plan to conduct a national analysis by combining transportation and community indicators with civil filing data.
- Noted potential concerns regarding geographic aggregation because ACS data were available at the tract level while court data were reported at higher levels of aggregation.

### Week 4: Integration Challenges and Scope Reassessment

- Began integrating ACS, RUCA, and CSP data into a single analytical framework.
- Encountered significant aggregation challenges due to differences in geographic levels of analysis.
- Determined that the CSP data did not contain tract-level civil filing measures and therefore could not provide a direct target variable aligned with the ACS data.
- Identified a growing disconnect between available court outcomes and the original research design.

### Week 5: Model Development Difficulties

- Constructed preliminary modeling workflows using the available national datasets.
- Found that model outputs were difficult to interpret within the context of the research question.
- Determined that the available outcome measures were not adequately capturing county-level civil court participation.
- Concluded that the modeling approach required substantial revision before meaningful conclusions could be drawn.

### Week 6: Dataset Redesign and Washington Pilot Selection

- Revisited the project scope and reviewed alternative court data sources.
- Selected Washington State as a pilot site due to the availability of county-level civil filing data through publicly accessible court records.
- Replaced the original secondary dataset with Washington civil filing data.
- Redesigned the integration workflow to better align transportation barriers, community characteristics, and civil filing outcomes.

### Week 7: Metric Development and County Comparisons

- Continued refining county-level transportation and access-barrier measures.
- Encountered challenges defining metrics that would allow meaningful comparison across counties of different sizes.
- Evaluated several approaches for representing filing activity and transportation risk.
- Developed a simplified framework that incorporated population and geographic context while preserving county-level comparability.
- Finalized the modeling and dashboard metrics used throughout the project.

### Week 8: Report Consolidation and Final Refinement

- Reviewed and revised deliverables produced during previous project phases.
- Consolidated exploratory analysis, modeling, evaluation, and deployment documentation into a single report structure.
- Updated narrative sections to reflect methodological changes made during development.
- Incorporated final visualizations, deployment documentation, and dashboard outputs.
- Prepared project materials for final submission and future expansion.
