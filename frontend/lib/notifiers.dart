import 'package:flutter/material.dart';

class ImageStateController extends ChangeNotifier {
  String? NodeID;
  String? PortID;

  void updateImageSelection(String nodeID, String portID)
  {
    NodeID = nodeID; 
    PortID = portID; 
    notifyListeners();
  }
}

ImageStateController leftCanvas = ImageStateController();

late ImageStateController rightCanvas = ImageStateController();
