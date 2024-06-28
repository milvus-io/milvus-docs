---
id: configure_indexcoord.md
related_key: configure
group: system_configuration.md
summary: Learn how to configure indexCoord for Milvus.
---

# indexCoord-related Configurations



## `indexCoord.bindIndexNodeMode.enable`

<table id="indexCoord.bindIndexNodeMode.enable">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `indexCoord.bindIndexNodeMode.address`

<table id="indexCoord.bindIndexNodeMode.address">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>localhost:22930</td>
    </tr>
  </tbody>
</table>


## `indexCoord.bindIndexNodeMode.withCred`

<table id="indexCoord.bindIndexNodeMode.withCred">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>false</td>
    </tr>
  </tbody>
</table>


## `indexCoord.bindIndexNodeMode.nodeID`

<table id="indexCoord.bindIndexNodeMode.nodeID">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0</td>
    </tr>
  </tbody>
</table>


## `indexCoord.segment.minSegmentNumRowsToEnableIndex`

<table id="indexCoord.segment.minSegmentNumRowsToEnableIndex">
  <thead>
    <tr>
      <th class="width80">Description</th>
      <th class="width20">Default Value</th> 
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <li>It's a threshold. When the segment num rows is less than this value, the segment will not be indexed</li>      </td>
      <td>1024</td>
    </tr>
  </tbody>
</table>


