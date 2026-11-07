import 'package:flutter/material.dart';
import 'package:node_program_editor/node_program_editor.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


class NodeDescription{
  String id = "";
  String name = "";
  String category = "";
  String docs = "";
  String alerts = "";

  NodeDescription.fromDict(Map<String, dynamic> json) {
    id = (json['id'] as String?) ?? "";
    name = (json['name'] as String?) ?? "";
    category = (json['category'] as String?) ?? "";
    docs = (json['docs'] as String?) ?? "";
    alerts = (json['alerts'] as String?) ?? "";

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

class TypeListItem{
  late String id;
  late String name;
  late Color color;
  late List<String> compatibleWith;

  TypeListItem.fromDict(Map<String, dynamic> json) {
    id = (json['id'] as String?) ?? "";
    name = (json['name'] as String?) ?? "";
    color = Color(int.parse('0xFF${json['color'].replaceAll('#', '')}'));
    compatibleWith = json['compatibleWith'] != null 
      ? List<String>.from(json['compatibleWith']) 
      : [];

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

class WorkflowCanvas extends StatelessWidget {
  late final List<NodeDefinition> nodeDefinitions;

  late final Future<List<TypeListItem>> _typeListFuture  = getTypeList();
  late final Future<List<NodeDescription>> _nodeDefinitionsFuture = getNodeDefinitionsList();
  @override
  Widget build(BuildContext context) {
        return Scaffold(
          body: Center(
            child: FutureBuilder<List<TypeListItem>>(
              future: _typeListFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const CircularProgressIndicator();
                } else if (snapshot.hasError) {
                  return Text('Error: ${snapshot.error}');
                } else if (snapshot.hasData) {
                  final typeList = snapshot.data!;
                  return _typeListFuture;
                } else {
                  return const Text('No data available');
                }
              },
            ),
            child: FutureBuilder<List<NodeDescription>>(
              future: _nodeDefinitionsFuture,
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const CircularProgressIndicator();
                } else if (snapshot.hasError) {
                  return Text('Error: ${snapshot.error}');
                } else if (snapshot.hasData) {
                  final nodeDefinitions = snapshot.data!;
                  return _nodeDefinitionsFuture;
                } else {
                  return const Text('No data available');
                }
              },
            ),
          ),
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

