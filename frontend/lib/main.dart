import 'package:flutter/material.dart';
import 'package:frontend/image_canvas.dart';
import 'graph_canvas.dart';
import 'notifiers.dart';

void main(){
  runApp(const MyApp());
}



class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Easy Image Analysis',
      theme: ThemeData(

        colorScheme: .fromSeed(seedColor: Colors.grey),
      ),
      home: const MyHomePage(title: 'Easy Image Analysis'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        toolbarHeight: 50,
        backgroundColor: Colors.blueGrey.shade400,//Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Row(spacing: 5, mainAxisAlignment: MainAxisAlignment.center,
        children: [
                      ListenableBuilder(
              listenable: leftCanvas,
              builder: (BuildContext context, Widget? child) {
                return ImageCanvas(imageController: leftCanvas);
              },
            ),
                        ListenableBuilder(
              listenable: rightCanvas,
              builder: (BuildContext context, Widget? child) {
                return ImageCanvas(imageController: rightCanvas);
              },
            ),
          SizedBox(
            width: 600,   // Provide a defined width
            height: 512,  // Provide a defined height
            child: WorkflowCanvas()
          ),

        
        ]),
      //floatingActionButton: FloatingActionButton(
      //  onPressed: _incrementCounter,
       // tooltip: 'Increment',
       // child: const Icon(Icons.add),
      //),
    )
    );
  }
}
