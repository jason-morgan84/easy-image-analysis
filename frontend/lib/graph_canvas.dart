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

// define class to hold descriptions of Nodes for canvas pallete (distinct from node lists in workflow), imported from backend
class NodeDescription{
  String id = "";
  String name = "";
  String category = "";
  String docs = "";
  String alerts = "";
  late List<PortDescription> ports;
  late List<PortDescription> parameters;

  NodeDescription.fromDict(Map<String, dynamic> json) {
    id = (json['id'] as String?) ?? "";
    name = (json['name'] as String?) ?? "";
    category = (json['category'] as String?) ?? "";
    docs = (json['docs'] as String?) ?? "";
    alerts = (json['alerts'] as String?) ?? "";
    ports = json['ports'] != null 
      ? List<PortDescription>.from(json['ports'].map((portJson) => PortDescription.fromDict(portJson))) 
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
      final decodedItem = (jsonDecode(response.body) as Map<String, dynamic>);
      List<NodeDescription> imageOperationList = [for (var value in decodedItem.values) NodeDescription.fromDict(value)];
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
      final decodedItem = (jsonDecode(response.body) as Map<String, dynamic>);
      List<TypeListItem> typeList = [for (var value in decodedItem.values) TypeListItem.fromDict(value)];
      return typeList;
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load TypeListItem');
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
                final typeList = snapshot.data![0];
                // convert typeList to actual PortType instances
                final portTypes = {
                  for (var type in typeList)
                    type.id: PortType(type.name, color: type.color, compatibleWith: Set<String>.from(type.compatibleWith)),
                };
                // get nodeDefinitionsList from http
                final nodeDefinitionsList = snapshot.data![1];

                // define node registry based on nodeDefinitionsList
                final registry = NodeRegistry(definitions: [
                  for (var nodeDef in nodeDefinitionsList)
                    NodeDefinition(
                      type: nodeDef.id,
                      title: nodeDef.name,
                      category: nodeDef.category,
                      icon: Icons.extension, // You can customize the icon based on your needs
                      variant: NodeVariant.dynamic,
                      ports: [
                        for (var port in nodeDef.ports)
                          if (port.isInput)
                            PortSpec.input(port.name, label: port.label, type: portTypes[port.type.id] ?? PortType.any)
                          else
                            PortSpec.output(port.name, label: port.label, type: portTypes[port.type.id] ?? PortType.any),
                      ],
                    ),
                ]);
                // create node pallete based on registry
                final controller = NodeEditorController(registry: registry);
                final nodePallete = NodePalette(
                  controller: controller,
                  mode: NodePaletteMode.both,        // click, drag or both
                  layout: NodePaletteLayout.list,    // list, grid or compact
                  showSearch: true,
                  showFilters: true,                 // category chips + port type filter
                  title: 'Nodes',
                  filter: (def) => !def.tags.contains('hidden'),
                  categoryOrder: ['Triggers', 'Actions', 'Flow'],
                  initiallyCollapsed: {'Advanced'},
                  itemBuilder: null,                 // custom item (tap / drag still handled)
                  headerBuilder: null,               // custom category header
                  );
                final canvas = NodeCanvas(controller: controller);
                return Row(children: [nodePallete, canvas],);

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

