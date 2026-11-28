import 'dart:typed_data';
import 'package:frontend/notifiers.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'dart:convert';

class ImageData {
  late int zMax;
  late int cMax;
  late Uint8List imageBytes;

  ImageData.fromDict(Map<String, dynamic> json) {
    zMax = (json['z_max'] as int?) ?? 0;
    cMax = (json['c_max'] as int?) ?? 0;
    imageBytes = base64Decode(json['image_bytes']);
  }
}

Future <ImageData> getImageData(String nodeID, String portID, int z, int c, int centreX, int centreY, double zoom) async {
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
      "centre_x": centreX, 
      "centre_y": centreY, 
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
  final ImageStateController imageController;
  const ImageCanvas({super.key, required this.imageController});
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

  late Future<ImageData> _imageFuture;
  @override
  void initState() {
    super.initState();
    _imageFuture = getImageData(widget.imageController.NodeID ?? "", widget.imageController.PortID ?? "", _z, _c, _centre_x, _centre_y, _zoom);
  }
  @override
  void didUpdateWidget(covariant ImageCanvas oldWidget) {
    super.didUpdateWidget(oldWidget);
    _imageFuture = getImageData(widget.imageController.NodeID ?? "", widget.imageController.PortID ?? "", widget.imageController.Z ?? 0, _c, _centre_x, _centre_y, _zoom);
    }

  double _currentSliderValue = 1;
  @override
  Widget build(BuildContext context) {
  return Center(
      child: FutureBuilder(
        future: _imageFuture,
        builder: (context, snapshot) {
            if (snapshot.hasError) 
            {
              return Text('Error: ${snapshot.error}');
            } 
            else if (snapshot.hasData) 
            {
              // get data from snapshot
              return Center(child: Stack(
                children: [
                  Image.memory(snapshot.data!.imageBytes, width: 512, height: 512, gaplessPlayback: true,),
                  if (snapshot.data!.zMax != 1)
                    Positioned(bottom:0, left:0, right:0, child: Opacity(
                      opacity: 0.3,
                      child: Slider(
                        activeColor: Colors.grey.shade100,
                        max: snapshot.data!.zMax.toDouble(),
                        min: 1,
                        divisions: snapshot.data!.zMax,
                        value:_currentSliderValue,
                        onChanged: (double value)
                        {
                          setState(() 
                          {
                          _currentSliderValue = value;
                          widget.imageController.updateImageSelection(widget.imageController.NodeID!, widget.imageController.PortID!, value.toInt()-1);
                          });
                        }
                        )
                      )
                    )
                ] ));
            }
            else 
            {
              return const Text('No data available');
            } 
          },
        )

    );
  } 
}