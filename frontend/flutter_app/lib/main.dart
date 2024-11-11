import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart'; // Import the generated options
import 'package:flutter_app/screens/splash_screen.dart'; // Import the splash screen

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,  // This will load platform-specific config
    );

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'Horizon',
      themeMode: ThemeMode.system,
      home: SplashScreen(), // Set SplashScreen as the home screen
    );
  }
}
