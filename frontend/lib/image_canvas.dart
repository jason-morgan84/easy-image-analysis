import 'dart:typed_data';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'dart:convert';

//TODO:
// update load and save image nodes to actually load and save images
// implement means of changing ImageStateController values from graph
// test if it works

class ImageData {
  late int zMax;
  late int cMax;
  late Uint8List imageBytes;

  ImageData.fromDict(Map<String, dynamic> json) {
    zMax = (json['z_max'] as int?) ?? 0;
    cMax = (json['c_max'] as int?) ?? 0;
  }
}

Future <ImageData> getImageData(String nodeID, String portID, int z, int c, int centerX, int centerY, double zoom) async {
    final response = await http.post(
    Uri.parse('http://127.0.0.1:8000/image'),
    headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
    body: json.encode({
      "node": nodeID, 
      "port": portID, 
      "z": z, 
      "c": c, 
      "center_x": centerX, 
      "center_y": centerY, 
      "zoom": zoom}),
    );
    if (response.statusCode == 200) {
      final decodedNodeDescription = (jsonDecode(response.body) as Map<String, dynamic>);
      final receivedImageData = ImageData.fromDict(decodedNodeDescription);
      return receivedImageData;
  } else {
    throw Exception('Failed to load ImageOperationListItem');
    }
}

class ImageCanvas extends StatefulWidget {
  final String nodeID;
  final String portID;
  const ImageCanvas({super.key, required this.nodeID, required this.portID});
  @override
    State<ImageCanvas> createState() => _ImageCanvasState();
}
class _ImageCanvasState extends State<ImageCanvas> {
  // Safe: Handled once per page lifecycle
  int _z = 0;
  int _c = 0;
  int _centre_y = 256;
  int _centre_x = 256;
  double _zoom = 1.0;

  late Future _imageFuture;


  /*@override
  void initState() {
    super.initState();
    _triggerFetch();
  }*/

  @override
  void didUpdateWidget(covariant ImageCanvas oldWidget) {
    super.didUpdateWidget(oldWidget);
    // Re-fetch if either nodeID or portID changed from parent
    if (widget.nodeID != oldWidget.nodeID || widget.portID != oldWidget.portID) {
      _imageFuture = getImageData(widget.nodeID, widget.portID, _z, _c, _centre_x, _centre_y, _zoom);
    }
  }

  @override
  Widget build(BuildContext context) {
  return Center(
      child: FutureBuilder(
        future: _imageFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const CircularProgressIndicator();
            } 
            else if (snapshot.hasError) {
              return Text('Error: ${snapshot.error}');
              } 
              else if (snapshot.hasData) {

                // get data from snapshot

                final output = Text("Image to come");
                return output;

                } 
                else {
                  return const Text('No data available');
                } 
              },
            )

    );
  } 
}