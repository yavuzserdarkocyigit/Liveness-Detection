import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'dart:async';
import 'package:http/http.dart' as http;
import 'dart:convert';

List<CameraDescription>? cameras;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> with TickerProviderStateMixin {
  CameraController? _controller;
  Future<void>? _initializeControllerFuture;
  String _decision = '';
  int selectedCameraIndex = 0;
  AnimationController? _animationController;
  bool _showVerifyButton = false;
  bool _showCamera = false;

  @override
  void initState() {
    super.initState();
    _animationController = AnimationController(
      duration: const Duration(seconds: 3),
      vsync: this,
    );
    _animationController!.forward().whenComplete(() {
      setState(() {
        _showVerifyButton = true;
      });
    });
  }

  void initializeCamera(int cameraIndex) {
    _controller = CameraController(cameras![cameraIndex], ResolutionPreset.medium);
    _initializeControllerFuture = _controller!.initialize().then((_) {
      setState(() {
        _showCamera = true;
        captureImagesPeriodically();
      });
    });
  }

  void switchCamera() {
    selectedCameraIndex = (selectedCameraIndex + 1) % cameras!.length;
    initializeCamera(selectedCameraIndex);
  }

  void captureImagesPeriodically() {
    Timer.periodic(Duration(seconds: 1), (timer) async {
      if (_controller != null && _controller!.value.isInitialized) {
        XFile image = await _controller!.takePicture();
        await sendImageToServer(image.path);
      }
    });
  }

  Future<void> sendImageToServer(String imagePath) async {
    var request = http.MultipartRequest('POST', Uri.parse('http://172.20.10.3:5000/upload')); //172.20.10.3, 192.168.1.42
    request.files.add(await http.MultipartFile.fromPath('picture', imagePath));
    try {
      var response = await request.send();
      if (response.statusCode == 200) {
        var responseData = await response.stream.bytesToString();
        var decodedData = jsonDecode(responseData);
        setState(() {
          // Update to include percentage in decision text
          _decision = '${decodedData['decision']} (${decodedData['percentage']})';
        });
      }
    } catch (e) {
      // Exception handling
    }
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              FadeTransition(
                opacity: Tween(begin: 1.0, end: 0.0).animate(CurvedAnimation(parent: _animationController!, curve: Curves.easeOut)),
                child: Text('dolares', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
              ),
              if (_showVerifyButton && !_showCamera) ElevatedButton(
                onPressed: () {
                  setState(() {
                    _showVerifyButton = false;
                    initializeCamera(selectedCameraIndex);
                  });
                },
                child: Text('Verify')
              ),
              if (_showCamera && _controller != null) Expanded(
                child: FutureBuilder<void>(
                  future: _initializeControllerFuture,
                  builder: (context, snapshot) {
                    if (snapshot.connectionState == ConnectionState.done) {
                      return CameraPreview(_controller!);
                    } else {
                      return CircularProgressIndicator();
                    }
                  },
                ),
              ),
              if (_showCamera) Text(
                _decision,
                style: TextStyle(
                  fontSize: 24,
                  color: _decision.contains("Real") ? Colors.green : (_decision.contains("Fake") ? Colors.red : Colors.black),
                ),
              ),
              if (_showCamera) ElevatedButton(
                onPressed: switchCamera,
                child: Text('Change the Cam')
              ),
            ],
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    _animationController?.dispose();
    _controller?.dispose();
    super.dispose();
  }
}
