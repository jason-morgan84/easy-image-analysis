import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(

        colorScheme: .fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
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

class ImageOperationListItem{
  String id = "";
  String name = "";
  String category = "";
  String docs = "";
  String alerts = "";

  ImageOperationListItem.fromDict(Map<String, dynamic> json) {
    id = (json['id'] as String?) ?? "";
    name = (json['name'] as String?) ?? "";
    category = (json['category'] as String?) ?? "";
    docs = (json['docs'] as String?) ?? "";
    alerts = (json['alerts'] as String?) ?? "";

  }
}
Future<List<ImageOperationListItem>> getOperationsList() async {
    final response = await http.get(
    Uri.parse('http://127.0.0.1:8000/operations'),
    headers: {'Accept': 'application/json'},);
    if (response.statusCode == 200) {
    // If the server did return a 200 OK response,
    // then parse the JSON.
      final decodedItem = (jsonDecode(response.body) as Map<String, dynamic>);
      List<ImageOperationListItem> imageOperationList = [for (var value in decodedItem.values) ImageOperationListItem.fromDict(value)];
      return imageOperationList;
  } else {
    // If the server did not return a 200 OK response,
    // then throw an exception.
    throw Exception('Failed to load ImageOperationListItem');
    }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  late final Future<List<TypeListItem>> _operationsFuture  = getTypeList();
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(

        backgroundColor: Theme.of(context).colorScheme.inversePrimary,

        title: Text(widget.title),
      ),
      body: Center(
        // 3. Use FutureBuilder to watch the network request
        child: FutureBuilder<List<TypeListItem>>(
          future: _operationsFuture,
          builder: (context, snapshot) {
            // State A: Still fetching data -> Show a loading indicator
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const CircularProgressIndicator();
            }
            
            // State B: An error occurred (e.g., server offline, 404)
            if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
            }

            // State C: Successfully retrieved data
            if (snapshot.hasData) {
              final operations = snapshot.data!;

              // If the list is empty, show a friendly message
              if (operations.isEmpty) {
                return const Text('No operations found.');
              }

              // Return your layout with the populated data
              return Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    'Operations:',
                    style: TextStyle(fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 10),
                  // Loop through the items safely now that they exist
                  for (var operation in operations)
                    Text(
                      operation.name,
                      style: TextStyle(color: operation.color)
                    ),
                ],
              );
            }

            // Fallback state
            return const Text('No data available');
          },
        ),
      ),
      //floatingActionButton: FloatingActionButton(
      //  onPressed: _incrementCounter,
       // tooltip: 'Increment',
       // child: const Icon(Icons.add),
      //),
    );
  }
}
