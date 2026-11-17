These rough estimates cover loaded index memory with memory mapping disabled. Calculate them per segment, then sum across loaded segments and replicas.

<div class="alert note">

> Allow extra memory for loaded field data, vector indexes, collection and index overhead, and temporary allocations. Validate with representative data and queries; arrays, JSON, older index formats, and memory mapping require separate measurement.

</div>
