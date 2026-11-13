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

  // called when a node is added, communicates with backend and creates a node in WorkFlow
  void onNodeAdd(NodeInstance node) async
  {
      // tells backend to create a node and awaits response
      var response = await http.post(
      Uri.parse('http://127.0.0.1:8000/new_node'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: json.encode({"image_operation": node.definition.type, "id": node.id}),
    );
    // decodes response from json to map
    if (response.statusCode == 200)
    {
      var responseDecode = json.decode(response.body);

      // if the response is not that a node with the correct id was created in backend, delete the node from frontend
      if (responseDecode["status"] != "created" || responseDecode["node"] != node.id)
      {
        deleteNode(node.id);
      }
    }
  }


  void onRemove(Iterable<NodeId> nodes, Iterable edges) async
  {
      // tells backend to create a node and awaits response
      var response = await http.post(
      Uri.parse('http://127.0.0.1:8000/remove'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: json.encode({"nodes": nodes, "edges": edges}),
    );
    var responseDecode = json.decode(response.body);
    if (responseDecode["status"] == "failed")
    {
      // if removal wasn't sucessful on backend, undo removal on frontend
      undo();

    }

  }
  void onConnectionAdd(Edge connection) async
  {
      var response = await http.post(
      Uri.parse('http://127.0.0.1:8000/add_connection'),
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: json.encode({
        "id": connection.id,
        "source_node": connection.source.node, 
        "source_port": connection.source.port, 
        "target_node": connection.target.node,
        "target_port": connection.target.port}),
    );
    var responseDecode = json.decode(response.body);
    if (responseDecode["status"] == "failed")
    {
      remove(edges:[connection.id]);
    }


  }
  CustomNodeEditorController({
    required super.registry,
    //this.onNodeAdd,
  });



  @override
  // remove is used to remove edges, remove nodes and to remove selections (ie, a node with attached edges, a group of nodes)
  // This is done with as a single command with a single undo step.
  // Because this is a single command with a single undo, it needs to be sent to the backend as a single command with a single response
  void remove({
    Iterable<NodeId> nodes = const [],
    Iterable<EdgeId> edges = const [],
    bool userAction = false,
  }) {

    super.remove(
      nodes: nodes,
      edges: edges,
      userAction: userAction
    );
    onRemove(nodes, edges);


  }
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

// overrides the connect function to create a new edge
// this will have a default id in the form connection.######### which is created by the connect function
// this id will then be passed to the backend, rather than using the previous iterating integer id method
// there is an option to copy the entire connect code to the override to adjust how connection ids are generated, but doesn't seem
// worth the effort
  @override
    Edge? connect(
    PortRef a,
    PortRef b, {
    EdgeStyle? style,
    String? label,
    bool userAction = false,
  })
  {
    final Edge? edge = super.connect(a, b,
      style:style,
      label:label,
      userAction:userAction);

    if (edge != null){
      onConnectionAdd(edge);
    }
    return edge;
  }

  //TODO - NEED REDO FOR REMOVE and ADDING CONNECTIONS
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
          for (final connection in c.edges){
          onConnectionAdd(connection);
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

    for (final edge in edges){
      print("edge added back?");
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

