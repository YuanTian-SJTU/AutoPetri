# PNML 文件格式规范说明

Petri Net Markup Language（PNML）是一种基于 XML 的标准化格式，用于描述和交换 Petri 网模型。PNML 文件的结构遵循严格的语法规则，以确保模型在不同工具之间的一致性和互操作性。以下是对 PNML 文件格式的规范说明，结合具体示例进行解读。

## 1. 文件根元素和 XML 声明

- **XML 声明**：PNML 文件以标准的 XML 声明开头，指定文件版本和字符编码。
  ```xml
  <?xml version="1.0" ?>
  ```
  - 示例中使用了 `version="1.0"`，这是标准的 XML 声明，通常不需要额外的编码属性（如 `encoding`），默认使用 UTF-8。

- **根元素 `<pnml>`**：PNML 文件的根元素是 `<pnml>`，包含所有 Petri 网的定义。
  ```xml
  <pnml>
    ...
  </pnml>
  ```
  - `<pnml>` 元素没有属性要求，但通常包含一个或多个 `<net>` 子元素。

## 2. 网络定义 `<net>`

- **`<net>` 元素**：表示一个 Petri 网，包含整个模型的定义。
  - 必须包含 `id` 属性，用于唯一标识网络。
  - 必须包含 `type` 属性，指定 Petri 网的类型，通常是一个 URI，指向 PNML 标准中的语法定义。
  ```xml
  <net id="net1" type="http://www.pnml.org/version-2009/grammar/ptnet">
  ```
  - 示例中，`id="net1"` 是网络的唯一标识，`type="http://www.pnml.org/version-2009/grammar/ptnet"` 表示这是一个 Place/Transition 网（P/T 网），遵循 2009 版 PNML 标准。

- **子元素**：`<net>` 包含以下主要子元素：
  - `<place>`：定义位置（Place）。
  - `<transition>`：定义变迁（Transition）。
  - `<arc>`：定义连接（Arc）。
  - 其他可选元素（如 `<page>`、`<referencePlace>` 等）。

## 3. 位置 `<place>`

- **`<place>` 元素**：表示 Petri 网中的一个位置，通常用于表示状态或资源。
  - 必须包含 `id` 属性，唯一标识该位置。
  ```xml
  <place id="___T1">
  ```
  - 示例中，`id="___T1"` 是位置的唯一标识，命名中避免使用特殊字符以确保兼容性。

- **子元素**：
  - **`<name>`**：位置的名称，用于可视化显示。
    ```xml
    <name>
      <text>仓库-T1</text>
    </name>
    ```
    - 示例中，`<text>仓库-T1</text>` 表示位置的名称为“仓库-T1”。
  - **`<initialMarking>`**：初始标记，表示位置的初始资源量（通常为非负整数）。
    ```xml
    <initialMarking>
      <text>180</text>
    </initialMarking>
    ```
    - 示例中，`仓库-T1` 的初始标记为 180。
  - **`<graphics>`**：定义位置的可视化坐标。
    ```xml
    <graphics>
      <position x="100" y="100"/>
    </graphics>
    ```
    - 示例中，`仓库-T1` 的位置坐标为 (100, 100)，用于工具（如 WOPEd）中的图形渲染。
  - **自定义扩展（如 `<attribute>`）**：PNML 支持扩展元素，用于添加非标准信息。
    ```xml
    <attribute name="location">
      <longitude>112.9388</longitude>
      <latitude>28.2282</latitude>
    </attribute>
    ```
    - 示例中，添加了一个名为 `location` 的自定义属性，包含经纬度信息（经度 112.9388，纬度 28.2282）。这种扩展需要在工具中明确支持，否则可能被忽略。

## 4. 变迁 `<transition>`

- **`<transition>` 元素**：表示 Petri 网中的一个变迁，通常用于表示事件或任务。
  - 必须包含 `id` 属性，唯一标识该变迁。
  ```xml
  <transition id="___001">
  ```
  - 示例中，`id="___001"` 是变迁的唯一标识。

