import 'package:flutter/material.dart';

class ImageStateController extends ChangeNotifier {
  String? NodeID;
  String? PortID;
  int? Z;

  void updateImageSelection(String nodeID, String portID, int z)
  {
    NodeID = nodeID; 
    PortID = portID; 
    Z = z;
    notifyListeners();
  }
}

ImageStateController leftCanvas = ImageStateController();

ImageStateController rightCanvas = ImageStateController();
