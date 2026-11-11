import 'package:flutter/material.dart';
import 'package:node_program_editor/node_program_editor.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


// define a class to Type data imported from backend
class TypeListItem{
  late String name;
  late Color color;
  late List<String> compatibleWith;

  TypeListItem.fromDict(Map<String, dynamic> json) {
    name = (json['name'] as String?) ?? "";
    color = Color(int.parse('0xFF${json['color'].replaceAll('#', '')}'));
    compatibleWith = json['compatibleWith'] != null 
      ? List<String>.from(json['compatibleWith']) 
      : [];

  }
}

// define class to hold port data as part of Node descriptions imported from backend
class PortDescription{
  late String name;
  late String label;
  late String type;
  late bool isInput;
  
  PortDescription.fromDict(Map<String, dynamic> json) {
    name = (json['id'] as String?) ?? "";
    label = (json['name'] as String?) ?? "";
    type = (json['dtype'] as String?) ?? "";
    isInput = (json['is_input'] as bool?) ?? true;
  }
}


class ParameterDescription{
  late String name;
  late String label;
  late ParamType type;
  late Map<String,dynamic> options;


  ParameterDescription.fromDict(Map<String, dynamic> json) {
    name = (json['id'] as String?) ?? "";
    label = (json['name'] as String?) ?? "";
    options = (json['user_input_options'] as Map<String,dynamic>);
    if ((json['user_input_method'] as String?) == "integer")
    {
      type = IntParam(min: options["min"] ?? 0, 
                                                max: options["max"] ?? 10, 
                                                step: options["step"] ?? 1, 
                                                slider: options["slider"] ?? false,
                                                unit: "");
    }
    else if ((json['user_input_method'] as String?) == "dropdown")
    {
      type = EnumParam.values(List<String>.from(options["values"]));
    }
    else
    {
      type = TextParam();
    }



  }
  
}

// define class to hold descriptions of Nodes for canvas pallete (distinct from node lists in workflow), imported from backend
class NodeDescription{
  String id = "";
  String name = "";
  String category = "";
  String docs = "";
  String alerts = "";
  late List<PortDescription> ports;
  late List<ParameterDescription> parameters;

  NodeDescription.fromDict(Map<String, dynamic> json) {
    id = (json['id'] as String?) ?? "";
    name = (json['name'] as String?) ?? "";
    category = (json['category'] as String?) ?? "";
    docs = (json['docs'] as String?) ?? "";
    alerts = (json['alerts'] as String?) ?? "";
    ports = json['ports'] != null 
      ? List<PortDescription>.from(json['ports'].map((portJson) => PortDescription.fromDict(portJson))) 
      : [];
    parameters = json['parameters'] != null
      ? List<ParameterDescription>.from(json['parameters'].map((parameterJson) => ParameterDescription.fromDict(parameterJson)))
      : [];

  }
}
Future<List<NodeDescription>> getNodeDefinitionsList() async {
    final response = await http.get(
    Uri.parse('http://127.0.0.1:8000/operations'),
    headers: {'Accept': 'application/json'},);
    if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
      final decodedNodeDescription = (jsonDecode(response.body) as Map<String, dynamic>);
      List<NodeDescription> imageOperationList = [for (var value in decodedNodeDescription.values) NodeDescription.fromDict(value)];
      return imageOperationList;
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load ImageOperationListItem');
    }
}

Future<List<TypeListItem>> getTypeList() async {
    final response = await http.get(
    Uri.parse('http://127.0.0.1:8000/types'),
    headers: {'Accept': 'application/json'},);
    if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
      final decodedType = (jsonDecode(response.body) as Map<String, dynamic>);
      List<TypeListItem> typeList = [for (var value in decodedType.values) TypeListItem.fromDict(value)];
      return typeList;
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load TypeListItem');
    }
}

// extends NodeEditorController with custom commands for adding, deleting and editing nodes and
// adding and deleting connections to call relevant backend functions
class CustomNodeEditorController extends NodeEditorController
{
  int identifier = 0;
  void onNodeAdd(NodeInstance node)
  {
    print(node.id);
  }

  void onConnectionAdd(Edge Connection)
  {
    print(Connection.id);
  }
  CustomNodeEditorController({
    required super.registry,
    //this.onNodeAdd,
  });

  // overrides addNode to custom ID on addition and run onNodeAdd
  @override
  NodeInstance addNode(
    String type, {
    required Offset position,
    Map<String, Object?>? params,
    NodeId? id,
    String? title,
    bool select = true,
  }) {
    // newID in format node.image_operation_name.integer
    String newID = ["node", type.toString(), identifier].join(".");
    // increment identifier
    identifier ++ ;

    // run normal addNode function
    final newNode = super.addNode(
      type,
      position: position,
      params: params,
      id: NodeId(newID),
      title: title,
      select: select,
    );

    // call onNodeAdd
    onNodeAdd(newNode);
    return(newNode);
  }

  // overrides undo for changes to nodes/edges
  // changes to id not needed (or possible here), as custom ID would have been created on initial element addition
  @override
  void undo() {
    final c = history.takeUndo();
    if (c != null) {
      batch(() => c.revert(this));

      if (c is RemoveElementsCommand) {
        for (final node in c.nodes) {
          onNodeAdd(node);
        }
        for (final connection in c.edges){
          onConnectionAdd(connection);
        }
      }
    }
  }

