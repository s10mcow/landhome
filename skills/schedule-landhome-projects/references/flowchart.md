# High-level scheduling view

Adapt to actual applicability. Arrows express dependencies, not durations. Home procurement and utility planning continue on parallel paths with their own later release checks.

```mermaid
flowchart TD
    A["Contract: confirm access, DD deadline and budget"] --> B["Survey and septic evaluation"]
    A --> C["Home information, utility planning and trade pricing"]
    B --> D["Coordinate site plan and site budget"]
    C --> D
    D --> E["Requity purchase decision and closing"]
    D --> F["Well and septic permits, if required"]
    D --> G["Prepare remaining permit documents"]
    F --> H["Complete filing and required permit issuance"]
    G --> H
    E --> I["Verify sitework release requirements"]
    H --> I
    I --> J["Prepare access, pad and utility work"]
    J --> K["Verify site, home and delivery crew readiness"]
    C -.-> K
    K --> L["Deliver, set and overlap compatible trades"]
    L --> M["GC subcontractor scope complete"]
    L --> N["Complete utilities, testing and agency closeout"]
    C -.-> N
    N --> O["CO issued: ready for occupancy"]
```

State separately: preclosing filing depends on office acceptance; sitework requires applicable ownership/authority, permits and commencement documentation; well/septic installation order depends on access; closeout coordination starts early. GC completion and CO are separate milestones and can have different dates.