- **子元素**：
  - **`<name>`**：变迁的名称。
    ```xml
    <name>
      <text>任务-001</text>
    </name>
    ```
    - 示例中，变迁的名称为“任务-001”。
  - **`<graphics>`**：定义变迁的可视化坐标。
    ```xml
    <graphics>
      <position x="1300" y="100"/>
    </graphics>
    ```
    - 示例中，`任务-001` 的坐标为 (1300, 100)。

## 5. 连接 `<arc>`

- **`<arc>` 元素**：表示 Petri 网中的连接，连接 Place 和 Transition。
  - 必须包含 `id` 属性，唯一标识该连接。
  - 必须包含 `source` 和 `target` 属性，分别指定连接的起点和终点（可以是 Place 或 Transition）。
  ```xml
  <arc id="arc____T1_trans____T1____S1" source="___T1" target="trans____T1____S1">
  ```
  - 示例中，`id="arc____T1_trans____T1____S1"` 是连接的唯一标识，`source="___T1"` 表示起点为 `仓库-T1`，`target="trans____T1____S1"` 表示终点为运输变迁。

- **子元素**：
  - **`<graphics>`**：定义连接的路径，通常包含多个 `<position>` 点。
    ```xml
    <graphics>
      <position x="100" y="100"/>
      <position x="250" y="100"/>
    </graphics>
    ```
    - 示例中，连接的路径从 (100, 100) 到 (250, 100)，对应于起点和终点的坐标。
  - **`<inscription>`**：定义连接的权重，通常表示资源流动的数量。
    ```xml
    <inscription>
      <text>3.4</text>
    </inscription>
    ```
    - 示例中，`<inscription>` 的值为 3.4，表示运输时间（尽管语义上更适合放在 Transition 上，此处用作权重）。

## 6. 规范要求和最佳实践

- **语法规范**：
  - PNML 文件必须是格式良好的 XML，标签必须正确嵌套且闭合。
  - 所有 `id` 必须唯一，`source` 和 `target` 必须引用已定义的 Place 或 Transition。
  - Petri 网的语义要求 Arc 只能连接 Place 和 Transition（即 Place → Transition 或 Transition → Place），不能直接连接 Place 和 Place 或 Transition 和 Transition。
- **类型指定**：
  - `type` 属性应明确指定 Petri 网的类型（如 P/T 网、时间 Petri 网等），以确保工具正确解析。
  - 示例中使用了 `http://www.pnml.org/version-2009/grammar/ptnet`，表示标准的 Place/Transition 网。
- **图形信息**：
  - `<graphics>` 是可选的，但如果提供，应包含合理的 `<position>` 值，避免所有点为 (0, 0)，否则可能导致渲染问题。
  - 示例中为 Arc 提供了起点和终点的坐标，确保连边渲染正确。
- **扩展和自定义**：
  - PNML 支持通过 `<attribute>` 或 `<toolSpecific>` 添加自定义信息，但这些信息需要工具支持。
  - 示例中为 Place 添加了经纬度信息，适合地理相关的应用，但可能不被所有工具识别。
- **语义准确性**：
  - 确保 `<inscription>` 表示权重（通常为正整数），而非其他属性（如时间）。
  - 时间或延迟信息应放在 Transition 上，使用 `<delay>` 或自定义注解。

## 7. 示例文件的特点

- **结构完整性**：文件包含了 Place、Transition 和 Arc，符合 Petri 网的基本结构。
- **图形信息**：为 Place、Transition 和 Arc 提供了 `<graphics>`，便于可视化工具（如 WOPEd）渲染。
- **扩展信息**：为 Place 添加了经纬度信息，适合描述地理位置，但需要工具支持。
- **改进建议**：
  - 运输时间（如 3.4）应移到 Transition 上，作为自定义注解（如 `<annotation><text>time=3.4</text></annotation>`）。
  - 多个 Transition 的坐标重叠（如 `任务-001` 至 `任务-006` 都在 (1300, 100)），建议错开以提高可视化可读性。

## 8. 总结

PNML 是一种灵活且标准化的 Petri 网描述语言，支持基本的 Place/Transition 网结构以及扩展属性。规范的 PNML 文件应包含完整的 `<net>` 定义，合理的 Place、Transition 和 Arc 元素，并提供适当的图形信息以支持可视化。自定义扩展（如经纬度）可以增强模型的表达能力，但需确保工具兼容性。