  // likewise for redo-ing undone additions
  @override
  void redo() {
    final c = history.takeRedo();
    if (c != null) {
      batch(() => c.apply(this));

      if (c is AddElementsCommand) {
        for (final node in c.nodes) {
          onNodeAdd.call(node);
        }
      }
    }
  }
  @override
  void addElements(
    List<NodeInstance> nodes,
    List<Edge> edges, {
    String label = 'Add',
  }) {
    // 1. Run the parent logic first so nodes and edges are restored to the graph
    super.addElements(nodes, edges, label: label);

    // 2. Notify your custom handler for each restored/pasted node
    for (final node in nodes) {
      onNodeAdd.call(node);
    }
  }
}




class WorkflowCanvas extends StatefulWidget {
  const WorkflowCanvas({super.key});
  @override
    State<WorkflowCanvas> createState() => _WorkflowCanvasState();
}
class _WorkflowCanvasState extends State<WorkflowCanvas> {
  // Safe: Handled once per page lifecycle
  late final Future<List<dynamic>> _initDataFuture;
  @override
  void initState() {
    super.initState();
    // Fires both network calls simultaneously in isolation
    _initDataFuture = Future.wait([getNodeDefinitionsList(), getTypeList()]);
  }

  @override
  Widget build(BuildContext context) {
  return Scaffold(
    body: Center(
      child: FutureBuilder<List<dynamic>>(
        future: _initDataFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const CircularProgressIndicator();
            } 
            else if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
              } 
              else if (snapshot.hasData) {
                // get typeList from http
                final typeList = snapshot.data![1];
                // convert typeList to actual PortType instances
                final portTypes = {
                  for (var type in typeList)
                    type.name: PortType(type.name, color: type.color, compatibleWith: Set<String>.from(type.compatibleWith)),
                };
                // get nodeDefinitionsList from http
                final nodeDefinitionsList = snapshot.data![0];

                // define node registry based on nodeDefinitionsList
                final registry = NodeRegistry(definitions: [
                  for (var nodeDef in nodeDefinitionsList)
                    NodeDefinition(
                      type: nodeDef.id,
                      title: nodeDef.name,
                      category: nodeDef.category, 
                      variant: NodeVariant.dynamic,
                      copyable: false,
                      style: NodeStyle(headerColor: Color(0xFF888888)),
                      ports: [
                        for (var port in nodeDef.ports)
                          if (port.isInput)
                            PortSpec.input(port.name, label: port.label, side: PortSide.top, type: portTypes[port.type] ?? PortType.any)
                          else
                            PortSpec.output(port.name, label: port.label, side: PortSide.bottom, type: portTypes[port.type] ?? PortType.any),
                      ],
                      params: [
                        for (var parameter in nodeDef.parameters)
                            ParamSpec(parameter.name, parameter.type, label: parameter.label)
                      ],
                    ),
                ]);
                // create node pallete based on registry
                final controller = CustomNodeEditorController(registry: registry);
                controller.canvasSettings.value = const CanvasSettings(
                  gridStyle: GridStyle.none,     // none, dots, lines, cross
                  gridSpacing: 20,                // also the snapping step
                  majorEvery: 5,                  // major line every 5 cells (≤ 1 disables)
                  snapToGrid: true,               // node moves and resizes
                  snapEdgesToGrid: true,          // edge waypoints
                  defaultEdgeStyle: EdgeStyle(pathType: EdgePathType.smoothStep),
                  gridColor: null, majorGridColor: null, backgroundColor: null,
);

                final nodePallete = NodePalette(
                  controller: controller,
                  mode: NodePaletteMode.drag,        // click, drag or both
                  layout: NodePaletteLayout.compact,    // list, grid or compact
                  showSearch: true,
                  showFilters: false,                 // category chips + port type filter
                  title: 'Image Operations',
                  filter: (def) => !def.tags.contains('hidden'),
                  categoryOrder: ['Input/Outut', 'Selection', 'Filters'],
                  initiallyCollapsed: {'Advanced'},
                  itemBuilder: null,                 // custom item (tap / drag still handled)
                  headerBuilder: null,               // custom category header
                  );
                final canvas = NodeCanvas(controller: controller);
                //controller.revision.addListener((){
                    //Future.microtask(() {
                      //final lastCommand = controller.history.undoLabel;
                      //print("Stabilized change: $lastCommand");
                      //final output = controller.history._undo[controller.history.undoDepth - 1];
                    //});
// if
                  //});
                final output = Row(children: [
                  SizedBox(width: 280, child: nodePallete), 
                  Expanded(child: canvas),
                  ],
                  );
                return output;

                } 
                else {
                  return const Text('No data available');
                } 
              },
            )
    )
    );
  } 
}




final registry = NodeRegistry(definitions: [
  NodeDefinition(
    type: 'math.add',
    title: 'Add',
    category: 'Math',
    icon: Icons.add,
    variant: NodeVariant.dynamic,
    ports: const [
      PortSpec.input('a', label: 'a', type: PortType.number),
      PortSpec.input('b', label: 'b', type: PortType.number),
      PortSpec.output('sum', label: 'sum', type: PortType.number),
    ],
    params: const [
      ParamSpec('bias', DoubleParam(min: -10, max: 10, slider: true), showInNode: true),
    ],
  ),
]);

