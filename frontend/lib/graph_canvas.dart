import 'package:flutter/material.dart';
import 'package:node_program_editor/node_program_editor.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';


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